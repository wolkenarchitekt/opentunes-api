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

fake = faker.Faker(["de_DE", "en_US", "ja_JP"])


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
