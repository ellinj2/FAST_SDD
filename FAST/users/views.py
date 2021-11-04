from flask import render_template, Blueprint, redirect, url_for
from flask_login import current_user, login_required, logout_user
from FAST import app
from FAST.users.forms import *

users = Blueprint("users", __name__)

""" User homepage / dashboard """
@users.route('/dashboard', methods =['GET'])
@login_required
def dashboard():
    return render_template('dashboard.html')

@users.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))

@users.route('/register')
def register():
    form = SignupForm()
    return render_template("register.html", form=form)

@users.route('/login')
def login():
    form = LoginForm()
    return render_template("login.html", form=form)
