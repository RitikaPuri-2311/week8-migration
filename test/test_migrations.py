
import sys
import os

sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..")
    )
)

from app.database import engine

from sqlalchemy import inspect



def test_migrations():

    # Upgrade
    assert os.system(
        "alembic upgrade head"
    ) == 0

    inspector = inspect(engine)

    tables = inspector.get_table_names()

    assert "users" in tables
    assert "posts" in tables

    # Downgrade
    assert os.system(
        "alembic downgrade base"
    ) == 0

    inspector = inspect(engine)

    tables = inspector.get_table_names()

    assert "users" not in tables
