from opentunes_api.database.repository import add_track, get_track, get_tracks
from opentunes_api.schemas import TrackSchema


def test_add_track(mp3_file, db_session):
    track_schema = TrackSchema.from_path(mp3_file)
    add_track(db_session, track_schema)
    assert len(get_tracks(db_session)) == 1
    assert (
        get_track(
            session=db_session,
            file=track_schema.file,
            file_mtime=track_schema.file_mtime,
        )
        is not None
    )
