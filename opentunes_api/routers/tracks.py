from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from opentunes_api.database import get_db
from opentunes_api.database.repository import get_tracks

router = APIRouter()


@router.get("/")
async def tracks_api(session: Session = Depends(get_db)):
    tracks = get_tracks(session=session)
    return tracks


#
# @router.get("/images/{path:path}", response_class=StreamingResponse)
# async def images(path: Path):
#     media_file = MediaFile(path)
#     if media_file.images:
#         image = media_file.images[0]
#         return StreamingResponse(io.BytesIO(image.data), media_type=image.mime_type)
#
#
# @router.get("/browse/{path:path}", response_class=HTMLResponse)
# async def browse(request: Request, path: Optional[Path] = None):
#     if not path:
#         path = Path(settings.music_root)
#     else:
#         path = Path(settings.music_root / path)
#
#     if path.is_dir():
#         links = []
#
#         for subdir in path.iterdir():
#             relpath = subdir.relative_to(settings.music_root)
#             links.append(
#                 {
#                     "href": f"/browse/{quote(str(relpath))}",
#                     "text": relpath.name,
#                 }
#             )
#         links = sorted(links, key=lambda k: k["text"])
#         return templates.TemplateResponse(
#             "track_list.html", {"request": request, "links": links}
#         )
#     else:
#         track = TrackSchema.from_path(path)
#         return templates.TemplateResponse(
#             "track_detail.html", {"request": request, "track": track, "images": images}
#         )
#
#
# @router.get("/api/browse/{path:path}")
# async def browse_api(path: Optional[Path] = None):
#     if not path:
#         path = Path(settings.music_root)
#     else:
#         path = Path(settings.music_root / path)
#
#     if path.is_dir():
#         links = []
#
#         for subdir in path.iterdir():
#             relpath = subdir.relative_to(settings.music_root)
#             links.append(
#                 {
#                     "href": f"/browse/{quote(str(relpath))}",
#                     "text": relpath.name,
#                 }
#             )
#         links = sorted(links, key=lambda k: k["text"])
#         return links
