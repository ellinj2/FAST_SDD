"""Initialize app."""
from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

import os

# Establish root directory
basedir = os.path.abspath(os.path.dirname(__file__))

# Initialize app and set config
app = Flask(__name__)
app.config["SECRET_KEY"] = "mysecretkey"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir, "data.sqlite")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["TEMP_DATA"] = os.path.join(basedir, "temp")

# Migrate database
db = SQLAlchemy(app)
Migrate(app, db)

# Handle login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "users.login"

# Bring in Blueprints
from FAST.core.views import core
# from FAST.error_pages.handlers import error_pages
from FAST.users.views import users
from FAST.calendar.views import calendar

# Register Blueprints
app.register_blueprint(core)
# app.register_blueprint(error_pages)
app.register_blueprint(users)
app.register_blueprint(calendar)

# Create database
from FAST.database import *

db.create_all()
