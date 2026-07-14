def test_register_and_login(client):
    resp = client.post(
        "/api/auth/register",
        json={"email": "user1@test.com", "password": "secret123", "nombre": "Usuario Uno"},
    )
    assert resp.status_code == 201
    assert resp.get_json()["usuario"]["rol"] == "Vendedor"

    resp = client.post(
        "/api/auth/login", json={"email": "user1@test.com", "password": "secret123"}
    )
    assert resp.status_code == 200
    assert "token" in resp.get_json()


def test_register_duplicate_email(client):
    payload = {"email": "dup@test.com", "password": "secret123", "nombre": "Dup"}
    client.post("/api/auth/register", json=payload)
    resp = client.post("/api/auth/register", json=payload)
    assert resp.status_code == 409


def test_login_wrong_password(client):
    client.post(
        "/api/auth/register",
        json={"email": "user2@test.com", "password": "secret123", "nombre": "Usuario Dos"},
    )
    resp = client.post(
        "/api/auth/login", json={"email": "user2@test.com", "password": "wrongpass"}
    )
    assert resp.status_code == 401


def test_me_requires_token(client):
    resp = client.get("/api/auth/me")
    assert resp.status_code == 401
