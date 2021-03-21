import os

import pytest
from fastapi.testclient import TestClient

from opentunes_api.database.repository import get_tracks


@pytest.fixture(scope="session")
def api_client(settings, sqlite_file_uri):
    os.environ["DATABASE_URL"] = sqlite_file_uri
    from opentunes_api.api import fastapi_app
    yield TestClient(fastapi_app)


def test_config(api_client, sqlite_file_uri, tmpdir_factory):
    response = api_client.get("/info")
    result = response.json()

    assert response.status_code == 200, response.text
    assert sqlite_file_uri in result['database_url']
    assert str(tmpdir_factory.getbasetemp()) in result['music_root']


def test_tracks_api(track_db, api_client, db_session_tmpfile):

    tracks = get_tracks(session=db_session_tmpfile)
    assert len(tracks) == 1

    tracks = get_tracks(session=db_session_tmpfile)
    assert len(tracks) == 1

    # print("Starting test")
    print(api_client.get("/info").json())

    response = api_client.get("/api/tracks")
    assert response.status_code == 200
    print(response.json())
    # # # assert response.json() == {"msg": "Hello World"}
    # print(response.json())
