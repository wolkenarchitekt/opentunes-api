from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.sql.schema import Column
from sqlalchemy.types import Integer, String
from fastapi import Depends
from opentunes_api import schemas

SQLALCHEMY_DATABASE_URL = "sqlite:///opentunes.sqlite"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
)
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_tables():
    Base.metadata.create_all(bind=engine)


class Track(Base):
    __tablename__ = "tracks"
    id = Column(Integer, primary_key=True, index=True)
    artist = Column(String)
    title = Column(String)


def create_track(track: schemas.Track):
    db = SessionLocal()
    db_track = Track(artist=track.artist, title=track.title)
    db.add(db_track)
    db.commit()
    db.refresh(db_track)
    return db_track
