from flask import render_template, Blueprint, redirect, url_for, request
from flask_login import login_user, current_user, login_required, logout_user
from FAST import app, db
from FAST.users.forms import *
from FAST.database import *

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

@users.route("/view_events", methods=["GET"])
@login_required
def view_events():
    events = Event.query.filter_by(user_id=current_user.id).order_by(Event.name.asc()).all()
    print(events[0].obj.start_time, events[0].obj.end_time)
    return render_template("view_events.html", events=events, len=len(events))

@users.route('/generate_calendar', methods=["GET", "POST"])
@login_required
def generate_calendar():
    form = CalendarForm()

    if form.validate_on_submit():
        times = form.timeslots.data
        times = [line.strip() for line in times.strip().split('\n')]
        calendar = CalendarObject(tag=form.name.data, time_slots=times)
        events = [event.obj for event in Event.query.filter_by(user_id=current_user.id).all()]
        if form.heuristic.data == "rand":
            calendar.randomAssign(events)
        elif form.heuristic.data == "start":
            calendar.startTimeAssign(events)
        calendar.load(events)
        calendar_entry = Calendar(user_id=current_user.id,
                                  name=form.name.data,
                                  obj=calendar)

        db.session.add(calendar_entry)
        db.session.commit()

        return redirect(url_for("users.view_calendar", calendar_id=calendar_entry.id))
        
    return render_template("generate_calendar.html", form=form)

@users.route('/view_calendar/<int:calendar_id>', methods=["GET"])
@login_required
def view_calendar(calendar_id):
    calendar = Calendar.query.get_or_404(calendar_id)
    return render_template("view_calendar.html", calendar=calendar)
