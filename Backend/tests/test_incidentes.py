from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_crear_tecnico():
    response = client.post(
        "/api/tecnicos",
        json={
            "nombre": "Técnico de Prueba",
            "especialidad": "fibra_optica"
        }
    )

    assert response.status_code == 200
    data = response.json()
    assert data["nombre"] == "Técnico de Prueba"
    assert data["especialidad"] == "fibra_optica"


def test_crear_incidente():
    response = client.post(
        "/api/incidentes",
        json={
            "sitio": "POP Jalapa",
            "tipo_incidente": "fibra_optica",
            "severidad": "critico",
            "descripcion": "Falla de fibra óptica."
        }
    )

    assert response.status_code == 200
    data = response.json()
    assert data["estado"] == "Registrado"
    assert data["escalado"] is False


def test_asignar_incidente_correctamente():
    tecnico = client.post(
        "/api/tecnicos",
        json={
            "nombre": "Técnico Fibra",
            "especialidad": "fibra_optica"
        }
    ).json()

    incidente = client.post(
        "/api/incidentes",
        json={
            "sitio": "Nodo Jalapa Norte",
            "tipo_incidente": "fibra_optica",
            "severidad": "alta",
            "descripcion": "Pérdida de señal en enlace de fibra."
        }
    ).json()

    response = client.put(
        f"/api/incidentes/{incidente['id']}/asignar",
        json={
            "tecnico_id": tecnico["id"]
        }
    )

    assert response.status_code == 200
    data = response.json()
    assert data["estado"] == "Asignado"
    assert data["tecnico_id"] == tecnico["id"]


def test_no_asignar_por_especialidad_incorrecta():
    tecnico = client.post(
        "/api/tecnicos",
        json={
            "nombre": "Técnico Microondas",
            "especialidad": "microondas"
        }
    ).json()

    incidente = client.post(
        "/api/incidentes",
        json={
            "sitio": "POP Jalapa Sur",
            "tipo_incidente": "fibra_optica",
            "severidad": "media",
            "descripcion": "Daño en cableado de fibra."
        }
    ).json()

    response = client.put(
        f"/api/incidentes/{incidente['id']}/asignar",
        json={
            "tecnico_id": tecnico["id"]
        }
    )

    assert response.status_code == 400
    assert "especialidad" in response.json()["detail"]


def test_no_saltar_estados():
    incidente = client.post(
        "/api/incidentes",
        json={
            "sitio": "POP Jalapa Este",
            "tipo_incidente": "sistemas_electricos",
            "severidad": "urgente",
            "descripcion": "Falla eléctrica en gabinete principal."
        }
    ).json()

    response = client.put(
        f"/api/incidentes/{incidente['id']}/estado",
        json={
            "nuevo_estado": "Resuelto"
        }
    )

    assert response.status_code == 400
    assert "estado" in response.json()["detail"]