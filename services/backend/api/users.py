from fastapi import APIRouter, status, Request, Query
from database import User
from pymongo.errors import DuplicateKeyError
from . import schemas
from .schemas import GenericResponse
from auth import create_jwt, auth_required
import json

route = APIRouter()


@route.post("/signup")
async def add_user(user:schemas.User):
    try:
        username = user.username
        password = user.hash_password()

        user = User(username=username, password=password)
        await user.create()
        return GenericResponse()
    except DuplicateKeyError:
        return GenericResponse(status_code=status.HTTP_409_CONFLICT,message="User name not available!!")


@route.post("/login")
async def login(user:schemas.User):
    
    username = user.username

    _user = await User.find_one(User.username == username)
    if _user == None or not user.check_password(_user.password):
        return GenericResponse(status_code=status.HTTP_404_NOT_FOUND,message="Username or Password wrong!!")
    if not _user.is_active:
        return GenericResponse(status_code=status.HTTP_403_FORBIDDEN, message="Account Locked!!")
    token = create_jwt({"id":_user.id})
    

    return GenericResponse(data={"token":token}, cookies=[("token", token), ("username",_user.username)])


@route.delete("/logout")
async def logout():
    return GenericResponse(remove_cookies = ("token","username"))


@route.get('/users')
@auth_required
async def get_users(request: Request, token=None, skip: int = Query(0), limit: int = Query(500)):
    users = await User.find(User.id!=token).skip(skip).limit(limit).to_list()
    
    return GenericResponse(data=[{"id":user.id,"username":user.username} for user in users])


    


