import datetime
from pydantic import BaseModel, Field


class User(BaseModel):
    name: str
    hashed_pwd: str
    salt: str


class Record(BaseModel):
    id: str
    username: str
    timestamp: datetime.datetime = Field(default=datetime.datetime.now())
    data: str | None = None
