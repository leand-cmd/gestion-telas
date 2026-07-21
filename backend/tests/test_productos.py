import io


def producto_payload(cod="TEL-001"):
    return {
        "cod_producto": cod,
        "proveedor": "KARRETEL",
        "marca": "KARRETEL",
        "cod_color": "AZ01",
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
        "descripcion": "Boston",
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
        json=producto_payload(cod="TEL-200") | {"color_general": "Verde"},
        headers=auth_headers,
    )

    resp = client.get("/api/productos?q=TEL-200", headers=auth_headers)
    data = resp.get_json()
    assert data["total"] == 1
    assert data["items"][0]["cod_producto"] == "TEL-200"


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


def test_listar_colecciones_con_productos(client, auth_headers):
    coleccion_id = client.post(
        "/api/colecciones", json={"nombre": "TUL Frances"}, headers=auth_headers
    ).get_json()["id"]

    client.post(
        "/api/productos",
        json=producto_payload(cod="TEL-400") | {"coleccion_id": coleccion_id},
        headers=auth_headers,
    )
    client.post("/api/productos", json=producto_payload(cod="TEL-401"), headers=auth_headers)

    resp = client.get("/api/productos/colecciones", headers=auth_headers)
    assert resp.status_code == 200
    data = resp.get_json()

    grupo_coleccion = next(g for g in data if g["id"] == coleccion_id)
    assert [p["cod_producto"] for p in grupo_coleccion["productos"]] == ["TEL-400"]

    grupo_sin_coleccion = next(g for g in data if g["id"] is None)
    assert grupo_sin_coleccion["nombre"] == "Sin colección"
    assert [p["cod_producto"] for p in grupo_sin_coleccion["productos"]] == ["TEL-401"]


def test_eliminar_imagen_producto(client, auth_headers):
    producto_id = client.post(
        "/api/productos", json=producto_payload(cod="TEL-700"), headers=auth_headers
    ).get_json()["id"]

    client.put(
        f"/api/productos/{producto_id}",
        json={"imagen_url": "https://res.cloudinary.com/demo/image/upload/producto.png"},
        headers=auth_headers,
    )

    resp = client.delete(f"/api/productos/{producto_id}/image", headers=auth_headers)
    assert resp.status_code == 200
    assert resp.get_json()["imagen_url"] is None


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


def test_import_crea_coleccion_automaticamente_por_coleccion(client, auth_headers):
    csv_content = (
        "cod_producto,coleccion,categoria,stock_rollos\n"
        "TEL-600,Tull Frances,Tejido plano,10\n"
        "TEL-601,Tull Frances,Tejido plano,5\n"
        "TEL-602,Boston,Tejido plano,3\n"
    )
    data = {"file": (io.BytesIO(csv_content.encode()), "productos.csv")}
    resp = client.post(
        "/api/productos/import",
        data=data,
        headers=auth_headers,
        content_type="multipart/form-data",
    )
    assert resp.status_code == 200
    assert resp.get_json()["insertados"] == 3

    colecciones = client.get("/api/colecciones", headers=auth_headers).get_json()
    nombres = {c["nombre"]: c["productos_count"] for c in colecciones["items"]}
    assert nombres["Tull Frances"] == 2
    assert nombres["Boston"] == 1

    # Reimportar con la misma coleccion no debe duplicarla
    resp2 = client.post(
        "/api/productos/import",
        data={"file": (io.BytesIO(csv_content.encode()), "productos.csv")},
        headers=auth_headers,
        content_type="multipart/form-data",
    )
    assert resp2.get_json()["actualizados"] == 3
    colecciones2 = client.get("/api/colecciones", headers=auth_headers).get_json()
    assert colecciones2["total"] == 2
