from fastapi import FastAPI

fastapi_app = FastAPI()


if __name__ == "__main__":
    from cli import typer_app

    typer_app()
