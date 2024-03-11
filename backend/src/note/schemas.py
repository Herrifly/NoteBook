from pydantic import BaseModel, Field
from database import PyObjectId

from user.schemas import UserRead
from typing import Optional, List


class Note(BaseModel):
    id: Optional[PyObjectId] = Field(alias='_id', default=None)
    name: str
    description: Optional[str]
    user: PyObjectId = Field(alias='user_id')

class NotePatch(BaseModel):
    name: str
    desctiption: str


class Notes(BaseModel):
    notes: List[Note]
