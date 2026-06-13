# NetGuard GT - Gestión de Incidentes de Red

## Descripción del proyecto

Este proyecto consiste en un prototipo funcional de una API REST con interfaz web para la gestión de incidentes de red de la empresa NetGuard GT, un proveedor de telecomunicaciones que administra sitios de red, antenas, nodos y puntos de presencia.

El sistema permite registrar incidentes, asignarlos a técnicos especializados, controlar el avance de estados, validar reglas de negocio, guardar historial de cambios y generar reportes de cumplimiento.

## Tecnologías utilizadas

### Backend

* Python
* FastAPI
* SQLAlchemy
* SQLite
* Uvicorn
* Pytest

### Frontend

* React
* Vite
* Axios
* React Router DOM

### Base de datos

* SQLite

La base de datos utilizada es `netguard.db`, generada automáticamente por el backend.

---

# Historias de usuario

## HU-01 Registro de incidentes

Como operador de soporte de NetGuard GT, quiero registrar incidentes de red con sitio, tipo, severidad y descripción, para llevar un control ordenado de los problemas reportados.

Criterios de aceptación:

* El sistema debe permitir registrar el sitio afectado.
* El sistema debe permitir registrar el tipo de incidente.
* El sistema debe permitir registrar la severidad.
* Todo incidente nuevo debe iniciar en estado Registrado.
* El sistema debe guardar la fecha y hora de creación.

## HU-02 Registro de técnicos

Como administrador del sistema, quiero registrar técnicos con nombre y especialidad, para poder asignar incidentes a personal capacitado.

Criterios de aceptación:

* El sistema debe permitir registrar nombre del técnico.
* El sistema debe permitir registrar especialidad.
* Las especialidades disponibles son fibra óptica, microondas y sistemas eléctricos.
* El técnico queda disponible para futuras asignaciones.

## HU-03 Asignación de incidentes

Como coordinador de soporte, quiero asignar un incidente a un técnico disponible, para que el incidente pueda ser atendido correctamente.

Criterios de aceptación:

* Solo se puede asignar un incidente en estado Registrado.
* El incidente pasa al estado Asignado.
* El sistema guarda la fecha y hora de asignación.
* El cambio queda registrado en el historial.

## HU-04 Límite de incidentes activos por técnico

Como coordinador de soporte, quiero que un técnico no pueda tener más de 3 incidentes activos al mismo tiempo, para evitar sobrecarga de trabajo.

Criterios de aceptación:

* El sistema debe contar los incidentes activos del técnico.
* Se consideran activos los estados Asignado y En progreso.
* Si el técnico ya tiene 3 incidentes activos, el sistema debe impedir una nueva asignación.
* El sistema debe mostrar un mensaje indicando que el técnico alcanzó el límite permitido.

## HU-05 Validación por especialidad

Como coordinador de soporte, quiero asignar incidentes solo a técnicos con especialidad coincidente, para asegurar que el incidente sea atendido por personal capacitado.

Criterios de aceptación:

* El tipo de incidente debe coincidir con la especialidad del técnico.
* Si no coincide, el sistema rechaza la asignación.
* El sistema muestra un mensaje de error claro.
* La validación se realiza antes de guardar la asignación.

## HU-06 Cambio de estado del incidente

Como técnico asignado, quiero cambiar el estado de un incidente siguiendo el flujo correcto, para reflejar el avance real del trabajo.

Criterios de aceptación:

* Los estados deben avanzar en el orden: Registrado → Asignado → En progreso → Resuelto → Cerrado.
* No se permite retroceder de estado.
* No se permite saltar estados.
* Cada cambio se guarda en el historial.

## HU-07 Reasignación de incidentes

Como coordinador de soporte, quiero reasignar un incidente a otro técnico, para continuar la atención cuando el técnico anterior no pueda resolverlo.

Criterios de aceptación:

* El incidente puede reasignarse antes de cerrarse.
* El nuevo técnico debe tener especialidad coincidente.
* El nuevo técnico no debe superar 3 incidentes activos.
* El historial debe guardar el técnico anterior y el nuevo técnico.

## HU-08 Escalamiento automático

