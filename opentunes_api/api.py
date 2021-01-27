from opentunes_api.main import fastapi_app


@fastapi_app.get("/")
async def root():
    return {"message": "Hello World"}
