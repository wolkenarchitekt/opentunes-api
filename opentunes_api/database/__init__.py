from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from opentunes_api.config import Settings


def get_engine():
    settings = Settings()
    print(settings.database_url)
    if "sqlite" in settings.database_url:
        return create_engine(
            settings.database_url, connect_args={"check_same_thread": False}
        )
    else:
        return create_engine(settings.database_url)


def get_db():
    engine = get_engine()
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@contextmanager
def db_session():
    """Creates a context with an open SQLAlchemy session."""
    engine = get_engine()
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
