import os
import pytest
from flask import Flask, jsonify
from shared.db import db
from flask_jwt_extended import JWTManager
from web_app.routes.auth_routes import api as auth_ns
from web_app.routes.post_routes import api as post_ns
from flask_restx import Api
from flask_jwt_extended import JWTManager, exceptions

@pytest.fixture(scope="session")
def app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "test-secret"
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY", "test-secret")
    app.config['PROPAGATE_EXCEPTIONS'] = True
    db.init_app(app)
    jwt = JWTManager(app)

    api = Api(app, doc=False)
    api.add_namespace(auth_ns)
    api.add_namespace(post_ns)

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def session(app):
    with app.app_context():
        db.drop_all()
        db.create_all()
        yield db.session
        db.session.rollback()

@pytest.fixture
def access_token(app):
    from flask_jwt_extended import create_access_token
    with app.app_context():
        return create_access_token(identity=str(1))
