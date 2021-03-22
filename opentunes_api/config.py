import os
from pathlib import Path

from pydantic import BaseSettings

# Split config:
# https://rednafi.github.io/digressions/python/2020/06/03/python-configs.html


class Settings(BaseSettings):
    database_url: str

    # Root dir for entire music library
    music_root: Path

    # Root dir to cache images from tags
    image_root: Path

    class Config:
        if os.environ.get("STAGE", "DEVELOPMENT") == "DEVELOPMENT":
            env_file = ".env"
