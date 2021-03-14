from pathlib import Path

from pydantic import BaseSettings


class Settings(BaseSettings):
    database_url: str

    # Root for entire music library
    music_root: Path

    # Root to cache images from tags
    image_root: Path

    class Config:
        env_file = ".env"
