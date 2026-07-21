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


def test_listar_colecciones_incluye_conteo_de_productos(client, auth_headers):
    coleccion_id = client.post(
        "/api/colecciones", json=coleccion_payload("TUL Frances"), headers=auth_headers
    ).get_json()["id"]

    def producto_payload(cod):
        return {
            "cod_producto": cod,
            "categoria": "Tejido plano",
            "coleccion_id": coleccion_id,
        }

    client.post("/api/productos", json=producto_payload("TUL-1"), headers=auth_headers)
    client.post("/api/productos", json=producto_payload("TUL-2"), headers=auth_headers)
    client.post(
        "/api/productos",
        json={"cod_producto": "SIN-1", "categoria": "Tejido plano"},
        headers=auth_headers,
    )

    resp = client.get("/api/colecciones", headers=auth_headers)
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["items"][0]["productos_count"] == 2
    assert data["sin_coleccion_count"] == 1

    resp_filtrado = client.get(
        f"/api/productos?coleccion_id={coleccion_id}", headers=auth_headers
    )
    assert resp_filtrado.get_json()["total"] == 2

    resp_sin = client.get("/api/productos?coleccion_id=none", headers=auth_headers)
    assert resp_sin.get_json()["total"] == 1
