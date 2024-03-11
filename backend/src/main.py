from fastapi import FastAPI
from user.router import router as user_router

app = FastAPI()


@app.get('/')
async def hello():
    return 'Hello'

app.include_router(user_router)