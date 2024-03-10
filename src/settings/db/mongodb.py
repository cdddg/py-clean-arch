from urllib.parse import urlparse

from motor.motor_asyncio import AsyncIOMotorClient

from .. import DATABASE_URI
from .base import normalize_uri, should_reinitialize

DATABASE_NAME = urlparse(DATABASE_URI).path.lstrip('/')
COLLECTION_NAME = 'pokemon'

AsyncMongoDBEngine = AsyncIOMotorClient(normalize_uri(DATABASE_URI))


async def initialize_mongo_db(**kwargs):
    if should_reinitialize(DATABASE_URI):
        await AsyncMongoDBEngine.drop_database(AsyncMongoDBEngine.get_default_database().name)