Como coordinador de soporte, quiero que los incidentes críticos o urgentes sean marcados como escalados si pasan más de 2 horas sin atención, para priorizar los casos más importantes.

Criterios de aceptación:

* Solo aplica para incidentes con severidad Crítico o Urgente.
* El incidente debe estar en estado Registrado.
* Si pasan más de 2 horas sin asignación, debe marcarse como escalado.
* El escalamiento queda registrado en el historial.

## HU-09 Historial de cambios

Como administrador del sistema, quiero consultar el historial de cambios de cada incidente, para conocer cómo avanzó su atención.

Criterios de aceptación:

* El sistema guarda cambios de estado.
* El sistema guarda asignaciones y reasignaciones.
* El sistema guarda fecha y hora de cada cambio.
* El historial se puede consultar por incidente.

## HU-10 Reportes de incidentes

Como gerente de operaciones, quiero generar reportes de incidentes por estado, severidad y técnico, para medir el cumplimiento del servicio.

Criterios de aceptación:

* El sistema muestra cantidad total de incidentes.
* El sistema muestra incidentes por estado.
* El sistema muestra incidentes por severidad.
* El sistema muestra incidentes asignados por técnico.
* El reporte se consulta desde un endpoint REST.

## HU-11 Consulta de incidentes

Como operador de soporte, quiero consultar la lista de incidentes registrados, para dar seguimiento a los casos pendientes.

Criterios de aceptación:

* El sistema lista todos los incidentes.
* El sistema muestra estado actual.
* El sistema muestra severidad.
* El sistema muestra técnico asignado si existe.
* El sistema muestra si el incidente está escalado.

---

# Estructura del proyecto

```text
0907-23-19496_ANALISISB2026FINAL/
│
├── Backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── database.py
│   │   ├── models.py
│   │   ├── schemas.py
│   │   ├── services.py
│   │   └── routers/
│   │       ├── tecnicos.py
│   │       ├── incidentes.py
│   │       └── reportes.py
│   │
│   ├── tests/
│   │   └── test_incidentes.py
│   │
│   ├── netguard.db
│   ├── pytest.ini
│   └── requirements.txt
│
└── Frontend/
    ├── src/
    │   ├── api/
    │   │   └── api.js
    │   ├── pages/
    │   │   ├── Dashboard.jsx
    │   │   ├── RegistrarTecnico.jsx
    │   │   ├── RegistrarIncidente.jsx
    │   │   ├── ListaIncidentes.jsx
    │   │   └── Reportes.jsx
    │   ├── App.jsx
    │   └── main.jsx
```

---

# Instalación del backend

Ingresar a la carpeta del backend:

```bash
cd Backend
```

Crear entorno virtual:

```bash
python -m venv .venv
```

Activar entorno virtual en Windows:

```bash
.venv\Scripts\activate
```

Instalar dependencias:

```bash
pip install -r requirements.txt
```

Ejecutar backend:

```bash
python -m uvicorn app.main:app --reload
```

Abrir Swagger:

```text
http://127.0.0.1:8000/docs
```

---

# Instalación del frontend

Ingresar a la carpeta del frontend:

```bash
cd Frontend
```

Instalar dependencias:

```bash
npm install
```

Ejecutar frontend:

```bash
npm run dev
```

Abrir en el navegador:

```text
http://localhost:5173/
```

---

# Pruebas unitarias

Para ejecutar las pruebas unitarias:

```bash
cd Backend
pytest
```

Las pruebas validan:

* Creación de técnicos.
* Creación de incidentes.
* Asignación correcta de incidentes.
* Validación de especialidad.
* Validación del flujo de estados.

---

# Endpoints principales

## Técnicos

```text
POST /api/tecnicos
GET /api/tecnicos
```

## Incidentes

```text
POST /api/incidentes
GET /api/incidentes
GET /api/incidentes/{id}
PUT /api/incidentes/{id}/asignar
PUT /api/incidentes/{id}/estado
PUT /api/incidentes/{id}/reasignar
GET /api/incidentes/{id}/historial
POST /api/incidentes/verificar-escalamientos
```

## Reportes

```text
GET /api/reportes/incidentes
```