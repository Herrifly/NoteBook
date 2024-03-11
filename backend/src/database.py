from typing import Annotated
from pydantic import BeforeValidator
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/notebook")

db = client["notebook"]

users = db['users']
notes = db['notes']


PyObjectId = Annotated[str, BeforeValidator(str)]