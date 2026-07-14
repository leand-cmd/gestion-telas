import io


def producto_payload(sku="TEL-001"):
    return {
        "cod_sku": sku,
        "nro_producto": 1001,
        "descripcion": "Tela de algodon estampada",
        "clase": "Algodon",
        "categoria": "Tela",
        "origen": "Nacional",
        "metros": 50.5,
        "kilogramos": 12.3,
        "piezas": 10,
        "color": "Azul",
        "marca": "TelaSur",
        "precio": 25000,
        "costo": 15000,
        "stock_actual": 100,
        "stock_minimo": 10,
    }


def test_crud_producto(client, auth_headers):
    resp = client.post("/api/productos", json=producto_payload(), headers=auth_headers)
    assert resp.status_code == 201
    producto_id = resp.get_json()["id"]

    resp = client.get(f"/api/productos/{producto_id}", headers=auth_headers)
    assert resp.status_code == 200
    assert resp.get_json()["cod_sku"] == "TEL-001"

    resp = client.put(
        f"/api/productos/{producto_id}", json={"precio": 27000}, headers=auth_headers
    )
    assert resp.status_code == 200
    assert resp.get_json()["precio"] == 27000

    resp = client.delete(f"/api/productos/{producto_id}", headers=auth_headers)
    assert resp.status_code == 204


def test_duplicate_sku_rejected(client, auth_headers):
    client.post("/api/productos", json=producto_payload(), headers=auth_headers)
    resp = client.post("/api/productos", json=producto_payload(), headers=auth_headers)
    assert resp.status_code == 409


def test_search_productos(client, auth_headers):
    client.post("/api/productos", json=producto_payload(sku="TEL-100"), headers=auth_headers)
    client.post(
        "/api/productos",
        json=producto_payload(sku="TEL-200") | {"nro_producto": 1002, "color": "Rojo"},
        headers=auth_headers,
    )

    resp = client.get("/api/productos?q=Rojo", headers=auth_headers)
    data = resp.get_json()
    assert data["total"] == 1
    assert data["items"][0]["cod_sku"] == "TEL-200"


def test_import_productos_csv(client, auth_headers):
    csv_content = (
        "cod_sku,descripcion,clase,categoria,precio,stock_actual\n"
        "TEL-500,Lino natural,Lino,Tela,30000,20\n"
        "TEL-500,Duplicado,Lino,Tela,30000,20\n"
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
    assert report["cantidad_errores"] == 1
