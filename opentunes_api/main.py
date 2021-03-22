from fastapi import FastAPI

from opentunes_api.cli import typer_app

fastapi_app = FastAPI()


def main():
    typer_app()


if __name__ == "__main__":
    main()
