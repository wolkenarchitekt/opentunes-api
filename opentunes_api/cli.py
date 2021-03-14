import logging
from pathlib import Path
from typing import List

import typer
import uvicorn
from tabulate import tabulate

from opentunes_api.config import Settings
from opentunes_api.database import db_session
from opentunes_api.database.repository import add_track, get_tracks
from opentunes_api.mediafile_import import MusicImportError, iter_tracks

logger = logging.getLogger(__name__)
typer_app = typer.Typer()
settings = Settings()


@typer_app.callback()
def main(verbose: int = typer.Option(0, "--verbose", "-v", count=True)):
    if verbose == 0:
        logging.basicConfig(level=logging.WARNING)
    elif verbose == 1:
        logging.basicConfig(level=logging.INFO)
    elif verbose >= 2:
        logging.basicConfig(level=logging.DEBUG)

    logging.getLogger("watchgod.main").setLevel(logging.WARNING)


@typer_app.command(name="import")
def import_tracks(files: List[Path] = typer.Argument(...)):
    if not files:
        files = [settings.music_root]

    for file in files:
        try:
            for track_schema in iter_tracks(path=file):
                if not track_schema.import_error:
                    with db_session() as session:
                        add_track(session=session, track_schema=track_schema)
        except MusicImportError as error:
            # raise typer.Exit(error)
            logger.error(f"Error importing '{file}': {error}")


@typer_app.command()
def info():
    logger = logging.getLogger(__name__)
    logger.debug("DEBUG")
    logger.info("INFO")
    logger.warning("WARNING")
    logger.error("ERROR")


@typer_app.command()
def list_tracks():
    max_length = 30
    with db_session() as session:
        tracks = get_tracks(session=session)
        data = []
        for track in tracks:
            if track.artist:
                artist = (
                    track.artist
                    if len(track.artist) < max_length
                    else track.artist[: max_length - 3] + "..."
                )
            else:
                artist = ""

            if track.title:
                title = (
                    track.title
                    if len(track.title) < max_length
                    else track.title[: max_length - 3] + "..."
                )
            else:
                title = ""

            data.append(
                {
                    "Artist": artist,
                    "Title": title,
                }
            )

        print(tabulate(data, headers="keys", tablefmt="simple"))


@typer_app.command()
def server(
    reload: bool = False,
    log_level: str = "info",
    port: int = 5000,
    host: str = "127.0.0.1",
):
    uvicorn.run(
        "opentunes_api.api:fastapi_app",
        host=host,
        port=port,
        log_level=log_level,
        reload=reload,
    )
