from __future__ import annotations

import datetime
import logging
from decimal import Decimal
from pathlib import Path
from typing import List, Optional

import mediafile
import pydantic
from pydantic import FilePath


class TrackSchema(pydantic.BaseModel):
    class Config:
        orm_mode = True

    file: FilePath  # Relative to music_root
    file_mtime: datetime.datetime

    artist: Optional[str]
    title: Optional[str]
    comment: Optional[str]
    bpm: Optional[Decimal]
    key: Optional[str]
    duration: Optional[Decimal]
    bitrate: Optional[int]
    album: Optional[str]
    import_error: Optional[str]
    image_files: Optional[List[str]]
    image_import_error: Optional[str]

    @classmethod
    def from_path(cls, path: Path) -> "TrackSchema":
        logger = logging.getLogger(__name__)
        logger.debug(f"Importing track: {path.name}")

        file_modification_date = datetime.datetime.fromtimestamp(path.stat().st_mtime)

        track = TrackSchema(file=path, file_mtime=file_modification_date)

        try:
            media_file = mediafile.MediaFile(path)
            track.artist = media_file.artist
            track.title = media_file.title
            track.comment = media_file.comments
            track.bpm = media_file.bpm
            track.key = media_file.initial_key
            track.duration = media_file.length
            track.bitrate = media_file.bitrate
            track.album = media_file.album
        except (mediafile.FileTypeError, mediafile.UnreadableFileError) as error:
            track.import_error = str(error)

        return track
