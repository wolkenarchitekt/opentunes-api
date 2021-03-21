from typer.testing import CliRunner

from opentunes_api.schemas import TrackSchema

runner = CliRunner()


def test_import(mp3_file, tmpdir_factory):
    track = TrackSchema.from_path(mp3_file)
    assert track.artist
    assert track.title
