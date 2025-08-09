from typing import Iterable, cast

from redis import Redis

from api.api_v1.auth.services.tokens_helper import TokensHelper
from core import config


class RedisTokensHelper(TokensHelper):
    def __init__(
        self,
        host: str,
        port: int,
        db: int,
        tokens_set_name: str,
    ) -> None:
        self.redis = Redis(
            host=host,
            port=port,
            db=db,
            decode_responses=True,
        )
        self.tokens_set_name = tokens_set_name

    def token_exists(self, token: str) -> bool:
        return bool(
            self.redis.sismember(
                self.tokens_set_name,
                token,
            )
        )

    def add_token(self, token: str) -> None:
        self.redis.sadd(
            self.tokens_set_name,
            token,
        )

    def get_tokens(self) -> list[str]:
        return list(
            cast(
                Iterable[str],
                self.redis.smembers(self.tokens_set_name),
            )
        )

    def delete_token(self, token: str) -> None:
        self.redis.srem(self.tokens_set_name, token)


redis_tokens = RedisTokensHelper(
    host=config.REDIS_HOST,
    port=config.REDIS_PORT,
    db=config.REDIS_TOKENS_DB,
    tokens_set_name=config.REDIS_API_TOKENS_SET_NAME,
)
