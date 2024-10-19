from typing import Optional

from pydantic import BaseModel


class AddLogEventModel(BaseModel):
    id: str
    timezone: str
    title: Optional[str]
    url: str
    date: str
