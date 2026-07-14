import pytest

from app import create_app
from app.extensions import db as _db


@pytest.fixture()
def app():
    application = create_app("testing")
    with application.app_context():
        _db.create_all()
        yield application
        _db.session.remove()
        _db.drop_all()


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def auth_headers(client):
    client.post(
        "/api/auth/register",
        json={"email": "admin@test.com", "password": "secret123", "nombre": "Admin Test"},
    )
    resp = client.post(
        "/api/auth/login", json={"email": "admin@test.com", "password": "secret123"}
    )
    token = resp.get_json()["token"]
    return {"Authorization": f"Bearer {token}"}
