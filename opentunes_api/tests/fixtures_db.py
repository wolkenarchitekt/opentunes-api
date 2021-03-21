import os

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

import alembic
from alembic.config import Config
from opentunes_api.database.models import Base


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


@pytest.fixture(scope="session", autouse=True)
def settings(tmpdir_factory):
    os.environ["DATABASE_URL"] = "sqlite://"
    os.environ["MUSIC_ROOT"] = f"{tmpdir_factory.getbasetemp()}/music"
    os.environ["IMAGE_ROOT"] = f"{tmpdir_factory.getbasetemp()}/images"


@pytest.fixture(scope="session")
def apply_migrations():
    config = Config("alembic.ini")
    alembic.command.upgrade(config, "head")
    yield
    alembic.command.downgrade(config, "base")
