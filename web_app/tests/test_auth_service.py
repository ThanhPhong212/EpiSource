import pytest
from flask import Flask, session
from web_app.services.auth_service import AuthService

class DummyUserRepository:
    def get_by_id(self, user_id):
        return {'Id': user_id, 'Name': 'Test User'}

@pytest.fixture
def app():
    app = Flask(__name__)
    app.secret_key = 'test-secret'

    # Gán endpoint để khớp với AuthService
    @app.route('/posts', endpoint='post.index')
    def post_index():
        return 'Post Index'

    @app.route('/auth/login', endpoint='auth.login')
    def login():
        return 'Login Page'

    return app

@pytest.fixture
def client(app):
    return app.test_client()

def test_login_redirect_sets_session(client, app):
    with app.test_request_context():
        auth_service = AuthService(DummyUserRepository())
        response = auth_service.login(10)

        assert response.status_code == 302
        assert response.location.endswith('/posts')

        with client.session_transaction() as sess:
            sess['user_id'] = 10
            assert sess['user_id'] == 10

def test_logout_redirect_clears_session(client, app):
    with app.test_request_context():
        auth_service = AuthService(DummyUserRepository())
        session['user_id'] = 10
        response = auth_service.logout()

        assert response.status_code == 302
        assert response.location.endswith('/auth/login')
