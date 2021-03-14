from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.schema import Column
from sqlalchemy.types import DateTime, Integer, String

from opentunes_api.database.types import ArrayType, DBAgnosticNumeric

Base = declarative_base()


class Track(Base):
    __tablename__ = "tracks"
    id = Column(Integer, primary_key=True, index=True)
    artist = Column(String)
    title = Column(String)
    path = Column(String)
    comment = Column(String)
    bpm = Column(DBAgnosticNumeric)
    key = Column(String)
    duration = Column(DBAgnosticNumeric)
    bitrate = Column(Integer)
    album = Column(String)
    import_error = Column(String)
    image_files = Column(ArrayType)
    file_mtime = Column(DateTime)
