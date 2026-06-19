import pytest
from fastapi.testclient import TestClient
from main import app
import uuid

client = TestClient(app)

email = f"test_{uuid.uuid4()}@example.com"


def test_register_success():
    response = client.post(
        "/auth/register",
        json={
            "name": "Test User",
            "email": "test@example.com",
            "password": "test123"
        }
    )

    assert response.status_code == 200
    assert response.json()["email"] == "test@example.com"


def test_register_duplicate_email():
    client.post(
        "/auth/register",
        json={
            "name": "Test User",
            "email": "dup@example.com",
            "password": "test123"
        }
    )

    response = client.post(
        "/auth/register",
        json={
            "name": "Test User",
            "email": "dup@example.com",
            "password": "test123"
        }
    )

    assert response.status_code in [400, 409]


def test_login_success():
    client.post(
        "/auth/register",
        json={
            "name": "Login User",
            "email": "login@example.com",
            "password": "test123"
        }
    )

    response = client.post(
        "/auth/login",
        data={
            "username": "login@example.com",
            "password": "test123"
        }
    )

    assert response.status_code == 200
    assert "access_token" in response.json()


def test_login_wrong_password():
    client.post(
        "/auth/register",
        json={
            "name": "Wrong Pass",
            "email": "wrong@example.com",
            "password": "test123"
        }
    )

    response = client.post(
        "/auth/login",
        data={
            "username": "wrong@example.com",
            "password": "wrongpass"
        }
    )

    assert response.status_code == 401


def test_protected_route_valid_token():
    client.post(
        "/auth/register",
        json={
            "name": "Protected",
            "email": "prot@example.com",
            "password": "test123"
        }
    )

    login = client.post(
        "/auth/login",
        data={
            "username": "prot@example.com",
            "password": "test123"
        }
    )

    token = login.json()["access_token"]

    response = client.get(
        "/users/me",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 200


def test_protected_route_no_token():
    response = client.get("/users/me")

    assert response.status_code == 401


def test_expired_token():
    fake_token = (
        "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9."
        "invalid.signature"
    )

    response = client.get(
        "/users/me",
        headers={
            "Authorization": f"Bearer {fake_token}"
        }
    )

    assert response.status_code == 401


def test_admin_route_with_scope():
    login = client.post(
        "/auth/login",
        data={
            "username": "admin@gmail.com",
            "password": "admin123"
        }
    )

    token = login.json()["access_token"]

    response = client.get(
        "/users/admin",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 200


def test_admin_route_without_token():
    response = client.get("/users/admin")

    assert response.status_code == 401