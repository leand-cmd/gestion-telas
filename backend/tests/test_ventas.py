def cliente_payload(ruc="80088888-1"):
    return {"ruc": ruc, "razon_social": "Cliente Ventas SA"}


def test_crear_venta_suelta(client, auth_headers):
    cliente_id = client.post(
        "/api/clientes", json=cliente_payload(), headers=auth_headers
    ).get_json()["id"]

    resp = client.post(
        "/api/ventas",
        json={"cliente_id": cliente_id, "total": 5000, "tipo_compra": "Contado"},
        headers=auth_headers,
    )
    assert resp.status_code == 201
    data = resp.get_json()
    assert data["nro_factura"] == "FAC-00001"
    assert data["estado_pago"] == "pendiente"


def test_cambiar_estado_pago(client, auth_headers):
    cliente_id = client.post(
        "/api/clientes", json=cliente_payload(), headers=auth_headers
    ).get_json()["id"]
    venta = client.post(
        "/api/ventas", json={"cliente_id": cliente_id, "total": 1000}, headers=auth_headers
    ).get_json()

    resp = client.patch(
        f"/api/ventas/{venta['id']}/estado-pago",
        json={"estado_pago": "pagado"},
        headers=auth_headers,
    )
    assert resp.status_code == 200
    assert resp.get_json()["estado_pago"] == "pagado"

    resp_invalido = client.patch(
        f"/api/ventas/{venta['id']}/estado-pago",
        json={"estado_pago": "invalido"},
        headers=auth_headers,
    )
    assert resp_invalido.status_code == 400


def test_pdf_venta(client, auth_headers):
    cliente_id = client.post(
        "/api/clientes", json=cliente_payload(), headers=auth_headers
    ).get_json()["id"]
    venta = client.post(
        "/api/ventas", json={"cliente_id": cliente_id, "total": 2500}, headers=auth_headers
    ).get_json()

    resp = client.get(f"/api/ventas/{venta['id']}/pdf", headers=auth_headers)
    assert resp.status_code == 200
    assert resp.mimetype == "application/pdf"
