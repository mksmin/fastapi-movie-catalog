from redis import Redis
from core import config

redis = Redis(
    host=config.REDIS_HOST,
    port=config.REDIS_PORT,
    db=config.REDIS_TOKENS_DB,
    decode_responses=True,
)
