from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/notebook")

db = client["notebook"]

users = db['users']
notes = db['notes']
