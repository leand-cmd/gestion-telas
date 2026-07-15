def cliente_payload(ruc="80099999-1"):
    return {"ruc": ruc, "razon_social": "Cliente Pedidos SA", "direccion": "Calle Falsa 123"}


def producto_payload(sku="TEL-PED-1"):
    return {"cod_sku": sku, "descripcion": "Tela test", "precio": 1000, "stock_actual": 50}


def crear_cliente_y_producto(client, auth_headers):
    cliente_id = client.post(
        "/api/clientes", json=cliente_payload(), headers=auth_headers
    ).get_json()["id"]
    producto_id = client.post(
        "/api/productos", json=producto_payload(), headers=auth_headers
    ).get_json()["id"]
    return cliente_id, producto_id


def pedido_payload(cliente_id, producto_id):
    return {
        "cliente_id": cliente_id,
        "tipo_compra": "Contado",
        "detalles": [{"producto_id": producto_id, "cantidad": 3}],
    }


def test_crear_pedido_calcula_total_y_numeracion(client, auth_headers):
    cliente_id, producto_id = crear_cliente_y_producto(client, auth_headers)

    resp = client.post(
        "/api/pedidos", json=pedido_payload(cliente_id, producto_id), headers=auth_headers
    )
    assert resp.status_code == 201
    data = resp.get_json()
    assert data["nro_pedido"] == "PED-00001"
    assert data["total"] == 3000
    assert data["estado"] == "Pendiente"

    resp2 = client.post(
        "/api/pedidos", json=pedido_payload(cliente_id, producto_id), headers=auth_headers
    )
    assert resp2.get_json()["nro_pedido"] == "PED-00002"


def test_no_se_puede_editar_pedido_confirmado(client, auth_headers):
    cliente_id, producto_id = crear_cliente_y_producto(client, auth_headers)
    pedido = client.post(
        "/api/pedidos", json=pedido_payload(cliente_id, producto_id), headers=auth_headers
    ).get_json()

    client.patch(
        f"/api/pedidos/{pedido['id']}/estado",
        json={"estado": "Confirmado"},
        headers=auth_headers,
    )

    resp = client.put(
        f"/api/pedidos/{pedido['id']}",
        json={"observaciones": "cambio"},
        headers=auth_headers,
    )
    assert resp.status_code == 409


def test_transicion_estado_invalida_rechazada(client, auth_headers):
    cliente_id, producto_id = crear_cliente_y_producto(client, auth_headers)
    pedido = client.post(
        "/api/pedidos", json=pedido_payload(cliente_id, producto_id), headers=auth_headers
    ).get_json()

    resp = client.patch(
        f"/api/pedidos/{pedido['id']}/estado",
        json={"estado": "Entregado"},
        headers=auth_headers,
    )
    assert resp.status_code == 400


def test_convertir_a_venta(client, auth_headers):
    cliente_id, producto_id = crear_cliente_y_producto(client, auth_headers)
    pedido = client.post(
        "/api/pedidos", json=pedido_payload(cliente_id, producto_id), headers=auth_headers
    ).get_json()

    client.patch(
        f"/api/pedidos/{pedido['id']}/estado",
        json={"estado": "Confirmado"},
        headers=auth_headers,
    )

    resp = client.post(
        f"/api/pedidos/{pedido['id']}/convertir-a-venta", headers=auth_headers
    )
    assert resp.status_code == 201
    venta = resp.get_json()
    assert venta["nro_factura"] == "FAC-00001"
    assert venta["total"] == 3000

    pedido_actualizado = client.get(
        f"/api/pedidos/{pedido['id']}", headers=auth_headers
    ).get_json()
    assert pedido_actualizado["estado"] == "Facturado"

    resp2 = client.post(
        f"/api/pedidos/{pedido['id']}/convertir-a-venta", headers=auth_headers
    )
    assert resp2.status_code == 409
