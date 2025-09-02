import os
import sys
import time
import base64
from pathlib import Path
from typing import Dict, Any

from dotenv import load_dotenv
from openai import OpenAI
import requests


# =========================
# Configuración
# =========================
SYSTEM_PROMPT = (
    "Eres un asistente de inteligencia artificial dedicado a la "
    "creación de planes de dictado de clase para educadores y "
    "profesores de primaria y secundaria."
)

MODEL_TEXT = "gpt-4o"        # cámbialo si quieres otro modelo
MODEL_IMAGE = "gpt-image-1"  # DALL·E 3 vía API

OUT_DIR = Path("outputs")
OUT_DIR.mkdir(exist_ok=True)

MAX_RETRIES = 3
RETRY_BACKOFF_SEC = 4  # exponencial: 4s, 8s, 16s...


# =========================
# Utilidades
# =========================
def ensure_api_key() -> str:
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("❌ Falta OPENAI_API_KEY en tu .env", file=sys.stderr)
        sys.exit(1)
    return api_key


def with_retries(fn, *args, **kwargs):
    """
    Ejecuta 'fn' con reintentos ante errores transitorios (p.ej., 429/timeout).
    """
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            return fn(*args, **kwargs)
        except Exception as e:
            msg = str(e)
            is_last = attempt == MAX_RETRIES
            # Tolerante a variaciones del mensaje
            if any(s in msg.lower() for s in ["429", "rate limit", "timeout"]):
                if is_last:
                    raise
                sleep_s = RETRY_BACKOFF_SEC * (2 ** (attempt - 1))
                print(f"⚠️  Intento {attempt}/{MAX_RETRIES} falló ({msg}). "
                      f"Reintentando en {sleep_s}s…")
                time.sleep(sleep_s)
            else:
                # Errores no transitorios: salimos
                raise


def save_text(content: str, basename: str) -> Path:
    txt_path = OUT_DIR / f"{basename}.txt"
    md_path = OUT_DIR / f"{basename}.md"
    txt_path.write_text(content, encoding="utf-8")
    md_path.write_text(f"{content}\n", encoding="utf-8")
    return txt_path


def save_image_from_b64(b64_data: str, basename: str) -> Path:
    img_path = OUT_DIR / f"{basename}.png"
    img_bytes = base64.b64decode(b64_data)
    img_path.write_bytes(img_bytes)
    return img_path


def download_image(url: str, basename: str) -> Path:
    img_path = OUT_DIR / f"{basename}.png"
    r = requests.get(url, timeout=60)
    r.raise_for_status()
    img_path.write_bytes(r.content)
    return img_path


def _validate_markdown_plan(md: str) -> bool:
    """Validación simple del esquema esperado en Markdown."""
    required = [
        "## Objetivos de aprendizaje",
        "## Contenidos clave",
        "## Actividades",
        "## Evaluación formativa",
        "## Materiales y recursos",
        "## Adaptaciones (NEE)",
    ]
    return all(section in md for section in required)


# =========================
# OpenAI wrappers
# =========================
def make_client(api_key: str) -> OpenAI:
    return OpenAI(api_key=api_key)


