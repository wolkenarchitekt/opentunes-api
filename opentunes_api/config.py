import os
from pathlib import Path

from pydantic import BaseSettings


class Settings(BaseSettings):
    database_url: str

    # Root dir for entire music library
    music_root: Path

    class Config:
        if os.environ.get("STAGE", "DEVELOPMENT") == "DEVELOPMENT":
            env_file = ".env"
