from flask import render_template, Blueprint
from flask_login import current_user, login_required, logout_user
from FAST import app

users = Blueprint("users", __name__)

""" User homepage / dashboard """
@app.route('/dashboard', methods =['GET'])
@login_required
def dashboard():
    return render_template('dashboard.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
