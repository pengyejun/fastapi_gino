import uuid


def test_crud(client):
    nickname = str(uuid.uuid4())
    r = client.post("/users", json=dict(name=nickname))
    r.raise_for_status()

    url = f"/users/{r.json()['id']}"
    assert client.get(url).json()["nickname"] == nickname

    client.delete(url).raise_for_status()

    assert client.get(url).status_code == 404
