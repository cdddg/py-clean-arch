from redis.asyncio import Redis as AsyncRedis
from redis.exceptions import ConnectionError as RedisConnectionError

from .. import DATABASE_URI
from .base import has_reinitialize, normalize_uri

CHUNK_SIZE = 5000


async_redis = AsyncRedis.from_url(
    normalize_uri(DATABASE_URI),
    encoding='utf-8',
    decode_responses=True,
    retry_on_error=[RedisConnectionError],
)


async def initialize_redis():
    if has_reinitialize(DATABASE_URI):
        async with async_redis.client() as client:
            cursor = '0'
            while cursor != 0:
                cursor, keys = await client.scan(cursor=int(cursor), match='*', count=CHUNK_SIZE)
                if keys:
                    await client.delete(*keys)


def get_async_redis_client() -> AsyncRedis:
    return async_redis.client()
