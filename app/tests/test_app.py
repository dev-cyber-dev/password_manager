from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_create_password():
    response = client.post(
        "/password/yandex", json={"password": "supersecret"})
    assert response.status_code == 200
    data = response.json()
    assert data["service_name"] == "yandex"
    assert data["password"] == "supersecret"


def test_get_password():
    client.post("/password/yandex", json={"password": "supersecret"})
    response = client.get("/password/yandex")
    assert response.status_code == 200
    data = response.json()
    assert data["service_name"] == "yandex"
    assert data["password"] == "supersecret"


def test_search_password():
    client.post("/password/yandex", json={"password": "supersecret"})
    client.post("/password/google", json={"password": "googlesupersecret"})
    response = client.get("/password/?service_name=yan")
    assert response.status_code == 200
    data = response.json()
    assert any(p["service_name"] == "yandex" for p in data)
    assert not any(p["service_name"] == "google" for p in data)


def test_get_password_not_found():
    response = client.get("/password/unknown_service")
    assert response.status_code == 404
    assert response.json() == {"detail": "Password not found"}
