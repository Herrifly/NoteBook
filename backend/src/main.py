from fastapi import FastAPI
from user.router import router as user_router
from note.router import router as note_router

app = FastAPI()


@app.get('/')
async def hello():
    return 'Hello'

app.include_router(user_router)
app.include_router(note_router)