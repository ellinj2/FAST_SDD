"""Initialize app."""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_session import Session

import os

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config["SECTET_KEY"] = "mysecretkey"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir, "data.sqlite")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy()
Migrate(app, db)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "users.login"

def create_app():
    """Construct the core app object."""
    app = Flask(__name__, instance_relative_config=False)

    # Application Configuration
    # app.config.from_object('config.Config')

    # Initialize Plugins
    db.init_app(app)
    login_manager.init_app(app)

    with app.app_context():
        # from . import routes
        # from . import auth
        # from .assets import compile_assets

        # # Register Blueprints
        # app.register_blueprint(routes.main_bp)
        # app.register_blueprint(auth.auth_bp)

        # Create Database Models
        db.create_all()

        # Compile static assets
        # if app.config['FLASK_ENV'] == 'development':
        #     compile_assets(app)

        return app

from FLASK.core.views import core
from FLASK.error_pages.handlers import error_pages
from FLASK.users.views import users
from FLASK.calendars.views import calendars

app.register_blueprint(core)
app.register_blueprint(error_pages)
app.register_blueprint(users)
app.register_blueprint(calendars)
