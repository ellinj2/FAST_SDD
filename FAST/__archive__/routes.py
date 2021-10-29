from flask import render_template
from flask_login import current_user, login_required, logout_user
from FAST import app
from forms import *

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

@app.route('/upload_data')
# @login_required
def upload_data():
    form = DataUploadForm()
    if form.validate_on_submit():
        print("Attempting to upload Schedule:\nTitle = {}\nContent = {}\n".format(
            form.data.data.title, form.data.data.content
            ))
    return render_template("upload_data.html", form=form)
