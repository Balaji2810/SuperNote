from contextlib import asynccontextmanager
from fastapi import FastAPI
from database import mongo_init
import api, websocket

@asynccontextmanager
async def lifespan(app: FastAPI):
    await mongo_init()
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(api.route)
app.include_router(websocket.route)


