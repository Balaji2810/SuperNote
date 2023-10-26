from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from .models import  Note, User, SharedNote
import os


MONGODB_URI = os.environ["MONGODB_URI"]


async def mongo_init():
    # Beanie uses Motor async client under the hood 
    client = AsyncIOMotorClient(MONGODB_URI)

    # Initialize beanie with the Product document class
    await init_beanie(database=client.db_name, document_models=[Note, User, SharedNote])

