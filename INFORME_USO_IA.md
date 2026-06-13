# Informe de utilización de IA

## Proyecto

NetGuard GT - Sistema de gestión de incidentes de red

## Objetivo del uso de IA

La inteligencia artificial fue utilizada como apoyo para analizar el enunciado del examen, organizar los requerimientos, definir historias de usuario, estructurar el backend, crear una interfaz sencilla, proponer pruebas unitarias y corregir errores durante la ejecución del proyecto.

El desarrollo fue revisado y probado paso a paso para validar que cumpliera con las reglas de negocio solicitadas.

---

# Prompts enviados

## Prompt 1

Necesito que analices este examen parcial y me ayudes paso a paso a realizar el proyecto usando Python. Necesito historias de usuario, backend, frontend, pruebas y explicación de carpetas.

## Resultado obtenido

Se identificó que el sistema debía gestionar incidentes de red para NetGuard GT. Se organizaron las funcionalidades principales: registro de técnicos, registro de incidentes, asignación, cambio de estados, historial, reportes y validaciones de reglas de negocio.

---

## Prompt 2

Necesito que las historias de usuario me las des escritas para pegarlas en el README.

## Resultado obtenido

Se generaron historias de usuario con formato: Como, quiero, para. Además, se agregaron criterios de aceptación medibles para cada historia.

---

## Prompt 3

Ayúdame a crear el backend con Python, FastAPI y SQLite, indicando qué archivos crear y qué código colocar.

## Resultado obtenido

Se generó la estructura del backend con carpetas y archivos. Se implementaron modelos, esquemas, servicios, routers y conexión a SQLite.

---

## Prompt 4

Me da error al ejecutar uvicorn y luego pytest. Ayúdame a corregirlo.

## Resultado obtenido

Se corrigieron errores relacionados con archivos incompletos y configuración de rutas para pruebas. Se agregó el archivo `pytest.ini` para que pytest reconociera correctamente la carpeta `app`.

---

## Prompt 5

Ayúdame a probar los endpoints en Swagger paso a paso.

## Resultado obtenido

Se probaron los endpoints principales:

* POST /api/tecnicos
* POST /api/incidentes
* PUT /api/incidentes/{id}/asignar
* PUT /api/incidentes/{id}/estado
* GET /api/incidentes/{id}/historial
* GET /api/reportes/incidentes

---

## Prompt 6

Ayúdame a crear el frontend en React para consumir la API.

## Resultado obtenido

Se creó una interfaz web sencilla con React y Vite. La interfaz incluye dashboard, registro de técnicos, registro de incidentes, lista de incidentes, historial y reportes.

---

# Correcciones realizadas

Durante el desarrollo se realizaron las siguientes correcciones:

1. Se corrigió el error donde el router de técnicos no estaba siendo reconocido por FastAPI.
2. Se agregó configuración `pytest.ini` para que las pruebas pudieran importar correctamente el módulo `app`.
3. Se verificó que la base de datos SQLite se estuviera creando automáticamente.
4. Se eliminó una carpeta `src` que fue creada por error dentro del backend.
5. Se confirmó que el frontend estuviera en la carpeta correcta.
6. Se validó la comunicación entre frontend y backend.
7. Se reinició el backend cuando Swagger mostró error de conexión.

---

# Reflexión sobre el uso de IA

El uso de IA fue útil para organizar el desarrollo del proyecto y reducir errores de estructura. La herramienta permitió interpretar el enunciado del examen y convertirlo en historias de usuario, reglas de negocio y componentes técnicos.

Sin embargo, no se utilizó la respuesta de IA sin revisión. Cada parte fue probada manualmente en el entorno local, especialmente los endpoints de la API, las pruebas unitarias y la conexión con el frontend.

La IA también ayudó a depurar errores, pero las decisiones finales fueron verificadas mediante ejecución del código y pruebas funcionales.

---

# Aprendizaje obtenido

Durante el desarrollo del proyecto se reforzaron conocimientos sobre:

* Creación de APIs REST.
* Uso de FastAPI.
* Manejo de SQLite.
* Validación de reglas de negocio.
* Pruebas unitarias con pytest.
* Integración de backend con frontend.
* Consumo de APIs desde React.
* Organización de carpetas en un proyecto web.

---

# Conclusión

La IA fue utilizada como herramienta de apoyo para guiar el desarrollo, documentar el proceso y corregir errores. El proyecto fue probado de forma local y se verificó que cumple con las reglas solicitadas en el examen.
