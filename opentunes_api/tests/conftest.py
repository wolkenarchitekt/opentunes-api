import faker
import logging
import subprocess
from pathlib import Path
from typing import List
import tempfile
import mediafile
import pytest

logger = logging.getLogger(__name__)

fake = faker.Faker(['it_IT', 'en_US', 'ja_JP'])

def create_mp3(path: Path, duration=5):
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


def set_id3_tags(filename):
    mf = mediafile.MediaFile(filename)
    mf.artist = fake.name()
    mf.title = fake.name()
    print(mf.__dict__)
    mf.save()


@pytest.fixture(scope="session")
def mp3_file(request, tmpdir_factory) -> Path:
    """ 
    Generate a valid MP3 file using ffmpeg.
    
    Parametrize fixture to set filename:
    @pytest.mark.parametrize("mp3_file", ("foobar.mp3",), indirect=True)
    """
    tmpdir = tmpdir_factory.mktemp("data")
    if not hasattr(request, "param"):
        filename = tempfile.NamedTemporaryFile(suffix=".mp3", dir=tmpdir).name
    else:
        filename = request.param
        filename = tmpdir / filename
    path = create_mp3(path=filename)
    set_id3_tags(filename)
    print(filename)
    return path
