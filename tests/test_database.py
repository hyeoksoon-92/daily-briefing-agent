# tests/test_database.py
import inspect
import os
from unittest.mock import patch


def test_database_url_converts_to_async_format():
    with patch.dict(os.environ, {"DATABASE_URL": "postgresql://user:pass@host/db"}):
        import importlib
        import api.database as db_module
        importlib.reload(db_module)
        assert "asyncpg" in db_module.DATABASE_URL


def test_get_session_is_async_generator():
    from api.database import get_session
    assert inspect.isasyncgenfunction(get_session)
