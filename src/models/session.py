from pydantic import BaseModel, Field
from datetime import datetime as dt


class Session(BaseModel):
    nickname: str = Field(..., alias="nickname")
    game: str = Field(..., alias="game")
    created_at: str = Field(dt.now(), alias="created_at")