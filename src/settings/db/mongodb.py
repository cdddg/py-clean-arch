from urllib.parse import urlparse

from motor.motor_asyncio import AsyncIOMotorClient

from .. import DATABASE_URI
from .base import has_reinitialize, normalize_uri

DATABASE_NAME = urlparse(DATABASE_URI).path.lstrip('/')
COLLECTION_NAME = 'pokemon'

AsyncMongoDBEngine = AsyncIOMotorClient(normalize_uri(DATABASE_URI))


async def initialize_mongo_db():
    if has_reinitialize(DATABASE_URI):
        await AsyncMongoDBEngine.drop_database(AsyncMongoDBEngine.get_default_database().name)

    db = AsyncMongoDBEngine[DATABASE_NAME]
    collection = db[COLLECTION_NAME]
    await collection.create_index([('no', 1)], unique=True)
