from os import environ
from pathlib import Path
from flask import Flask

from todo.models import db


def create_app(config_overrides=None):
    app = Flask(__name__, instance_relative_config=True)

    Path(app.instance_path).mkdir(parents=True, exist_ok=True)

    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db_path = Path(app.instance_path) / "db.sqlite"
    app.config["SQLALCHEMY_DATABASE_URI"] = environ.get(
        "SQLALCHEMY_DATABASE_URI",
        f"sqlite:///{db_path}"
    )

    if config_overrides:
        app.config.update(config_overrides)

    db.init_app(app)

    with app.app_context():
        from todo.models.todo import Todo  # noqa: F401
        db.create_all()

    from .views.routes import api
    app.register_blueprint(api)

    return app
