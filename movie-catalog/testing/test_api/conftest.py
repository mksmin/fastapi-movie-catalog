from collections.abc import Generator

import pytest
from starlette.testclient import TestClient

from main import app


@pytest.fixture()
def client() -> Generator[TestClient, None, None]:
    with TestClient(app) as client:
        yield client
