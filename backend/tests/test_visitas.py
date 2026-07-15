def cliente_payload(ruc="80077777-1"):
    return {"ruc": ruc, "razon_social": "Cliente Visitas SA", "direccion": "Calle Falsa 123"}


def crear_cliente_y_asesor(client, auth_headers):
    cliente_id = client.post(
        "/api/clientes", json=cliente_payload(), headers=auth_headers
    ).get_json()["id"]
    asesor_id = client.get("/api/auth/me", headers=auth_headers).get_json()["id"]
    return cliente_id, asesor_id


def visita_payload(cliente_id, asesor_id):
    return {
        "cliente_id": cliente_id,
        "asesor_id": asesor_id,
        "fecha": "2026-08-01",
        "hora": "10:30",
        "proposito": "Consulta",
    }


def test_crear_y_registrar_resultado_visita(client, auth_headers):
    cliente_id, asesor_id = crear_cliente_y_asesor(client, auth_headers)

    resp = client.post(
        "/api/visitas", json=visita_payload(cliente_id, asesor_id), headers=auth_headers
    )
    assert resp.status_code == 201
    visita = resp.get_json()
    assert visita["estado"] == "programada"

    resp2 = client.patch(
        f"/api/visitas/{visita['id']}/resultado",
        json={"resultado": "Interesado", "notas_visita": "Buena reunion"},
        headers=auth_headers,
    )
    assert resp2.status_code == 200
    data = resp2.get_json()
    assert data["estado"] == "realizada"
    assert data["resultado"] == "Interesado"


def test_proposito_invalido_rechazado(client, auth_headers):
    cliente_id, asesor_id = crear_cliente_y_asesor(client, auth_headers)
    payload = visita_payload(cliente_id, asesor_id)
    payload["proposito"] = "Invalido"

    resp = client.post("/api/visitas", json=payload, headers=auth_headers)
    assert resp.status_code == 400


def test_filtro_por_rango_de_fechas(client, auth_headers):
    cliente_id, asesor_id = crear_cliente_y_asesor(client, auth_headers)
    client.post("/api/visitas", json=visita_payload(cliente_id, asesor_id), headers=auth_headers)

    resp = client.get(
        "/api/visitas?desde=2026-01-01&hasta=2026-12-31", headers=auth_headers
    )
    assert resp.get_json()["total"] == 1

    resp_vacio = client.get(
        "/api/visitas?desde=2020-01-01&hasta=2020-12-31", headers=auth_headers
    )
    assert resp_vacio.get_json()["total"] == 0


def test_filtro_por_cliente(client, auth_headers):
    cliente_id, asesor_id = crear_cliente_y_asesor(client, auth_headers)
    otro_cliente_id = client.post(
        "/api/clientes", json=cliente_payload(ruc="80077777-2"), headers=auth_headers
    ).get_json()["id"]
    client.post("/api/visitas", json=visita_payload(cliente_id, asesor_id), headers=auth_headers)
    client.post(
        "/api/visitas", json=visita_payload(otro_cliente_id, asesor_id), headers=auth_headers
    )

    resp = client.get(f"/api/visitas?cliente_id={cliente_id}", headers=auth_headers)
    data = resp.get_json()
    assert data["total"] == 1
    assert data["items"][0]["cliente_id"] == cliente_id


def test_cancelar_visita(client, auth_headers):
    cliente_id, asesor_id = crear_cliente_y_asesor(client, auth_headers)
    visita = client.post(
        "/api/visitas", json=visita_payload(cliente_id, asesor_id), headers=auth_headers
    ).get_json()

    resp = client.patch(f"/api/visitas/{visita['id']}/cancelar", headers=auth_headers)
    assert resp.status_code == 200
    assert resp.get_json()["estado"] == "cancelada"


def test_no_se_puede_cancelar_visita_realizada(client, auth_headers):
    cliente_id, asesor_id = crear_cliente_y_asesor(client, auth_headers)
    visita = client.post(
        "/api/visitas", json=visita_payload(cliente_id, asesor_id), headers=auth_headers
    ).get_json()
    client.patch(
        f"/api/visitas/{visita['id']}/resultado",
        json={"resultado": "Interesado"},
        headers=auth_headers,
    )

    resp = client.patch(f"/api/visitas/{visita['id']}/cancelar", headers=auth_headers)
    assert resp.status_code == 409
