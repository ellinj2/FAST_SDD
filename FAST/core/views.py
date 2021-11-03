from flask import render_template, Blueprint
from flask_login import current_user, login_required, logout_user
from FAST import app

core = Blueprint("core", __name__)

@app.route('/')
def index():
    return render_template('index.html')
