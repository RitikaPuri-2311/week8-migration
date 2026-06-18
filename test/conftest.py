import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from fastapi.testclient import TestClient

from main import app
from app.database import Base, get_db


# -----------------------------
# TEST DATABASE (SQLite)
# -----------------------------
TEST_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False}
)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


# -----------------------------
# OVERRIDE DB DEPENDENCY
# -----------------------------
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


# -----------------------------
# CREATE TABLES ONCE
# -----------------------------
@pytest.fixture(scope="session", autouse=True)
def setup_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


# -----------------------------
# TEST CLIENT
# -----------------------------
@pytest.fixture()
def client():
    return TestClient(app)


# -----------------------------
# CLEAN DATABASE BETWEEN TESTS
# -----------------------------
@pytest.fixture(autouse=True)
def clean_db():
    connection = engine.connect()
    transaction = connection.begin()

    TestingSessionLocal.configure(bind=connection)

    yield

    transaction.rollback()
    connection.close()