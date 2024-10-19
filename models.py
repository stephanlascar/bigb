from pydantic import BaseModel


class AddLogEventModel(BaseModel):
    id: str
    timezone: str
    title: str
    url: str
    date: str
