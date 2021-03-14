from sqlalchemy.orm.session import Session

from opentunes_api import schemas
from opentunes_api.database.models import Track as TrackModel


def add_track(session: Session, track_schema: schemas.TrackSchema):
    image_files = []
    if track_schema.image_files:
        image_files = [path.name for path in track_schema.image_files]
    db_track = TrackModel(
        bitrate=track_schema.bitrate,
        bpm=track_schema.bpm,
        album=track_schema.album,
        artist=track_schema.artist,
        comment=track_schema.comment,
        duration=track_schema.duration,
        key=track_schema.key,
        path=str(track_schema.path),
        title=track_schema.title,
        import_error=track_schema.import_error,
        image_files=image_files,
        file_mtime=track_schema.file_mtime,
    )
    session.add(db_track)
    session.commit()
    session.refresh(db_track)
    return db_track


def get_tracks(session: Session, limit=None):
    return session.query(TrackModel).limit(limit)
