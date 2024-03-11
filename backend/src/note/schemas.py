from pydantic import BaseModel

from backend.src.user.schemas import UserRead
from typing import Optional, List


class Note(BaseModel):
    name: str
    description: Optional[str]
    user: UserRead


class Notes(BaseModel):
    notes: List[Note]
