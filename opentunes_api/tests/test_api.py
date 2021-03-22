from fastapi.testclient import TestClient

from opentunes_api.main import fastapi_app

client = TestClient(fastapi_app)


def test_browse_api(db_track):
    response = client.get("/api/browse/")
    assert response.status_code == 200
    # assert response.json() == {"msg": "Hello World"}
