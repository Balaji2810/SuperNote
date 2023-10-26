from beanie import Document, Indexed
from pydantic import BaseModel, Field
from typing import List
from datetime import datetime, date
import pymongo
from bson import ObjectId
from typing import Optional
from constants import StatusEnum
from pymongo import IndexModel


class SharedNote(Document):
    id:str = Field(default_factory=lambda:str(ObjectId()))
    note_id:str
    owner_id:str
    shared_with:str
    created:datetime = Field(default_factory=datetime.now)


    class Settings:
        name = "sharednotes"
        indexes = [
            IndexModel(
                [("note_id", pymongo.DESCENDING),("shared_with", pymongo.DESCENDING)],
                name="note_shared_name_index_DESCENDING", unique=True
            ),
            IndexModel(
                [("shared_with", pymongo.DESCENDING)],
                name="shared_with_index_DESCENDING"
            ),
            IndexModel(
                [("owner_id", pymongo.DESCENDING)],
                name="owner_id_index_DESCENDING"
            )
        ]
