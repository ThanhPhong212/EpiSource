import pytest
from shared.models.user_model import User

def test_login_api_returns_token(client, session):
    user = User(Name="Test User", Email="test@example.com")
    session.add(user)
    session.commit()

    res = client.post('/auth/login', json={'user_id': user.Id})
    assert res.status_code == 200

    data = res.get_json()
    assert "access_token" in data
    assert isinstance(data["access_token"], str)
    assert len(data["access_token"]) > 10

def test_login_api_invalid_user(client):
    res = client.post('/auth/login', json={'user_id': 9999})
    assert res.status_code == 404

    data = res.get_json()
    assert data["message"] == "User not found"

def test_logout_api_returns_message(client):
    res = client.get('/auth/logout')
    assert res.status_code == 200

    data = res.get_json()
    assert data["message"] == "Logged out"
