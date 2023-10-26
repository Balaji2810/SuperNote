from pydantic import BaseModel, validator
import bcrypt
from typing import Any
from fastapi import status
from fastapi.responses import JSONResponse
from datetime import datetime



class GenericResponse(BaseModel):
    data: Any = None
    message: str = "Success"

def GenericResponse(data:Any=None, message:str="Success", status_code=status.HTTP_200_OK, cookies=None, 
                    remove_cookies=None):
    res = JSONResponse(status_code=status_code,content={"message":message, "data":data})
    if cookies:
        [res.set_cookie(key=data[0], value=data[1]) for data in cookies]
    
    if remove_cookies:
        [res.delete_cookie(key) for key in remove_cookies]

    return res


class User(BaseModel):
    username:str
    password:str

    def hash_password(self):
        salt = bcrypt.gensalt()
        hash = bcrypt.hashpw(self.password.encode(), salt)
        return hash

    def check_password(self, hash):
        return bcrypt.checkpw(self.password.encode(), hash.encode())


class  Note(BaseModel):
    name:str

class NoteProject(BaseModel):
    owner_id:str
    name:str
    created:datetime

    @validator("created")
    def datetime_to_str(cls, value):
        return str(value)


class ShareNote(BaseModel):
    user_id:str
    note_id:str


class HtmlData(BaseModel):
    data:str