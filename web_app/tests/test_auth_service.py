from web_app.services.auth_service import AuthService
from shared.models.user_model import User
from shared.repository.user_repository import UserRepository

def test_login_returns_token(app, session):
    user = User(Name="Tester", Email="test@example.com")
    session.add(user)
    session.commit()

    repo = UserRepository(session)
    service = AuthService(repo)

    with app.app_context():
        response, status_code = service.login(user.Id)
        assert isinstance(response, dict)
        assert status_code == 200

def test_logout_returns_message(app):
    repo = UserRepository(None)
    service = AuthService(repo)

    with app.app_context():
        response, status_code = service.logout()
        assert response["message"] == "Logged out"
        assert status_code == 200
