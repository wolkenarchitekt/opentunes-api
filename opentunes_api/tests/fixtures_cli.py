import pytest
from typer.testing import CliRunner


@pytest.fixture
def cli_runner(db_session_tmpfile, sqlite_file):
    uri = f"sqlite:///{sqlite_file}"
    return CliRunner(env={"DATABASE_URL": uri})
