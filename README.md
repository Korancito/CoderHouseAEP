Proyecto Final – Pre Entrega #2
Autor: Francisco Gabriel Borgno Larroque
Curso: [Prompt Engineering]
Comisión: [Nº 84180]

Título del proyecto: Asistente de planificación educativa con generación automática de prompts

Presentación del problema
La planificación escolar es una tarea central para los docentes, que requiere combinar organización, creatividad y adaptación a distintos niveles educativos. En la práctica, los educadores enfrentan obstáculos frecuentes:
•	Escasez de tiempo para diseñar materiales atractivos y variados.
•	Dificultad para adaptar contenidos a distintos niveles de complejidad y estilos de aprendizaje.
•	Limitada disponibilidad de recursos visuales didácticos, actualizados y libres de licencias costosas.
Esta problemática repercute en la calidad de la enseñanza y en la carga laboral de los docentes. En este contexto, resulta relevante explorar herramientas de IA generativa que apoyen la planificación y producción de materiales educativos.

Desarrollo de la propuesta de solución
La propuesta consiste en el desarrollo de un Asistente Inteligente de Planificación Educativa, que aproveche la generación de prompts optimizados para obtener:
1.	Recursos de texto (modelo texto–texto):
o	Planes de clase estructurados (objetivos, actividades, cierre y evaluación).
o	Preguntas de repaso y evaluaciones breves.
o	Dinámicas de aula adaptadas al nivel educativo.
2.	Recursos visuales (modelo texto–imagen – DALL·E):
o	Imágenes ilustrativas sobre hechos históricos, fenómenos científicos o recursos visuales educativos.
o	Estilo controlado (infografía, ilustración escolar, caricatura, etc.).
o	Enfoque educativo y didáctico (no estético-artístico solamente).
Ejemplo de prompts:
Texto–texto:
Eres un asistente educativo.
Genera un plan de clase de 40 minutos sobre la Revolución Francesa para secundaria.
Incluye: objetivos de aprendizaje, contenidos principales, una actividad de inicio, desarrollo, cierre y una breve evaluación de 3 preguntas.
Formato: Markdown con títulos claros.
Texto–imagen (DALL·E):

Educational illustration of the Storming of the Bastille, didactic and historical, style: school textbook, clear lines, neutral colors, no violence, suitable for classroom use.

Justificación de la viabilidad técnica
Disponibilidad tecnológica:
o	Modelos de IA de texto (ChatGPT u otro similar) y DALL·E para generación de imágenes están disponibles en línea.
o	Acceso mediante cuentas de usuario o APIs, sin necesidad de entrenar modelos propios.
Infraestructura mínima requerida:
o	PC personal + conexión a internet.
o	Entorno de desarrollo en Python (para automatizar generación y gestión de prompts).
o	No se requiere servidor propio, escalabilidad cubierta por los proveedores.
Limitaciones técnicas:
o	Dependencia de plataformas externas (cambios de políticas o costos pueden impactar).
o	Riesgo de resultados poco precisos → requiere ajuste iterativo de prompts.
o	DALL·E produce imágenes con costos por unidad → implica un esquema de consumo controlado.





Justificación de la viabilidad económica
Costos asociados:
•	Texto (ChatGPT o equivalente):
Costo por tokens: muy bajo (≈ $0.002–0.01 USD por plan de clase).
Un docente que genere 10 planes de clase al mes tendría un costo < $0.10 USD.
•	Imágenes (DALL·E):
Costo por imagen estándar (1024x1024) ≈ $0.04 USD.
Para 10 imágenes al mes = $0.40 USD/mes por usuario.
Escenario de uso:
Un docente que genere al mes:
•	10 planes de clase (texto)
•	10 imágenes (DALL·E)
Costo mensual estimado:
•	Texto: $0.05 – $0.10 USD
•	Imágenes: $0.40 USD
•	Total: ≈ $0.41 USD por docente/mes
Conclusión económica:
El costo por usuario es muy bajo y sostenible. Incluso con 100 usuarios activos, el costo mensual total sería de ≈ $41 USD, fácilmente cubierto con un modelo de suscripción ($3–5 USD/mes por usuario).

