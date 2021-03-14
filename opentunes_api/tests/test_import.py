from opentunes_api.config import Settings
from opentunes_api.mediafile_import import track_from_path


def test_import(mp3_file):

    Settings.music_root = "/tmp/pytest-of-iweinmann/"
    track = track_from_path(mp3_file)
    assert track.artist
    assert track.title
