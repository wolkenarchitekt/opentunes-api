import os
import random
import subprocess
import tempfile
from io import BytesIO
from pathlib import Path
from typing import ByteString

import faker
import mediafile
import pytest
from PIL import Image
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from typer.testing import CliRunner

import alembic
from alembic.config import Config
from opentunes_api.database.models import Base

fake = faker.Faker(["de_DE", "en_US", "ja_JP"])


def pytest_addoption(parser):
    parser.addoption(
        "--collect-tests",
        action="store_true",
        help="Collect tests",
        default=False,
    )


def pytest_collection_modifyitems(config, items):
    tests = set()
    if config.option.collect_tests:
        for item in items:
            # filename::test_class[optional]::test_function
            path = os.path.relpath(item.module.__file__)
            item.add_marker(pytest.mark.skipif(True, reason="Skip"))
            tests.add("{}\n".format(path))
            test_str = path
            if item.cls:
                test_str += f"::{item.cls.__name__}"
            if item.function:
                test_str += f"::{item.function.__name__}"
            tests.add(f"{test_str}\n")
        with open(".pytest.completion", "w") as file:
            file.writelines(tests)


@pytest.fixture(scope="session", autouse=True)
def settings(tmpdir_factory):
    os.environ["DATABASE_URL"] = "sqlite://"
    os.environ["MUSIC_ROOT"] = f"{tmpdir_factory.getbasetemp()}/music"
    os.environ["IMAGE_ROOT"] = f"{tmpdir_factory.getbasetemp()}/images"


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
def db_session(engine, tables):
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
def cli_runner(db_session_tmpfile, sqlite_file):
    # CLI needs file-based sqlite, otherwise DB fixtures won't work
    uri = f"sqlite:///{sqlite_file}"
    return CliRunner(env={"DATABASE_URL": uri})
