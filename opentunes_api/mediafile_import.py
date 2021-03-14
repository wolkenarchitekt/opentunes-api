import datetime
import logging
import os
from pathlib import Path
from typing import Generator

import mediafile

from opentunes_api.config import Settings
from opentunes_api.schemas import TrackSchema

logger = logging.getLogger(__name__)


EXTENSIONS = (
    ".aif",
    ".aifc",
    ".aiff",
    ".amr",
    ".awb",
    ".axa",
    ".csd",
    ".flac",
    ".gsm",
    ".kar",
    ".m4a",
    ".mid",
    ".midi",
    ".mp2",
    ".mp3",
    ".mpega",
    ".mpga",
    ".oga",
    ".ogg",
    ".opus",
    ".orc",
    ".pls",
    ".ra",
    ".ram",
    ".rm",
    ".sco",
    ".sd2",
    ".sid",
    ".snd",
    ".spx",
    ".wav",
    ".wax",
    ".wma",
)


class MusicImportError(Exception):
    pass


def extract_images(media_file: mediafile.MediaFile):
    settings = Settings()
    image_files = []
    for i, image in enumerate(media_file.images):
        rel_file = media_file.path.relative_to(settings.music_root)
        rel_path = rel_file.parent
        suffix = image.mime_type.split("/")[-1]
        image_path = Path(settings.image_root / rel_path)
        image_file = Path(image_path / f"{rel_file.stem}{i}.{suffix}")
        os.makedirs(image_path, exist_ok=True)

        with open(image_file, "wb") as f:
            f.write(image.data)

        image_files.append(image_file.relative_to(settings.image_root))
    return image_files


def track_from_path(path: Path) -> TrackSchema:
    settings = Settings()
    logger.debug(f"Importing track: {path.name}")

    file_modification_date = datetime.datetime.fromtimestamp(path.stat().st_mtime)
    track = TrackSchema(
        path=path.relative_to(settings.music_root), file_mtime=file_modification_date
    )

    try:
        media_file = mediafile.MediaFile(path)
        track.image_files = extract_images(media_file)
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


def iter_media_files(path: Path) -> Generator[Path, None, None]:
    for path in [
        Path(os.path.join(dirpath, f))
        for dirpath, dirnames, filenames in os.walk(path)
        for f in filenames
        if f.endswith(EXTENSIONS)
    ]:
        yield path


def iter_tracks(path: Path) -> Generator[TrackSchema, None, None]:
    settings = Settings()
    if settings.music_root not in path.parents and settings.music_root != path:
        raise MusicImportError(
            f"Path '{path}' is not a subdirectory of MUSIC_ROOT:'{settings.music_root}'."
        )

    if path.is_dir():
        for file in iter_media_files(path):
            yield track_from_path(file)
    else:
        yield track_from_path(path)
