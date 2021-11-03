from flask import render_template, Blueprint
from flask_login import current_user, login_required, logout_user
from FAST import app

calendar = Blueprint("calendar", __name__)
