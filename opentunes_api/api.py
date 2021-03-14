import pprint
from pathlib import Path
from typing import Optional
from urllib.parse import quote

from fastapi import Depends, Request
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from opentunes_api.config import Settings
from opentunes_api.database import get_db
from opentunes_api.database.repository import get_tracks
from opentunes_api.main import fastapi_app

settings = Settings()
templates = Jinja2Templates(directory="opentunes_api/templates")


@fastapi_app.get("/")
async def root(session: Session = Depends(get_db)):
    tracks = get_tracks(session=session)[:20]
    return tracks


@fastapi_app.get("/tracks/favicon.ico")
async def favicon():
    return ""


@fastapi_app.get("/test")
async def test(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "foo": "bar"})


@fastapi_app.get("/tracks/{path:path}", response_class=HTMLResponse)
async def tracks(request: Request, path: Optional[Path] = None):
    path = Path(settings.music_root / path)

    if path.is_dir():
        links = []

        for subdir in path.iterdir():
            relpath = subdir.relative_to(settings.music_root)
            links.append(
                {
                    "href": f"/tracks/{quote(str(relpath))}",
                    "text": relpath.name,
                }
            )
        links = sorted(links, key=lambda k: k["text"])
        pprint.pprint(links)
        return templates.TemplateResponse(
            "track_list.html", {"request": request, "links": links}
        )
    else:
        data = open(path, mode="rb")
        return StreamingResponse(data)
