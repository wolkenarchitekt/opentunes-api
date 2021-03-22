import logging
import pprint
from pathlib import Path
from typing import List

import typer
import uvicorn
from prettytable import PrettyTable

from opentunes_api.config import Settings
from opentunes_api.database import db_session
from opentunes_api.database.repository import add_track, get_track, get_tracks
from opentunes_api.mediafile_import import MusicImportError, iter_tracks

logger = logging.getLogger(__name__)
typer_app = typer.Typer()


logging.getLogger("PIL").setLevel(logging.WARN)


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
def import_tracks(files: List[Path] = typer.Argument(None)):
    settings = Settings()

    if not files:
        files = [settings.music_root]

    with db_session() as session:
        for file in files:
            try:
                for track_schema in iter_tracks(path=file):
                    track_up_to_date = (
                        get_track(
                            session=session,
                            file=track_schema.file,
                            file_mtime=track_schema.file_mtime,
                        )
                        is not None
                    )
                    if not track_schema.import_error and not track_up_to_date:
                        add_track(session=session, track_schema=track_schema)
            except MusicImportError as error:
                logger.error(f"Error importing '{file}': {error}")


@typer_app.command()
def config():
    settings = Settings()
    pprint.pprint(settings.__dict__)


@typer_app.command()
def info():
    logger = logging.getLogger(__name__)
    logger.debug("DEBUG")
    logger.info("INFO")
    logger.warning("WARNING")
    logger.error("ERROR")


def truncate(text: str, max_length: int) -> str:
    text = text or ""
    text = str(text)
    if len(text) < max_length:
        return text
    else:
        return text[: max_length - 3] + "..."


@typer_app.command()
def list_tracks(columns: str = "artist,title"):
    columns_list = columns.split(",")

    with db_session() as session:
        tracks = get_tracks(session=session, limit=20)

    table = PrettyTable()
    table.field_names = columns_list
    table.align = "l"

    for track in tracks:
        values_list = []
        for column in columns_list:
            values_list.append(truncate(track.dict()[column], max_length=50))
        table.add_row(values_list)

    print(table)


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
