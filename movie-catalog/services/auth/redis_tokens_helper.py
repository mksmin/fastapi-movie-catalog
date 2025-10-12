from collections.abc import Iterable
from typing import cast

from redis import Redis

from core.config import settings
from services.auth.tokens_helper import TokensHelper


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
            ),
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
            ),
        )

    def delete_token(self, token: str) -> None:
        self.redis.srem(self.tokens_set_name, token)


redis_tokens = RedisTokensHelper(
    host=settings.redis.connection.host,
    port=settings.redis.connection.port,
    db=settings.redis.db.tokens,
    tokens_set_name=settings.redis.collections_names.tokens_set,
)
