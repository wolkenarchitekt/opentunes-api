import os
from pathlib import Path

import typer
import uvicorn
from mediafile_utils import is_audiofile, track_from_path

typer_app = typer.Typer()


@typer_app.command()
def server():
    uvicorn.run(
        "fastapi_tracks.main:app", host="127.0.0.1", port=5000, log_level="info"
    )


@typer_app.command()
def import_tracks(path: Path):
    files = [file for file in os.scandir(path) if file.is_file() and is_audiofile(file)]
    for file in files:
        print(track_from_path(file))
