import redis.asyncio as redis

# Подключение к Redis
redis_client = redis.Redis(host="localhost", port=6379, decode_responses=True)
redis_client.setex("temp_key", 7200, "This will expire in 7200 seconds")


async def redis_set(key, value):
    await redis_client.set(key, value)

async def redis_get(key):
    return await redis_client.get(key)