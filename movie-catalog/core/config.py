from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
USER_DATA_STORAGE_DIR = BASE_DIR / "data_storage"

if not USER_DATA_STORAGE_DIR.exists():
    USER_DATA_STORAGE_DIR.mkdir()
