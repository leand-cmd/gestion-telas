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


def test_crear_visita_sin_hora_permitido(client, auth_headers):
    cliente_id, asesor_id = crear_cliente_y_asesor(client, auth_headers)
    resp = client.post(
        "/api/visitas",
        json={"cliente_id": cliente_id, "asesor_id": asesor_id, "fecha": "2026-08-01"},
        headers=auth_headers,
    )
    assert resp.status_code == 201
    assert resp.get_json()["hora"] is None


def test_eliminar_visita(client, auth_headers):
    cliente_id, asesor_id = crear_cliente_y_asesor(client, auth_headers)
    visita = client.post(
        "/api/visitas", json=visita_payload(cliente_id, asesor_id), headers=auth_headers
    ).get_json()

    resp = client.delete(f"/api/visitas/{visita['id']}", headers=auth_headers)
    assert resp.status_code == 204

    resp2 = client.get(f"/api/visitas/{visita['id']}", headers=auth_headers)
    assert resp2.status_code == 404


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
        json={
            "resultado": "Interesado",
            "notas_visita": "Buena reunion",
            "tipo_gestion": "Venta Exitosa",
        },
        headers=auth_headers,
    )
    assert resp2.status_code == 200
    data = resp2.get_json()
    assert data["estado"] == "realizada"
    assert data["resultado"] == "Interesado"
    assert data["tipo_gestion"] == "Venta Exitosa"


def test_registrar_solo_tipo_gestion_sin_otros_campos(client, auth_headers):
    cliente_id, asesor_id = crear_cliente_y_asesor(client, auth_headers)
    visita = client.post(
        "/api/visitas", json=visita_payload(cliente_id, asesor_id), headers=auth_headers
    ).get_json()

    resp = client.patch(
        f"/api/visitas/{visita['id']}/resultado",
        json={"tipo_gestion": "Sin Contacto"},
        headers=auth_headers,
    )
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["estado"] == "realizada"
    assert data["tipo_gestion"] == "Sin Contacto"
    assert data["resultado"] is None
    assert data["notas_visita"] is None


def test_reeditar_tipo_gestion_no_pisa_notas_previas(client, auth_headers):
    cliente_id, asesor_id = crear_cliente_y_asesor(client, auth_headers)
    visita = client.post(
        "/api/visitas", json=visita_payload(cliente_id, asesor_id), headers=auth_headers
    ).get_json()

    client.patch(
        f"/api/visitas/{visita['id']}/resultado",
        json={"tipo_gestion": "Sin Contacto", "notas_visita": "Primer intento"},
        headers=auth_headers,
    )
    resp = client.patch(
        f"/api/visitas/{visita['id']}/resultado",
        json={"tipo_gestion": "Venta Exitosa"},
        headers=auth_headers,
    )
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["tipo_gestion"] == "Venta Exitosa"
    assert data["notas_visita"] == "Primer intento"


def test_filtro_por_tipo_gestion(client, auth_headers):
    cliente_id, asesor_id = crear_cliente_y_asesor(client, auth_headers)
    v1 = client.post(
        "/api/visitas", json=visita_payload(cliente_id, asesor_id), headers=auth_headers
    ).get_json()
    v2 = client.post(
        "/api/visitas",
        json=visita_payload(cliente_id, asesor_id) | {"fecha": "2026-08-02"},
        headers=auth_headers,
    ).get_json()
    client.patch(
        f"/api/visitas/{v1['id']}/resultado",
        json={"resultado": "Interesado", "tipo_gestion": "Venta Exitosa"},
        headers=auth_headers,
    )
    client.patch(
        f"/api/visitas/{v2['id']}/resultado",
        json={"resultado": "Requiere seguimiento", "tipo_gestion": "Visita de Seguimiento"},
        headers=auth_headers,
    )

    resp = client.get("/api/visitas?tipo_gestion=Venta Exitosa", headers=auth_headers)
    data = resp.get_json()
    assert data["total"] == 1
    assert data["items"][0]["id"] == v1["id"]


def test_tipo_gestion_invalido_rechazado(client, auth_headers):
    cliente_id, asesor_id = crear_cliente_y_asesor(client, auth_headers)
    visita = client.post(
        "/api/visitas", json=visita_payload(cliente_id, asesor_id), headers=auth_headers
    ).get_json()

    resp = client.patch(
        f"/api/visitas/{visita['id']}/resultado",
        json={"resultado": "Interesado", "tipo_gestion": "Invalido"},
        headers=auth_headers,
    )
    assert resp.status_code == 400


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
