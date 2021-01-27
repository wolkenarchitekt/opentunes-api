import mimetypes
from pathlib import Path

import mediafile

from opentunes_api.schemas import Track


def is_audiofile(path: Path):
    mimetype = mimetypes.guess_type(path)
    if mimetype and mimetype[0] and "audio" in mimetype[0].lower():
        return True
    return False


def track_from_path(path) -> Track:
    track = Track(path=path)
    try:
        media_file = mediafile.MediaFile(path)
    except (mediafile.FileTypeError, mediafile.UnreadableFileError):
        pass
    else:
        track.artist = media_file.artist
        track.title = media_file.title
    return track
