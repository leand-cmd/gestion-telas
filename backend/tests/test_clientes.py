import io


def cliente_payload(ruc="80012345-6"):
    return {
        "ruc": ruc,
        "razon_social": "Textiles del Sur SA",
        "localidad": "Asuncion",
        "barrio": "Centro",
        "direccion": "Av. Mariscal Lopez 123",
        "telefono": "0981123456",
        "email": "contacto@textilesdelsur.com",
        "canal": "Mayorista",
        "sub_canal": "Grandes cuentas",
        "tipo_compra": "Contado",
        "latitude": -25.2637,
        "longitude": -57.5759,
    }


def test_crud_cliente(client, auth_headers):
    resp = client.post("/api/clientes", json=cliente_payload(), headers=auth_headers)
    assert resp.status_code == 201
    cliente_id = resp.get_json()["id"]

    resp = client.get(f"/api/clientes/{cliente_id}", headers=auth_headers)
    assert resp.status_code == 200
    assert resp.get_json()["razon_social"] == "Textiles del Sur SA"
    assert resp.get_json()["telefono"] == "0981123456"
    assert resp.get_json()["email"] == "contacto@textilesdelsur.com"

    resp = client.put(
        f"/api/clientes/{cliente_id}",
        json={"razon_social": "Textiles del Sur SRL"},
        headers=auth_headers,
    )
    assert resp.status_code == 200
    assert resp.get_json()["razon_social"] == "Textiles del Sur SRL"

    resp = client.delete(f"/api/clientes/{cliente_id}", headers=auth_headers)
    assert resp.status_code == 204

    resp = client.get(f"/api/clientes/{cliente_id}", headers=auth_headers)
    assert resp.status_code == 404


def test_duplicate_ruc_rejected(client, auth_headers):
    client.post("/api/clientes", json=cliente_payload(), headers=auth_headers)
    resp = client.post("/api/clientes", json=cliente_payload(), headers=auth_headers)
    assert resp.status_code == 409


def test_search_and_pagination(client, auth_headers):
    for i in range(3):
        client.post(
            "/api/clientes", json=cliente_payload(ruc=f"800000{i}-1"), headers=auth_headers
        )

    resp = client.get("/api/clientes?q=Textiles&per_page=2&page=1", headers=auth_headers)
    data = resp.get_json()
    assert resp.status_code == 200
    assert data["total"] == 3
    assert len(data["items"]) == 2


def test_import_clientes_csv(client, auth_headers):
    csv_content = (
        "ruc,razon_social,localidad,canal,tipo_compra\n"
        "90011111-2,Hilados SA,Encarnacion,Minorista,Credito\n"
        "90011111-2,Hilados SA duplicado,Encarnacion,Minorista,Credito\n"
    )
    data = {"file": (io.BytesIO(csv_content.encode()), "clientes.csv")}
    resp = client.post(
        "/api/clientes/import",
        data=data,
        headers=auth_headers,
        content_type="multipart/form-data",
    )
    assert resp.status_code == 200
    report = resp.get_json()
    assert report["insertados"] == 1
    assert report["cantidad_errores"] == 1


def test_email_invalido_rechazado(client, auth_headers):
    payload = cliente_payload() | {"email": "no-es-un-email"}
    resp = client.post("/api/clientes", json=payload, headers=auth_headers)
    assert resp.status_code == 400


def test_unauthenticated_access_denied(client):
    resp = client.get("/api/clientes")
    assert resp.status_code == 401
