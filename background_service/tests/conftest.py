import os
import pytest
from flask import Flask
from shared.db import db

@pytest.fixture(scope="session")
def app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.secret_key = "test-worker"

    db.init_app(app)

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def session(app):
    with app.app_context():
        db.drop_all()
        db.create_all()
        yield db.session
        db.session.rollback()
