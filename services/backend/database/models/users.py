from beanie import Document, Indexed
from pydantic import  Field
from bson import ObjectId
from pymongo import IndexModel
import pymongo



class User(Document):
    id:str = Field(default_factory=lambda:str(ObjectId()))
    username:str
    password:str
    is_active:bool = True

    class Settings:
        name = "users"
        indexes = [
                    IndexModel(
                        [("username", pymongo.DESCENDING)],
                        name="username_string_index_DESCENDING",
                        unique=True
                    )
                  ]
        
