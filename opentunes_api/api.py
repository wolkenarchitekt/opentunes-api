import io
from pathlib import Path
from typing import Optional
from urllib.parse import quote

from fastapi import Depends, FastAPI, Request
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.templating import Jinja2Templates
from mediafile import MediaFile
from sqlalchemy.orm import Session

from opentunes_api.config import Settings
from opentunes_api.database import get_db
from opentunes_api.database.repository import get_tracks
from opentunes_api.schemas import TrackSchema

settings = Settings()
templates = Jinja2Templates(directory="opentunes_api/templates")


def get_app() -> FastAPI:
    application = FastAPI(title="OpenTunes")
    return application


fastapi_app = get_app()


@fastapi_app.get("/info")
async def info(session: Session = Depends(get_db)):
    tracks = get_tracks(session=session)
    print(f"Tracks: {tracks}")
    return settings.dict()


@fastapi_app.get("/api/tracks")
@fastapi_app.get("/api/tracks/")
def tracks_api(session: Session = Depends(get_db)):
    tracks = get_tracks(session=session)
    from ipdb import set_trace; set_trace()
    return tracks


@fastapi_app.get("/images/{path:path}", response_class=StreamingResponse)
async def images(path: Path):
    media_file = MediaFile(path)
    if media_file.images:
        image = media_file.images[0]
        return StreamingResponse(io.BytesIO(image.data), media_type=image.mime_type)


@fastapi_app.get("/browse/{path:path}", response_class=HTMLResponse)
async def browse(request: Request, path: Optional[Path] = None):
    path = Path(settings.music_root / path)

    if path.is_dir():
        links = []

        for subdir in path.iterdir():
            relpath = subdir.relative_to(settings.music_root)
            links.append(
                {
                    "href": f"/browse/{quote(str(relpath))}",
                    "text": relpath.name,
                }
            )
        links = sorted(links, key=lambda k: k["text"])
        return templates.TemplateResponse(
            "track_list.html", {"request": request, "links": links}
        )
    else:
        track = TrackSchema.from_path(path)
        return templates.TemplateResponse(
            "track_detail.html", {"request": request, "track": track, "images": images}
        )


@fastapi_app.get("/api/browse/{path:path}")
async def browse_api(path: Optional[Path] = None):
    path = Path(settings.music_root / path)

    if path.is_dir():
        links = []

        for subdir in path.iterdir():
            relpath = subdir.relative_to(settings.music_root)
            links.append(
                {
                    "href": f"/browse/{quote(str(relpath))}",
                    "text": relpath.name,
                }
            )
        links = sorted(links, key=lambda k: k["text"])
        return links
