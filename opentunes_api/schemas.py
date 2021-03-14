import datetime
from decimal import Decimal
from pathlib import Path
from typing import List, Optional

import pydantic
from pydantic import FilePath


class TrackSchema(pydantic.BaseModel):
    artist: Optional[str]
    title: Optional[str]
    path: Path
    comment: Optional[str]
    bpm: Optional[Decimal]
    key: Optional[str]
    duration: Optional[Decimal]
    bitrate: Optional[int]
    album: Optional[str]
    import_error: Optional[str]
    image_files: Optional[List[FilePath]]
    file_mtime: datetime.datetime
