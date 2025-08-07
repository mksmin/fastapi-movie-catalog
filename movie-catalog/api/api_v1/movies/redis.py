import secrets
from abc import ABC, abstractmethod

from redis import Redis
from core import config


class TokensHelper(ABC):
    @abstractmethod
    def token_exists(self, token: str) -> bool:
        pass

    @abstractmethod
    def add_token(self, token: str) -> None:
        pass

    @classmethod
    def generate_token(cls) -> str:
        return secrets.token_urlsafe(16)

    def generate_and_add_token(self) -> str:
        token = self.generate_token()
        self.add_token(token)
        return token


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


redis_tokens = RedisTokensHelper(
    host=config.REDIS_HOST,
    port=config.REDIS_PORT,
    db=config.REDIS_TOKENS_DB,
    tokens_set_name=config.REDIS_API_TOKENS_SET_NAME,
)
