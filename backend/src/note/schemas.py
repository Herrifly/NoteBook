from pydantic import BaseModel

from backend.src.user.schemas import User


class Note(BaseModel):
    name: str
    description: str
    user: User
