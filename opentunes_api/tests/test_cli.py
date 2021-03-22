import pytest
from click.testing import Result
from typer.testing import CliRunner

from opentunes_api.cli import typer_app
from opentunes_api.schemas import TrackSchema


@pytest.fixture
def cli_runner(db_session_tmpfile, sqlite_file):
    uri = f"sqlite:///{sqlite_file}"
    return CliRunner(env={"DATABASE_URL": uri})


def assert_exit_code(result: Result):
    if result.exception:
        raise result.exception
    assert result.exit_code == 0


def test_import_cli(mp3_file, cli_runner):
    track = TrackSchema.from_path(mp3_file)

    result = cli_runner.invoke(typer_app, ["import"])
    assert_exit_code(result)

    result = cli_runner.invoke(typer_app, "list-tracks")
    assert result.exit_code == 0

    assert track.artist in result.stdout
    assert track.title in result.stdout
