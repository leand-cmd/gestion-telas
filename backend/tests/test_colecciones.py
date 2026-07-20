def coleccion_payload(nombre="Tejidos de Coleccion"):
    return {"nombre": nombre, "descripcion": "Tejidos destacados de la temporada"}


def test_crud_coleccion(client, auth_headers):
    resp = client.post("/api/colecciones", json=coleccion_payload(), headers=auth_headers)
    assert resp.status_code == 201
    coleccion_id = resp.get_json()["id"]
    assert resp.get_json()["nombre"] == "Tejidos de Coleccion"

    resp_lista = client.get("/api/colecciones", headers=auth_headers)
    assert resp_lista.status_code == 200
    assert resp_lista.get_json()["total"] == 1

    resp_put = client.put(
        f"/api/colecciones/{coleccion_id}",
        json={"imagen_url": "https://res.cloudinary.com/demo/image/upload/coleccion.png"},
        headers=auth_headers,
    )
    assert resp_put.status_code == 200
    assert resp_put.get_json()["imagen_url"] == "https://res.cloudinary.com/demo/image/upload/coleccion.png"

    resp_delete = client.delete(f"/api/colecciones/{coleccion_id}", headers=auth_headers)
    assert resp_delete.status_code == 204

    resp_lista2 = client.get("/api/colecciones", headers=auth_headers)
    assert resp_lista2.get_json()["total"] == 0


def test_nombre_duplicado_rechazado(client, auth_headers):
    client.post("/api/colecciones", json=coleccion_payload(), headers=auth_headers)
    resp = client.post("/api/colecciones", json=coleccion_payload(), headers=auth_headers)
    assert resp.status_code == 409


def test_nombre_requerido(client, auth_headers):
    resp = client.post("/api/colecciones", json={"descripcion": "sin nombre"}, headers=auth_headers)
    assert resp.status_code == 400
