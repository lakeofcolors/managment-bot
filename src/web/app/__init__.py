from flask import Flask, send_file, render_template
from app.core.config import BaseConfig
from app.core.extensions import db, migrate, ma, admin as admin_app
from app.api import bp as api
from app.admin import bp as admin_bp


def create_app(config=BaseConfig):
    app = Flask(__name__)
    app.config.from_object(config)

    db.init_app(app)
    migrate.init_app(app, db)
    ma.init_app(app)
    admin_app.init_app(app)

    app.register_blueprint(api)
    app.register_blueprint(admin_bp)
    return app


from app.core import models
