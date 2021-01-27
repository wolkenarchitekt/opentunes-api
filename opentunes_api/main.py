from fastapi import FastAPI

from opentunes_api.cli import typer_app

fastapi_app = FastAPI()


if __name__ == "__main__":
    typer_app()
