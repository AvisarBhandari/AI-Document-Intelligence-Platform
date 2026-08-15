from fastapi.testclient import TestClient
import pytest
from app.main import app

client = TestClient(app)

def test_login_success():
    """Test successful login with correct credentials. """
    responce = client.post("/api/v1/auth/login",
                           data={"username": "test@example.com", "password": "test12345"}
                           )
    assert responce.status_code == 200
    data = responce.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_login_wrong_password():
    """Test login failure due to bad password."""
    responce = client.post("/api/v1/auth/login",
                           data={"username": "test@example.com", "password": "wrongPassword"}
                           )
    assert responce.status_code == 401
    assert responce.json()["detail"] == "Incorrect email or password"

def test_login_missing_fields():
    """Test login failure when fields are missing."""
    responce = client.post("/api/v1/auth/login",
                           data={"username": "test@example.com"}
                           )
    assert responce.status_code == 422