def producto_payload(sku="TEL-STK-1"):
    return {
        "cod_producto": sku,
        "categoria": "Tejido plano",
        "stock_rollos": 10,
    }


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
    assert producto["stock_rollos"] == 15

    client.post(
        "/api/stock/movimientos",
        json={"producto_id": producto_id, "tipo": "salida", "cantidad": 8, "motivo": "venta"},
        headers=auth_headers,
    )
    producto = client.get(f"/api/productos/{producto_id}", headers=auth_headers).get_json()
    assert producto["stock_rollos"] == 7


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


def test_listar_stock_busca_por_cod_producto(client, auth_headers):
    client.post("/api/productos", json=producto_payload(sku="TEL-STK-3"), headers=auth_headers)

    resp = client.get("/api/stock?q=TEL-STK-3", headers=auth_headers)
    assert resp.status_code == 200
    assert resp.get_json()["total"] == 1
