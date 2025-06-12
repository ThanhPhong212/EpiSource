import pkgutil
import importlib
from flask import Flask
from config import Config
from shared.db import db
from flask import Blueprint


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)

    register_blueprints(app)

    return app


def register_blueprints(app):
    from web_app import routes
    package_dir = routes.__path__

    for _, module_name, _ in pkgutil.iter_modules(package_dir):
        module = importlib.import_module(f"web_app.routes.{module_name}")
        for item_name in dir(module):
            item = getattr(module, item_name)
            if isinstance(item, Blueprint):
                app.register_blueprint(item)
