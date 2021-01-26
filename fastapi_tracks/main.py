import mimetypes
import os
from datetime import datetime
from pathlib import Path
from typing import List, Optional

import pydantic
import typer
import uvicorn
from fastapi import FastAPI

fastapi_app = FastAPI()
typer_app = typer.Typer()



class Track(pydantic.BaseModel):
    artist: Optional[str]
    title: Optional[str]
    file: Path


@typer_app.command()
def server():
    uvicorn.run(
        "fastapi_tracks.main:app", host="127.0.0.1", port=5000, log_level="info"
    )

def is_audiofile(path: Path):
    mimetype = mimetypes.guess_type(path)
    if mimetype and mimetype[0] and "audio" in mimetype[0].lower():
        return True
    return False


@typer_app.command()
def import_tracks(path: Path):
    files = [file for file in os.scandir(path) if file.is_file() and is_audiofile(file)]
    for file in files:
        print(file.name)


@fastapi_app.get("/")
async def root():
    return {"message": "Hello World"}


if __name__ == "__main__":
    typer_app()
