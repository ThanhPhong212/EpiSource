import pytest
from flask import Flask
from shared.db import db
from shared.models.user_model import User  # Import model cụ thể (tránh wildcard)
from web_app.routes.auth_routes import auth_bp
from web_app.routes.post_routes import post_bp
import os

# --- App setup fixture ---
@pytest.fixture(scope="session")
def app():
    # Tìm đường dẫn tuyệt đối đến thư mục chứa `templates/`
    base_dir = os.path.abspath(os.path.dirname(__file__))
    template_dir = os.path.join(base_dir, "../templates")

    app = Flask(__name__, template_folder=template_dir)
    app.secret_key = "test-secret-key"
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    app.register_blueprint(auth_bp)
    app.register_blueprint(post_bp)

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

# --- Test client fixture ---
@pytest.fixture
def client(app):
    return app.test_client()

# --- Session fixture (có rollback) ---
@pytest.fixture
def session(app):
    with app.app_context():
        db.drop_all()
        db.create_all() 
        yield db.session
        db.session.rollback()

# --- Mock repository + seed data ---
@pytest.fixture
def mock_user_repo(session):
    user1 = User(Name="User 1", Email="user1@test.com")
    user2 = User(Name="User 2", Email="user2@test.com")
    session.add_all([user1, user2])
    session.commit()

    from shared.repository.user_repository import UserRepository
    return UserRepository(session)
