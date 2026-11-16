"""
Pytest Configuration & Fixtures
Provides test database session, test client, and test user fixtures.
"""

import os
import pytest
from unittest.mock import patch

# Set test environment before any imports
os.environ.setdefault("DATABASE_URL", "sqlite:///./test.db")
os.environ.setdefault("JWT_SECRET_KEY", "test-secret-key-for-pytest-only")
os.environ.setdefault("FRONTEND_URL", "http://localhost:3000")
os.environ.setdefault("ALLOWED_ORIGINS", "http://localhost:3000")

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

from database import Base


# Use in-memory SQLite for tests
TEST_DATABASE_URL = "sqlite:///./test.db"
test_engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
)
TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


@pytest.fixture(scope="session", autouse=True)
def create_test_tables():
    """Create all tables once for the test session."""
    # Import models so they register with Base
    from models import user, game_session, friendship  # noqa: F401
    from models import notification, character, scenario, analytics  # noqa: F401
    Base.metadata.create_all(bind=test_engine)
    yield
    Base.metadata.drop_all(bind=test_engine)
    # Clean up test database file
    if os.path.exists("./test.db"):
        os.remove("./test.db")


@pytest.fixture()
def db_session():
    """Provide a transactional database session for each test."""
    session = TestSessionLocal()
    try:
        yield session
    finally:
        session.rollback()
        session.close()


@pytest.fixture()
def client(db_session):
    """FastAPI test client with overridden DB dependency."""
    from main import app
    from database import get_db

    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture()
def test_user(db_session):
    """Create a test user and return user data with credentials."""
    from models.user import User
    import bcrypt

    user = User(
        email="test@example.com",
        username="testuser",
        nickname="TestNick",
        hashed_password=bcrypt.hashpw(b"TestPassword123!", bcrypt.gensalt()).decode('utf-8'),
        credits=100,
        is_active=True,
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    return {
        "user": user,
        "username": "testuser",
        "password": "TestPassword123!",
        "email": "test@example.com",
    }


@pytest.fixture()
def auth_headers(client, test_user):
    """Get authentication headers for a test user."""
    response = client.post(
        "/api/auth/login",
        json={
            "username": test_user["username"],
            "password": test_user["password"],
        },
    )
    if response.status_code == 200:
        token = response.json()["access_token"]
        return {"Authorization": f"Bearer {token}"}
    # If login fails, return empty headers (test should handle)
    return {}
