from fastapi import APIRouter

from . import signalling

route = APIRouter(prefix="/websocket")

route.include_router(signalling.route)