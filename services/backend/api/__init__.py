from fastapi import APIRouter

from . import notes, users

route = APIRouter(prefix="/api")

route.include_router(users.route)
route.include_router(notes.route)