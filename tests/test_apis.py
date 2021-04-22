from fastapi.testclient import TestClient

from app.db import get_engine, get_session
from app.main import app
from app.models import Base, Pokemon

client = TestClient(app)


def setup_module():
    Base.metadata.create_all(get_engine())


def teardown_module():
    Base.metadata.drop_all(get_engine())


def test_hello():
    response = client.get("/api")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}


def test_create_pokemon():
    assert get_session().query(Pokemon).filter_by(no="006").count() == 0

    response = client.post(
        "/api/pokemon/create",
        json={"no": "006", "name": "CHARIZARD", "types": ["FIRE", "FLYING"]},
    )
    data = response.json()
    data["types"].sort(key=lambda k: k["name"])
    assert response.status_code == 200
    assert data == {
        "id": "006",
        "no": "006",
        "name": "CHARIZARD",
        "types": [
            {"id": data["types"][0]["id"], "name": "FIRE"},
            {"id": data["types"][1]["id"], "name": "FLYING"},
        ],
        "evolutions": {"before": [], "after": []},
    }
    assert get_session().query(Pokemon).filter_by(no="006").count() == 1


def test_get_pokemon():
    response = client.get("/api/pokemon/006")
    assert response.status_code == 200

    data = response.json()
    data["types"].sort(key=lambda k: k["name"])
    assert data == {
        "id": "006",
        "no": "006",
        "name": "CHARIZARD",
        "types": [
            {"id": data["types"][0]["id"], "name": "FIRE"},
            {"id": data["types"][1]["id"], "name": "FLYING"},
        ],
        "evolutions": {"before": [], "after": []},
    }


def test_update_pokemon():
    response = client.patch(
        "/api/pokemon/006",
        json={"name": "CHARIZARD_2", "types": ["NONE"]},
    )
    data = response.json()
    assert response.status_code == 200
    assert data == {
        "id": "006",
        "no": "006",
        "name": "CHARIZARD_2",
        "types": [
            {"id": data["types"][0]["id"], "name": "NONE"},
        ],
        "evolutions": {"before": [], "after": []},
    }


def test_delete_pokemon():
    assert get_session().query(Pokemon).filter_by(no="006").count() == 1

    response = client.delete("/api/pokemon/006")
    data = response.json()
    assert response.status_code == 200
    assert data == {
        "id": "006",
        "no": "006",
        "name": "CHARIZARD_2",
        "types": [
            {"id": data["types"][0]["id"], "name": "NONE"},
        ],
        "evolutions": {"before": [], "after": []},
    }


def test_add_evolution():
    # create pokemon
    client.post(
        "/api/pokemon/create",
        json={"no": "004", "name": "CHARMANDER", "types": ["FIRE"]},
    )
    client.post(
        "/api/pokemon/create",
        json={"no": "005", "name": "CHARMELEON", "types": ["FIRE"]},
    )
    client.post(
        "/api/pokemon/create",
        json={"no": "006", "name": "CHARIZARD", "types": ["FIRE", "FLYING"]},
    )

    # add evolution
    response = client.post(
        "/api/pokemon/004/evolution", json={"evolutions_no": ["005"]}
    )
    data = response.json()
    assert response.status_code == 200
    assert data == {
        "id": "004",
        "no": "004",
        "name": "CHARMANDER",
        "types": [{"id": data["types"][0]["id"], "name": "FIRE"}],
        "evolutions": {
            "before": [],
            "after": [{"id": "005", "no": "005", "name": "CHARMELEON"}],
        },
    }

    response = client.post(
        "/api/pokemon/005/evolution", json={"evolutions_no": ["006"]}
    )
    data = response.json()
    assert response.status_code == 200
    assert data == {
        "id": "005",
        "no": "005",
        "name": "CHARMELEON",
        "types": [{"id": data["types"][0]["id"], "name": "FIRE"}],
        "evolutions": {
            "before": [{"id": "004", "no": "004", "name": "CHARMANDER"}],
            "after": [{"id": "006", "no": "006", "name": "CHARIZARD"}],
        },
    }
