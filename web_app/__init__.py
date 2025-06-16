import os
import pkgutil
import importlib
from flask import Flask, jsonify
from config import Config
from shared.db import db
from flask_restx import Api
from flask_restx import Namespace
from flask_jwt_extended import JWTManager
from flask_jwt_extended.exceptions import NoAuthorizationError

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")

    db.init_app(app)
    jwt = JWTManager(app)
    api = Api(app, title="Swagger", version="1.0", doc="/docs")

    @jwt.unauthorized_loader
    def unauthorized_response(callback):
        return jsonify({
            "status": "error",
            "message": "Missing Authorization Header"
        }), 401

    @jwt.invalid_token_loader
    def invalid_token_response(callback):
        return jsonify({
            "status": "error",
            "message": "Invalid token"
        }), 422

    @jwt.expired_token_loader
    def expired_token_response(jwt_header, jwt_payload):
        return jsonify({
            "status": "error",
            "message": "Token has expired"
        }), 401

    @app.errorhandler(NoAuthorizationError)
    def handle_no_auth_error_global(error):
        return jsonify({"status": "error", "message": "Missing Authorization Header"}), 401

    register_blueprints(api)

    return app

def register_blueprints(api):
    from web_app import routes
    package_dir = routes.__path__

    for _, module_name, _ in pkgutil.iter_modules(package_dir):
        try:
            module = importlib.import_module(f"web_app.routes.{module_name}")
            for item_name in dir(module):
                item = getattr(module, item_name)
                if isinstance(item, Namespace):
                    api.add_namespace(item)
        except Exception as e:
            print(f"Error loading {module_name}: {e}")
