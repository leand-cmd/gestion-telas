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
    ):
        assert campo in data

    assert len(data["ventas_por_mes"]) == 6
    assert data["pedidos_pendientes"] == 0
