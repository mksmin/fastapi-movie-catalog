import logging
from os import getenv
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
USER_DATA_STORAGE_FILEPATH = BASE_DIR / "user_data.json"


LOG_LEVEL = logging.INFO
LOG_FORMAT: str = (
    "[%(asctime)s.%(msecs)03d] %(module)10s:%(lineno)-3d %(levelname)-7s - %(message)s"
)

REDIS_HOST = "localhost"
REDIS_PORT = int(getenv("REDIS_PORT", 0)) or 6379
REDIS_DB = 0
REDIS_TOKENS_DB = 1
REDIS_USERS_DB = 2
REDIS_MOVIE_DB = 3

REDIS_API_TOKENS_SET_NAME = "tokens"
REDIS_MOVIE_HASH_NAME = "movies"