def generate_lesson_plan(client: OpenAI, user_topic: str,
                         model: str = MODEL_TEXT,
                         temperature: float = 0.4,   # estabilidad
                         max_tokens: int = 900) -> str:
    """
    Genera el plan de clase como texto en formato Markdown (CRAFT).
    """
    tema = user_topic.strip()
    duracion_min = 40
    nivel = "Secundaria"

    # tiempos sugeridos
    t_inicio = max(5, duracion_min // 5)
    t_desarrollo = max(15, duracion_min // 2)
    t_cierre = max(5, duracion_min // 6)

    # ---- CRAFT ----
    context = (
        f"Contexto: Clase de {nivel} sobre \"{tema}\" con duración total de "
        f"{duracion_min} minutos en aula estándar, sin equipamiento especial."
    )
    role = f"Rol: Eres un asistente educativo experto en planificación didáctica para {nivel}."
    action = (
        "Acción: Redacta un plan de clase completo y aplicable en el aula, con "
        "tareas factibles y evaluación formativa."
    )
    format_md = (
        "Formato: Responde en Markdown estrictamente con este esquema:\n\n"
        f"# Plan de clase: {tema}\n"
        "## Objetivos de aprendizaje\n"
        "## Contenidos clave\n"
        "## Actividades\n"
        f"- Inicio (~{t_inicio} min):\n"
        f"- Desarrollo (~{t_desarrollo} min):\n"
        f"- Cierre (~{t_cierre} min):\n"
        "## Evaluación formativa (3 preguntas)\n"
        "## Materiales y recursos\n"
        "## Adaptaciones (NEE)\n"
    )
    tone = (
        "Tono: claro, inclusivo, didáctico y adecuado al nivel. "
        "Evita jerga técnica innecesaria."
    )
    constraints = (
        "Restricciones: tiempos coherentes; 3 preguntas de evaluación; "
        "incluir al menos 1 adaptación; no inventes bibliografía ni enlaces."
    )

    prompt_text = f"{context}\n{role}\n{action}\n{format_md}\n{tone}\n{constraints}"

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": prompt_text},
    ]

    def _call():
        return client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            top_p=0.95,
            n=1,
        )

    resp = with_retries(_call)
    content = resp.choices[0].message.content.strip()

    if not _validate_markdown_plan(content):
        print("⚠️ El plan no cumple el formato esperado. Considera reintentar.", file=sys.stderr)
    return content


def generate_image(client: OpenAI,
                   concepts: str,
                   model: str = MODEL_IMAGE,
                   size: str = "1024x1024",
                   prefer_b64: bool = True) -> Dict[str, Any]:
    """
    Genera la imagen (DALL·E). Devuelve un dict con:
        {"saved_path": Path, "from": "b64"|"url"}
    """
    # ---- CRAFT para imagen ----
    context = "Context: Educational material to accompany a lesson plan."
    role = "Role: You are an assistant that designs neutral, didactic illustrations."
    action = (
        "Action: Generate a clean, uncluttered illustration that helps students "
        "understand the theme without including any text."
    )
    format_hint = (
        "Format: 1024x1024 PNG. Composition centered, clear lines, minimal elements."
    )
    tone = "Tone: neutral, textbook-style, suitable for classroom use."

    style = (
        "Minimal, textbook-style educational illustration, neutral colors, "
        "clear lines, uncluttered composition, didactic tone, no text."
    )

    final_prompt = (
        f"{context}\n{role}\n{action}\n{format_hint}\n{tone}\n\n"
        f"Theme/subject: {concepts}\n\n"
        f"Style guide: {style}"
    )

    def _call():
        return client.images.generate(
            model=model,
            prompt=final_prompt,
            size=size,
            n=1
        )

    resp = with_retries(_call)

    # Guarda la imagen (prioriza b64 si está disponible)
    basename = f"lesson_image_{int(time.time())}"
    data0 = resp.data[0]
    if prefer_b64 and hasattr(data0, "b64_json") and data0.b64_json:
        img_path = save_image_from_b64(data0.b64_json, basename)
        return {"saved_path": img_path, "from": "b64"}
    else:
        url = getattr(data0, "url", None)
        if not url:
            raise RuntimeError("La respuesta de imagen no contiene b64 ni URL.")
        img_path = download_image(url, basename)
        return {"saved_path": img_path, "from": "url"}


# =========================
# CLI principal
# =========================
def main():
    api_key = ensure_api_key()
    client = make_client(api_key)

    # 1) Texto
    user_topic = input("Ingrese el tema para el plan de clase: ").strip()
    if not user_topic:
        print("❌ Debes ingresar un tema.")
        sys.exit(1)

    try:
        lesson = generate_lesson_plan(client, user_topic)
        print("\n--- Plan de Clase (Markdown) ---\n")
        print(lesson)
        ts = int(time.time())
        text_path = save_text(lesson, f"lesson_plan_{ts}")
        print(f"\n✅ Plan guardado en: {text_path.parent.resolve()}")
    except Exception as e:
        print(f"❌ Error al generar el plan de clase: {e}")
        sys.exit(1)

    # 2) Imagen
    concepts = input("\nIngrese los conceptos/tema para la imagen del plan de clase: ").strip()
    if not concepts:
        print("ℹ️ Saltando la generación de imagen (no se ingresaron conceptos).")
        return

    try:
        result = generate_image(client, concepts, prefer_b64=True)
        print(f"\n✅ Imagen guardada en: {result['saved_path'].resolve()}")
    except Exception as e:
        print(f"❌ Error al generar la imagen: {e}")


if __name__ == "__main__":
    main()