Evaluación final
•	Viabilidad técnica: Accesible con herramientas existentes y bajo requerimiento de infraestructura.
•	Viabilidad económica: Costos muy bajos en fase inicial, escalables con un modelo de suscripción.
•	Relevancia educativa: Permite ahorrar tiempo a los docentes y enriquecer la enseñanza con materiales personalizados.
•	Riesgos: dependencia de plataformas externas (políticas y precios).
En síntesis, el Asistente Inteligente de Planificación Educativa es un proyecto viable, sostenible y con alto impacto potencial en el ámbito docente.
Objetivos
1.	Generar planes de clase estructurados y claros (objetivos, actividades, materiales y evaluación).
2.	Producir ilustraciones educativas con DALL-E que complementen los contenidos generados en texto.
3.	Estandarizar el formato de los prompts para asegurar salidas consistentes y reutilizables.
4.	Reducir el tiempo de planificación docente en al menos un 50% en comparación con la preparación manual.
5.	Documentar un flujo de trabajo replicable (prompting + código en Python) que pueda ser ampliado a otros temas y niveles educativos.

Metodología
	El proyecto se llevará a cabo con un enfoque iterativo y controlado:
1.	Definición de casos de uso: se selecciona un tema inicial (ej. Revolución Francesa) y un nivel (primaria/secundaria).
2.	Diseño de prompts con técnica RICEF (Role, Input, Constraints, Examples, Format):
o	Para texto → estructura en Markdown con secciones fijas.
o	Para imágenes → estilo neutral, educativo, sin texto.
3.	Ejecución en Python mediante el script CLI:
o	Entrada del usuario → tema + conceptos para ilustración.
o	Generación del plan → generate_lesson_plan().
o	Generación de la imagen → generate_image().
4.	Validación:
o	En texto, se verifica que el Markdown incluya todas las secciones clave.
o	En imágenes, se revisa que el estilo sea claro y apto para uso escolar.
5.	Registro y refinamiento: los resultados se guardan en outputs/ (planes .md y .png), con logs en consola. Cada iteración se revisa y ajusta según resultados.
Justificación:
Este enfoque garantiza salidas consistentes, aprovecha el manejo de errores (reintentos exponenciales) y permite optimizar recursos (menos llamadas fallidas → menos costo).

Herramientas y Tecnologías
Lenguaje y entorno:
•	Python 3.13.x 
•	Uso de librerías:
o	openai → comunicación con modelos de texto e imagen.
o	dotenv → carga de credenciales desde .env.
o	requests y base64 → descarga y guardado de imágenes en disco.

Gestión de credenciales:
•	Archivo .env con la variable OPENAI_API_KEY, evitando exponer claves directamente en el código.
Modelos IA empleados:
•	Texto: gpt-4o para la generación de planes de clase detallados.
•	Imagen: gpt-image-1 (DALL·E 3) para ilustraciones educativas en formato PNG, con resolución configurable.
Técnica de prompting:
•	CRAFT (Context, Role, Action, Format, Tone):
o	Context: especifica el escenario educativo (tema, nivel, duración de clase).
o	Role: asigna a la IA el papel de asistente experto en planificación didáctica.
o	Action: indica la tarea concreta (crear plan de clase completo o ilustración educativa).
o	Format: define la estructura obligatoria de salida (Markdown para planes, PNG 1024x1024 para imágenes).
o	Tone: establece el estilo esperado (claro, inclusivo, neutral, didáctico).

Gestión de salidas:
•	Planes de clase en formato .md y .txt.
•	Ilustraciones generadas como archivos .png.
•	Carpeta outputs/ como directorio central de resultados.

Manejo de errores:
•	Reintentos automáticos con backoff exponencial en casos de límite de tasa o timeouts.
•	Validación de que el plan de clase contiene todas las secciones obligatorias antes de guardarlo.

Implementación
El proyecto se implementa con un script en Python que integra generación de texto e imágenes.
Flujo del programa
1.	El usuario ingresa el tema del plan de clase.
2.	El programa construye el prompt RICEF para el modelo de texto (gpt-4o) y genera un plan de clase en formato Markdown.
3.	El usuario ingresa conceptos clave para la imagen.
4.	El programa envía un prompt a DALL·E (gpt-image-1) y guarda la ilustración educativa en outputs/.

