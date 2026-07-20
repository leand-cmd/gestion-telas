import io


def producto_payload(cod="TEL-001"):
    return {
        "cod_producto": cod,
        "proveedor": "KARRETEL",
        "marca": "KARRETEL",
        "coleccion": "Tejidos de Coleccion",
        "cod_color": "AZ01",
        "nombre_tejido": "Boston",
        "color_general": "Azul",
        "color_descripcion": "Azul marino",
        "categoria": "Tejido plano",
        "sub_categoria": "Estampado",
        "tipo_diseno": "Liso",
        "composicion": "100% Algodon",
        "linea_sugerida": "Vestir",
        "ancho_cm": 150.0,
        "gramaje_gm2": 180.0,
        "precio_rollo": 13900,
        "precio_media_rollo": None,
        "precio_corte": 16680,
        "stock_rollos": 100,
        "fecha_creacion": "2026-07-17",
        "notas": None,
    }


def test_crud_producto(client, auth_headers):
    resp = client.post("/api/productos", json=producto_payload(), headers=auth_headers)
    assert resp.status_code == 201
    producto_id = resp.get_json()["id"]

    resp = client.get(f"/api/productos/{producto_id}", headers=auth_headers)
    assert resp.status_code == 200
    assert resp.get_json()["cod_producto"] == "TEL-001"

    resp = client.put(
        f"/api/productos/{producto_id}", json={"precio_rollo": 15000}, headers=auth_headers
    )
    assert resp.status_code == 200
    assert resp.get_json()["precio_rollo"] == 15000

    resp = client.delete(f"/api/productos/{producto_id}", headers=auth_headers)
    assert resp.status_code == 204


def test_duplicate_sku_rejected(client, auth_headers):
    client.post("/api/productos", json=producto_payload(), headers=auth_headers)
    resp = client.post("/api/productos", json=producto_payload(), headers=auth_headers)
    assert resp.status_code == 409


def test_search_productos(client, auth_headers):
    client.post("/api/productos", json=producto_payload(cod="TEL-100"), headers=auth_headers)
    client.post(
        "/api/productos",
        json=producto_payload(cod="TEL-200") | {"nombre_tejido": "Marrakesh Print"},
        headers=auth_headers,
    )

    resp = client.get("/api/productos?q=Marrakesh", headers=auth_headers)
    data = resp.get_json()
    assert data["total"] == 1
    assert data["items"][0]["cod_producto"] == "TEL-200"


def test_listar_tejidos_agrupa_por_nombre_tejido(client, auth_headers):
    client.post("/api/productos", json=producto_payload(cod="TEL-400"), headers=auth_headers)
    client.post(
        "/api/productos",
        json=producto_payload(cod="TEL-401") | {"nombre_tejido": "Boston"},
        headers=auth_headers,
    )
    client.post(
        "/api/productos",
        json=producto_payload(cod="TEL-402") | {"nombre_tejido": "Tull Frances"},
        headers=auth_headers,
    )

    resp = client.get("/api/productos/tejidos", headers=auth_headers)
    assert resp.status_code == 200
    tejidos = {t["nombre_tejido"]: t["count"] for t in resp.get_json()}
    assert tejidos["Boston"] == 2
    assert tejidos["Tull Frances"] == 1

    resp_filtro = client.get("/api/productos?nombre_tejido=Tull Frances", headers=auth_headers)
    data = resp_filtro.get_json()
    assert data["total"] == 1
    assert data["items"][0]["cod_producto"] == "TEL-402"


def test_asignar_coleccion_a_producto(client, auth_headers):
    coleccion_id = client.post(
        "/api/colecciones", json={"nombre": "TUL Frances"}, headers=auth_headers
    ).get_json()["id"]

    resp = client.post(
        "/api/productos",
        json=producto_payload(cod="TEL-300") | {"coleccion_id": coleccion_id},
        headers=auth_headers,
    )
    assert resp.status_code == 201
    assert resp.get_json()["coleccion_id"] == coleccion_id

    resp_inexistente = client.post(
        "/api/productos",
        json=producto_payload(cod="TEL-301") | {"coleccion_id": 9999},
        headers=auth_headers,
    )
    assert resp_inexistente.status_code == 400


def test_import_productos_csv_mapea_precios_karretel(client, auth_headers):
    csv_content = (
        "cod_producto,nombre_tejido,categoria,stock_rollos\n"
        "TEL-500,Rayon Challis,Tejido plano,20\n"
        "TEL-500,Rayon Challis,Tejido plano,20\n"
    )
    data = {"file": (io.BytesIO(csv_content.encode()), "productos.csv")}
    resp = client.post(
        "/api/productos/import",
        data=data,
        headers=auth_headers,
        content_type="multipart/form-data",
    )
    assert resp.status_code == 200
    report = resp.get_json()
    assert report["insertados"] == 1
    assert report["actualizados"] == 1
    assert report["cantidad_errores"] == 0

    productos = client.get("/api/productos?q=TEL-500", headers=auth_headers).get_json()["items"]
    assert productos[0]["precio_rollo"] == 11300
    assert productos[0]["precio_corte"] == 13560
