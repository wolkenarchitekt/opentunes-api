from pathlib import Path
from typing import Optional

import pydantic


class Track(pydantic.BaseModel):
    artist: Optional[str]
    title: Optional[str]
    path: Path
