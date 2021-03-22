import logging
import os
from pathlib import Path
from typing import Generator

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


def iter_media_files(path: Path) -> Generator[Path, None, None]:
    for path in [
        Path(os.path.join(dirpath, f))
        for dirpath, dirnames, filenames in os.walk(path)
        for f in filenames
        if f.endswith(EXTENSIONS)
    ]:
        yield path


def iter_tracks(path: Path) -> Generator[TrackSchema, None, None]:
    """Iterate valid music files"""
    settings = Settings()
    if settings.music_root not in path.parents and settings.music_root != path:
        raise MusicImportError(
            f"Path '{path}' is not a subdirectory of MUSIC_ROOT:'{settings.music_root}'."
        )

    if path.is_dir():
        for file in iter_media_files(path):
            yield TrackSchema.from_path(file)
    else:
        yield TrackSchema.from_path(path)
