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


def test_cliente_sin_ruc_permitido(client, auth_headers):
    resp = client.post(
        "/api/clientes",
        json={"razon_social": "Cliente Sin Ruc"},
        headers=auth_headers,
    )
    assert resp.status_code == 201
    assert resp.get_json()["ruc"] is None


def test_multiples_clientes_sin_ruc_no_colisionan(client, auth_headers):
    resp1 = client.post(
        "/api/clientes", json={"razon_social": "Cliente A"}, headers=auth_headers
    )
    resp2 = client.post(
        "/api/clientes", json={"razon_social": "Cliente B"}, headers=auth_headers
    )
    assert resp1.status_code == 201
    assert resp2.status_code == 201


def test_ruc_vacio_se_normaliza_a_null(client, auth_headers):
    resp = client.post(
        "/api/clientes",
        json={"razon_social": "Cliente RUC vacio", "ruc": ""},
        headers=auth_headers,
    )
    assert resp.status_code == 201
    assert resp.get_json()["ruc"] is None


def test_actualizar_a_ruc_vacio_no_colisiona_entre_clientes(client, auth_headers):
    c1 = client.post(
        "/api/clientes", json={"razon_social": "Cliente A"}, headers=auth_headers
    ).get_json()
    c2 = client.post(
        "/api/clientes", json={"razon_social": "Cliente B"}, headers=auth_headers
    ).get_json()

    resp1 = client.put(f"/api/clientes/{c1['id']}", json={"ruc": ""}, headers=auth_headers)
    resp2 = client.put(f"/api/clientes/{c2['id']}", json={"ruc": ""}, headers=auth_headers)
    assert resp1.status_code == 200
    assert resp2.status_code == 200


def test_actualizar_a_ruc_duplicado_rechazado(client, auth_headers):
    c1 = client.post("/api/clientes", json=cliente_payload(ruc="80099999-9"), headers=auth_headers).get_json()
    c2 = client.post(
        "/api/clientes", json={"razon_social": "Cliente sin ruc"}, headers=auth_headers
    ).get_json()

    resp = client.put(
        f"/api/clientes/{c2['id']}", json={"ruc": "80099999-9"}, headers=auth_headers
    )
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
        "ruc,razon_social,direccion,localidad,canal,tipo_compra\n"
        "90011111-2,Hilados SA,Av. Espana 456,Encarnacion,Minorista,Credito\n"
        "90011111-2,Hilados SA duplicado,Av. Espana 456,Encarnacion,Minorista,Credito\n"
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


def test_codigo_cliente_autoasignado_correlativo(client, auth_headers):
    resp1 = client.post("/api/clientes", json=cliente_payload(ruc="80020001-1"), headers=auth_headers)
    resp2 = client.post("/api/clientes", json=cliente_payload(ruc="80020002-2"), headers=auth_headers)
    assert resp1.get_json()["codigo_cliente"] == "1"
    assert resp2.get_json()["codigo_cliente"] == "2"


def test_codigo_cliente_personalizado(client, auth_headers):
    payload = cliente_payload(ruc="80020003-3") | {"codigo_cliente": "ABC-001"}
    resp = client.post("/api/clientes", json=payload, headers=auth_headers)
    assert resp.status_code == 201
    assert resp.get_json()["codigo_cliente"] == "ABC-001"


def test_codigo_cliente_duplicado_rechazado(client, auth_headers):
    payload = cliente_payload(ruc="80020004-4") | {"codigo_cliente": "ABC-001"}
    client.post("/api/clientes", json=payload, headers=auth_headers)

    payload2 = cliente_payload(ruc="80020005-5") | {"codigo_cliente": "ABC-001"}
    resp = client.post("/api/clientes", json=payload2, headers=auth_headers)
    assert resp.status_code == 409


def test_sugerencia_next_id(client, auth_headers):
    resp = client.get("/api/clientes/next-id", headers=auth_headers)
    assert resp.status_code == 200
    assert resp.get_json()["next_id"] == "1"

    client.post("/api/clientes", json=cliente_payload(ruc="80020006-6"), headers=auth_headers)

    resp2 = client.get("/api/clientes/next-id", headers=auth_headers)
    assert resp2.get_json()["next_id"] == "2"


def test_unauthenticated_access_denied(client):
    resp = client.get("/api/clientes")
    assert resp.status_code == 401
