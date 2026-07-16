from datetime import date


def test_resumen_dashboard_estructura(client, auth_headers):
    resp = client.get("/api/dashboard/resumen", headers=auth_headers)
    assert resp.status_code == 200
    data = resp.get_json()
    for campo in (
        "ventas_mes_actual",
        "ventas_por_mes",
        "pedidos_pendientes",
        "stock_bajo",
        "proximas_visitas",
        "top_clientes",
        "top_productos",
        "total_clientes_cartera",
        "clientes_visitados_mes",
        "cobertura_porcentaje",
        "gestiones_por_tipo",
        "efectividad_gestiones_porcentaje",
    ):
        assert campo in data

    assert len(data["ventas_por_mes"]) == 6
    assert data["pedidos_pendientes"] == 0


def test_cobertura_y_gestiones(client, auth_headers):
    asesor_id = client.get("/api/auth/me", headers=auth_headers).get_json()["id"]
    hoy = date.today().isoformat()

    cliente1 = client.post(
        "/api/clientes", json={"ruc": "80030001-1", "razon_social": "Cliente Uno"}, headers=auth_headers
    ).get_json()
    cliente2 = client.post(
        "/api/clientes", json={"ruc": "80030002-2", "razon_social": "Cliente Dos"}, headers=auth_headers
    ).get_json()

    visita1 = client.post(
        "/api/visitas",
        json={
            "cliente_id": cliente1["id"],
            "asesor_id": asesor_id,
            "fecha": hoy,
            "hora": "09:00",
        },
        headers=auth_headers,
    ).get_json()
    client.patch(
        f"/api/visitas/{visita1['id']}/resultado",
        json={"resultado": "Interesado", "tipo_gestion": "Venta Exitosa"},
        headers=auth_headers,
    )

    visita2 = client.post(
        "/api/visitas",
        json={
            "cliente_id": cliente2["id"],
            "asesor_id": asesor_id,
            "fecha": hoy,
            "hora": "10:00",
        },
        headers=auth_headers,
    ).get_json()
    client.patch(
        f"/api/visitas/{visita2['id']}/resultado",
        json={"resultado": "Requiere seguimiento", "tipo_gestion": "Visita de Seguimiento"},
        headers=auth_headers,
    )

    resp = client.get("/api/dashboard/resumen", headers=auth_headers)
    data = resp.get_json()

    assert data["total_clientes_cartera"] == 2
    assert data["clientes_visitados_mes"] == 2
    assert data["cobertura_porcentaje"] == 100.0
    assert {"tipo": "Venta Exitosa", "cantidad": 1} in data["gestiones_por_tipo"]
    assert {"tipo": "Visita de Seguimiento", "cantidad": 1} in data["gestiones_por_tipo"]
    assert data["efectividad_gestiones_porcentaje"] == 50.0
