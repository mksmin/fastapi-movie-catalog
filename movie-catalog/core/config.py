import logging
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
USER_DATA_STORAGE_DIR = BASE_DIR / "data_storage"
USER_DATA_STORAGE_FILEPATH = USER_DATA_STORAGE_DIR / "user_data.json"

if not USER_DATA_STORAGE_DIR.exists():
    USER_DATA_STORAGE_DIR.mkdir()

LOG_LEVEL = logging.INFO
LOG_FORMAT: str = (
    "[%(asctime)s.%(msecs)03d] %(module)10s:%(lineno)-3d %(levelname)-7s - %(message)s"
)

REDIS_HOST = "localhost"
REDIS_PORT = 6379
REDIS_DB = 0
REDIS_TOKENS_DB = 1
REDIS_USERS_DB = 2

REDIS_API_TOKENS_SET_NAME = "tokens"
