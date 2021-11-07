from flask import render_template, Blueprint, redirect, url_for
from flask_login import current_user, login_required, logout_user
from FAST import app
from FAST.calendar.forms import *
from FAST.calendar.models import *
from FAST.database import *

calendar = Blueprint("calendar", __name__)

@calendar.route('/upload_event', methods=["GET", "POST"])
@login_required
def upload_event():
	form = EventForm()

	if form.validate_on_submit():
		event = EventObject(tag=form.tag.data)
		notes = [[f.strip() for f in line.split(':')] for lin in form.information.data.split('\n')]
		event.assign({note[0]: ':'.join(note[1:]) for note in notes})
		event_entry = Event(name=event.tag,
							obj=event,
							user_id=current_user.id)

		db.session.add(event_entry)
		db.session.commit()
		form = EventForm()
		return redirect(url_for("users.view_events"))
	return render_template("upload_event.html", form=form)

@calendar.route('/generate_claendar', methods=["GET", "POST"])
@login_required
def generate_calendar():
	return render_template("generate_calendar.html")

@calendar.route('/download_calendar', methods=["GET", "POST"])
@login_required
def download_calendar():
	return render_template("download_calendar.html")

@calendar.route('/help')
def help():
	return redirect(url_for('calendar.upload_event'))
