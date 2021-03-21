import datetime
from pathlib import Path
from typing import List, Optional

from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm.session import Session

from opentunes_api import schemas
from opentunes_api.database.models import TrackModel as TrackModel
from opentunes_api.schemas import TrackSchema


def add_track(session: Session, track_schema: schemas.TrackSchema):
    image_files = []
    if track_schema.image_files:
        image_files = [image_file for image_file in track_schema.image_files]
    db_track = TrackModel(
        bitrate=track_schema.bitrate,
        bpm=track_schema.bpm,
        album=track_schema.album,
        artist=track_schema.artist,
        comment=track_schema.comment,
        duration=track_schema.duration,
        key=track_schema.key,
        file=str(track_schema.file),
        title=track_schema.title,
        import_error=track_schema.import_error,
        image_files=image_files,
        file_mtime=track_schema.file_mtime,
    )
    session.add(db_track)
    session.commit()
    session.refresh(db_track)
    return db_track


def get_tracks(session: Session, limit=None) -> List[TrackSchema]:
    result = []
    for track_model in session.query(TrackModel).limit(limit):
        result.append(TrackSchema.from_orm(track_model))
    return result


def get_track(
    session: Session, file: Path, file_mtime: datetime.datetime
) -> Optional[TrackSchema]:
    try:
        result = (
            session.query(TrackModel).filter_by(file=str(file), file_mtime=file_mtime).one()
        )
        return TrackSchema.from_orm(result)
    except NoResultFound:
        return None
