from urllib.parse import urlparse

from motor.motor_asyncio import AsyncIOMotorClient

from .. import DATABASE_URI
from .base import has_reinitialize, normalize_uri

DATABASE_NAME = urlparse(DATABASE_URI).path.lstrip('/')
POKEMON_COLLECTION_NAME = 'pokemon'
TRAINER_COLLECTION_NAME = 'trainer'

AsyncMongoDBEngine = AsyncIOMotorClient(normalize_uri(DATABASE_URI))


async def initialize_mongo_db():
    if has_reinitialize(DATABASE_URI):
        await AsyncMongoDBEngine.drop_database(AsyncMongoDBEngine.get_default_database().name)

    db = AsyncMongoDBEngine[DATABASE_NAME]

    pokemon_collection = db[POKEMON_COLLECTION_NAME]
    await pokemon_collection.create_index([('no', 1)], unique=True)

    trainer_collection = db[TRAINER_COLLECTION_NAME]
    await trainer_collection.create_index([('id', 1)], unique=True)
