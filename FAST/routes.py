from flask import render_template
from flask_login import current_user, login_required, logout_user
from __main__ import app

#main = Blueprint('main', __name__)

@app.route('/')
def index():
    return render_template('index.html')

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