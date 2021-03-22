from fastapi import FastAPI
from fastapi.templating import Jinja2Templates

from opentunes_api.config import Settings
from opentunes_api.routes import router

settings = Settings()
templates = Jinja2Templates(directory="opentunes_api/templates")


def get_application() -> FastAPI:
    application = FastAPI(title=settings.title)
    application.include_router(router)
    return application


fastapi_app = get_application()
