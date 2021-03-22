import logging
logging.getLogger('sqlalchemy.engine').setLevel(logging.DEBUG)

from fixtures_cli import *
from fixtures_db import *
from fixtures_db_mediafile import *
from fixtures_mediafile import *




@pytest.fixture(scope="session", autouse=True)
def settings(tmpdir_factory):
    os.environ["STAGE"] = "TESTING"
    os.environ["DATABASE_URL"] = "sqlite://"
    os.environ["MUSIC_ROOT"] = f"{tmpdir_factory.getbasetemp()}/music"
    os.environ["IMAGE_ROOT"] = f"{tmpdir_factory.getbasetemp()}/images"
