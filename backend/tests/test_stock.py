def producto_payload(sku="TEL-STK-1"):
    return {"cod_sku": sku, "descripcion": "Tela stock test", "stock_actual": 10, "stock_minimo": 5}


def test_movimiento_entrada_y_salida(client, auth_headers):
    producto_id = client.post(
        "/api/productos", json=producto_payload(), headers=auth_headers
    ).get_json()["id"]

    resp = client.post(
        "/api/stock/movimientos",
        json={"producto_id": producto_id, "tipo": "entrada", "cantidad": 5, "motivo": "compra"},
        headers=auth_headers,
    )
    assert resp.status_code == 201

    producto = client.get(f"/api/productos/{producto_id}", headers=auth_headers).get_json()
    assert producto["stock_actual"] == 15

    client.post(
        "/api/stock/movimientos",
        json={"producto_id": producto_id, "tipo": "salida", "cantidad": 8, "motivo": "venta"},
        headers=auth_headers,
    )
    producto = client.get(f"/api/productos/{producto_id}", headers=auth_headers).get_json()
    assert producto["stock_actual"] == 7


def test_salida_no_puede_dejar_stock_negativo(client, auth_headers):
    producto_id = client.post(
        "/api/productos", json=producto_payload(sku="TEL-STK-2"), headers=auth_headers
    ).get_json()["id"]

    resp = client.post(
        "/api/stock/movimientos",
        json={"producto_id": producto_id, "tipo": "salida", "cantidad": 999},
        headers=auth_headers,
    )
    assert resp.status_code == 400


def test_listar_stock_bajo_minimo(client, auth_headers):
    client.post("/api/productos", json=producto_payload(sku="TEL-STK-3"), headers=auth_headers)

    resp = client.get("/api/stock?bajo_minimo=true", headers=auth_headers)
    assert resp.status_code == 200
    assert resp.get_json()["total"] == 0
