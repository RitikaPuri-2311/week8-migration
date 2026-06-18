from sqlalchemy import inspect
from app.database import engine


def test_migrations():
    inspector = inspect(engine)
    tables = inspector.get_table_names()

    assert "users" in tables
    assert "posts" in tables