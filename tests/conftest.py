import pytest
from app.db_init import init_db


@pytest.fixture(scope="session", autouse=True)
def _bootstrap_db():
    init_db()
