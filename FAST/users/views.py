from flask import render_template, Blueprint, redirect, url_for
from flask_login import login_user, current_user, login_required, logout_user
from FAST import app, db
from FAST.users.forms import *
from FAST.database import User

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

@users.route('/register', methods=["GET", "POST"])
def register():
    form = SignupForm()

    if form.validate_on_submit():
        print(f"Registering {form.email.data}\n{form.password.data}")
        user = User(email=form.email.data,
                    password=form.password.data)

        db.session.add(user)
        db.session.commit()

        login_user(user)
        
        return redirect(url_for('index'))
    return render_template("register.html", form=form)

@users.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()
    return render_template("login.html", form=form)
