import os

import pytest
from fastapi.testclient import TestClient

from opentunes_api.database import get_db
from opentunes_api.database.repository import get_tracks, add_track
from opentunes_api.schemas import TrackSchema


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


def override_get_db(db_session_tmpfile):
    yield db_session_tmpfile


def test_tracks_api(api_client, track_db, sqlite_file_uri, db_session_tmpfile):
    # os.environ["DATABASE_URL"] = sqlite_file_uri
    from opentunes_api.api import fastapi_app
    fastapi_app.dependency_overrides[get_db] = db_session_tmpfile
    api_client = TestClient(fastapi_app)

    # print(get_tracks(session=db_session_tmpfile))
    # from ipdb import set_trace; set_trace()
    # assert len(get_tracks(session=db_session_tmpfile)) == 1

    # print("Starting test")
    # print(api_client.get("/info").json())

    response = api_client.get("/api/tracks")
    # assert response.status_code == 200
    print(response.json())
    # # # assert response.json() == {"msg": "Hello World"}
    # print(response.json())
