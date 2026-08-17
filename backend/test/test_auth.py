from fastapi.testclient import TestClient
import pytest
from app.main import app

client = TestClient(app)

@pytest.fixture(scope="function")
def registered_user(db_session):
    """Registers a user through the API endpoint so they exist for login tests."""
    client = TestClient(app)
    
    registration_payload = {
        "email": "test@example.com",
        "username": "testuser",
        "password": "test12345"
    }
    
    
    response = client.post("/api/v1/auth/register", json=registration_payload)
    assert response.status_code in [200, 201]
    return registration_payload
    
def test_login_success(db_session, registered_user):
    """Test successful login with correct credentials.

    The db_session fixture automatically handles isolation.
    """
    
    response = client.post(
        "/api/v1/auth/login",
        data={"username": registered_user["email"], "password": registered_user["password"]}    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_login_wrong_password(db_session, registered_user):
    """Test login failure due to bad password."""
    response = client.post(
        "/api/v1/auth/login",
        data={"username": registered_user["email"], "password": "wrongPassword"}
                )
    assert response.status_code == 401
    assert response.json()["detail"] == "Incorrect email or password"
