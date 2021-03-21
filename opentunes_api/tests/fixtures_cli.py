import pytest
from typer.testing import CliRunner


@pytest.fixture
def cli_runner(db_session_tmpfile, sqlite_file_uri):
    return CliRunner(env={"DATABASE_URL": sqlite_file_uri})
