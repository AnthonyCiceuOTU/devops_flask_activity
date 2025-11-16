import app


def test_hello():
    client = app.app.test_client()
    response = client.get("/hello")
    assert response.status_code == 200
    assert response.get_json() == {"message": "Hello, World!"}


def test_echo():
    client = app.app.test_client()
    payload = {"msg": "ping"}
    response = client.post("/echo", json=payload)
    assert response.status_code == 201
    assert response.get_json() == payload


def test_update_item_creates_or_updates():
    client = app.app.test_client()
    payload = {"name": "example item", "value": 42}
    response = client.put("/items/1", json=payload)
    assert response.status_code == 200
    data = response.get_json()
    assert data["id"] == 1
    assert data["data"] == payload

    # Update the same item id with different data
    updated_payload = {"name": "updated", "value": 100}
    response = client.put("/items/1", json=updated_payload)
    assert response.status_code == 200
    data = response.get_json()
    assert data["id"] == 1
    assert data["data"] == updated_payload


def test_delete_item_existing():
    client = app.app.test_client()
    payload = {"name": "to-delete"}
    # Ensure item exists first
    client.put("/items/99", json=payload)

    response = client.delete("/items/99")
    assert response.status_code == 200
    data = response.get_json()
    assert data["id"] == 99
    assert data["deleted"] == payload


def test_delete_item_missing():
    client = app.app.test_client()
    response = client.delete("/items/12345")
    assert response.status_code == 404
    data = response.get_json()
    assert "error" in data