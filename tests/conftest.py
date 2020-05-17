import pytest
from alembic.config import main
from starlette.config import environ
from starlette.testclient import TestClient

environ["TESTING"] = "TRUE"


@pytest.fixture
def client():
    from gino_fastapi_demo.main import db, get_app

    main(["--raiseerr", "upgrade", "head"])

    with TestClient(get_app()) as _client:
        yield _client

    main(["--raiseerr", "downgrade", "base"])
