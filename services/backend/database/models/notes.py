from beanie import Document, Indexed
from pydantic import BaseModel, Field
from typing import List
from datetime import datetime, date
import pymongo
from bson import ObjectId
from typing import Optional
from constants import StatusEnum
from pymongo import IndexModel


class Note(Document):
    id:str = Field(default_factory=lambda:str(ObjectId()))
    owner_id:str
    name:str
    created:datetime = Field(default_factory=datetime.now)


    class Settings:
        name = "notes"
        indexes = [
            IndexModel(
                [("owner_id", pymongo.DESCENDING),("name", pymongo.DESCENDING)],
                name="note_name_index_DESCENDING", unique=True
            )
        ]
