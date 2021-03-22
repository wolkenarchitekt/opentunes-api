from asgi_lifespan import LifespanManager
import logging

# logging.getLogger('sqlalchemy.engine').setLevel(logging.DEBUG)
from fastapi import FastAPI

from fixtures_cli import *
from fixtures_db import *
from fixtures_db_mediafile import *
from fixtures_mediafile import *


@pytest.fixture(scope="session", autouse=True)
def settings(tmpdir_factory):
    os.environ["STAGE"] = "TESTING"
    # os.environ["DATABASE_URL"] = "sqlite://"
    os.environ["MUSIC_ROOT"] = f"{tmpdir_factory.getbasetemp()}/music"
    os.environ["IMAGE_ROOT"] = f"{tmpdir_factory.getbasetemp()}/images"


@pytest.fixture
def app(apply_migrations: None) -> FastAPI:
    from app.main import get_application  # local import for testing purpose

    return get_application()


@pytest.fixture
async def initialized_app(app: FastAPI) -> FastAPI:
    async with LifespanManager(app):
        yield app

