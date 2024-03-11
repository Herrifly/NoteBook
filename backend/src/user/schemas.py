from typing import Annotated, Optional, List

from bson import ObjectId
from pydantic import BaseModel, BeforeValidator, Field, ConfigDict

from database import PyObjectId



class UserRead(BaseModel):
    id: Optional[PyObjectId] = Field(alias='_id', default=None)
    username: str
    login: str


class User(UserRead):
    password: str


class Users(BaseModel):
    users: List[UserRead]
