import os
from unittest import TestCase

from api.api_v1.auth.services import redis_tokens

print(  # noqa: T201
    "ENV REDIS HOST",
    os.getenv("URL_SHORTENER__REDIS__CONNECTION__HOST", "LALALALa"),
)


class RedisTokensHelperTestCase(TestCase):
    def test_generate_and_save_token(self) -> None:
        new_token = redis_tokens.generate_and_save_token()
        self.assertTrue(
            redis_tokens.token_exists(new_token),
        )
