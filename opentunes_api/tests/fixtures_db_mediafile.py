import pytest

from opentunes_api.database.repository import add_track
from opentunes_api.schemas import TrackSchema


@pytest.fixture
def track_db(mp3_file, db_session):
    track_schema = TrackSchema.from_path(mp3_file)
    add_track(session=db_session, track_schema=track_schema)
