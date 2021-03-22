import os
import random
import subprocess
import tempfile
from io import BytesIO
from pathlib import Path
from typing import Any, ByteString, Generator

import faker
import mediafile
import pytest
from fastapi import FastAPI
from PIL import Image
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from starlette.testclient import TestClient
from typer.testing import CliRunner

import alembic
from alembic.config import Config
from opentunes_api.api import get_application
from opentunes_api.database import get_db
from opentunes_api.database.models import Base
from opentunes_api.database.repository import add_track
from opentunes_api.schemas import TrackSchema

fake = faker.Faker(["de_DE", "en_US", "ja_JP"])


@pytest.fixture(scope="session", autouse=True)
def settings(tmpdir_factory):
    os.environ["DATABASE_URL"] = "sqlite://"
    os.environ["MUSIC_ROOT"] = f"{tmpdir_factory.getbasetemp()}/music"
    os.environ["IMAGE_ROOT"] = f"{tmpdir_factory.getbasetemp()}/images"


@pytest.fixture(autouse=True)
def app() -> Generator[FastAPI, Any, None]:
    """
    Create a fresh database on each test case.
    """
    _app = get_application()
    yield _app


@pytest.fixture(scope="session")
def sqlite_file(tmpdir_factory):
    fn = f"{tmpdir_factory.getbasetemp()}/opentunes.sqlite"
    return fn


@pytest.fixture(scope="session")
def sqlite_uri(sqlite_file):
    return f"sqlite:///{sqlite_file}"


@pytest.fixture(scope="session")
def engine():
    return create_engine("sqlite://")


@pytest.fixture(scope="session")
def engine_tmpfile(sqlite_uri):
    return create_engine(sqlite_uri)


@pytest.fixture(scope="session")
def tables(engine):
    Base.metadata.create_all(engine)
    yield
    Base.metadata.drop_all(engine)


@pytest.fixture(scope="session")
def tables_tmpfile(engine_tmpfile):
    Base.metadata.create_all(engine_tmpfile)
    yield
    Base.metadata.drop_all(engine_tmpfile)


@pytest.fixture(scope="function")
def db_session(app, engine, tables):
    """Returns an sqlalchemy session, and after the test tears down everything properly."""
    connection = engine.connect()
    # begin the nested transaction
    transaction = connection.begin()
    # use the connection with the already started transaction
    session = Session(bind=connection)

    yield session

    session.close()
    # roll back the broader transaction
    transaction.rollback()
    # put back the connection to the connection pool
    connection.close()


@pytest.fixture(scope="function")
def db_session_tmpfile(engine_tmpfile, tables_tmpfile):
    """Returns an sqlalchemy session, and after the test tears down everything properly."""
    connection = engine_tmpfile.connect()
    # begin the nested transaction
    transaction = connection.begin()
    # use the connection with the already started transaction
    session = Session(bind=connection)

    yield session

    session.close()
    # roll back the broader transaction
    transaction.rollback()
    # put back the connection to the connection pool
    connection.close()


@pytest.fixture(scope="session")
def apply_migrations():
    config = Config("alembic.ini")
    alembic.command.upgrade(config, "head")
    yield
    alembic.command.downgrade(config, "base")


# Needs ffmpeg installed
def create_mp3(path: Path, duration=5) -> Path:
    subprocess.run(
        [
            "/usr/bin/ffmpeg",
            "-y",
            "-f",
            "lavfi",
            "-i",
            f"sine=frequency=1000:duration={duration}",
            "-t",
            f"{duration}",
            "-q:a",
            "9",
            "-acodec",
            "libmp3lame",
            f"{path}",
        ],
        check=True,
        capture_output=True,
    )
    return Path(path)


@pytest.fixture(scope="session")
def image_data() -> ByteString:
    image = Image.new("RGB", (64, 64))
    pixels = image.load()
    for x in range(image.size[0]):
        for y in range(image.size[1]):
            pixels[x, y] = (
                random.randint(0, 255),
                random.randint(0, 255),
                random.randint(0, 255),
            )
    output = BytesIO()
    image.save(output, "JPEG")
    return output.getvalue()


def set_id3_tags(filename, image_data):
    mf = mediafile.MediaFile(filename)
    mf.artist = fake.name()
    mf.title = fake.name()
    mf.images = [mediafile.Image(data=image_data)]
    mf.save()


@pytest.fixture(scope="session")
def mp3_file(request, tmpdir_factory, image_data) -> Path:
    """
    Generate a valid MP3 file using ffmpeg.

    Parametrize fixture to set filename:
    @pytest.mark.parametrize("mp3_file", ("foobar.mp3",), indirect=True)
    """
    tmpdir = tmpdir_factory.mktemp("data")

    # Overwrite pydantic settings and use tempdir for music root
    os.environ["MUSIC_ROOT"] = str(tmpdir)

    if not hasattr(request, "param"):
        filename = tempfile.NamedTemporaryFile(suffix=".mp3", dir=tmpdir).name
    else:
        filename = request.param
        filename = tmpdir / filename
    path = create_mp3(path=Path(filename))
    set_id3_tags(filename=filename, image_data=image_data)
    return path


@pytest.fixture
def track_db(mp3_file, db_session):
    track_schema = TrackSchema.from_path(mp3_file)
    track_model = add_track(session=db_session, track_schema=track_schema)
    return track_model


@pytest.fixture
def cli_runner(db_session_tmpfile, sqlite_file):
    # CLI needs file-based sqlite, otherwise DB fixtures won't work
    uri = f"sqlite:///{sqlite_file}"
    return CliRunner(env={"DATABASE_URL": uri})


@pytest.fixture()
def api_client(app: FastAPI, db_session: Session) -> Generator[TestClient, Any, None]:
    """
    Create a new FastAPI TestClient that uses the `db_session` fixture to override
    the `get_db` dependency that is injected into routes.
    """

    def _get_test_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = _get_test_db
    with TestClient(app) as client:
        yield client
