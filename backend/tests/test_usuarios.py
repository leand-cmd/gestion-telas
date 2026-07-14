import pytest


@pytest.fixture()
def admin_headers(client):
    client.post(
        "/api/auth/register",
        json={
            "email": "boss@test.com",
            "password": "secret123",
            "nombre": "Jefa",
            "rol": "Admin",
        },
    )
    resp = client.post("/api/auth/login", json={"email": "boss@test.com", "password": "secret123"})
    token = resp.get_json()["token"]
    return {"Authorization": f"Bearer {token}"}


def test_no_admin_no_puede_listar_usuarios(client, auth_headers):
    resp = client.get("/api/usuarios", headers=auth_headers)
    assert resp.status_code == 403


def test_admin_crea_y_desactiva_usuario(client, admin_headers):
    resp = client.post(
        "/api/usuarios",
        json={
            "email": "vendedor@test.com",
            "password": "secret123",
            "nombre": "Vendedor Uno",
            "rol": "Vendedor",
        },
        headers=admin_headers,
    )
    assert resp.status_code == 201
    usuario_id = resp.get_json()["id"]

    resp_lista = client.get("/api/usuarios", headers=admin_headers)
    assert resp_lista.get_json()["total"] == 2  # admin + vendedor

    resp_desactivar = client.patch(
        f"/api/usuarios/{usuario_id}/estado", json={"activo": False}, headers=admin_headers
    )
    assert resp_desactivar.status_code == 200
    assert resp_desactivar.get_json()["activo"] is False

    resp_login = client.post(
        "/api/auth/login", json={"email": "vendedor@test.com", "password": "secret123"}
    )
    assert resp_login.status_code == 403


def test_listar_asesores_accesible_a_cualquier_usuario(client, auth_headers):
    resp = client.get("/api/usuarios/asesores", headers=auth_headers)
    assert resp.status_code == 200
    assert len(resp.get_json()) == 1
