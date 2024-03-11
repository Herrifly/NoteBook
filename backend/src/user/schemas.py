from pydantic import BaseModel


class User(BaseModel):
    username: str
    login: str
    password: str
