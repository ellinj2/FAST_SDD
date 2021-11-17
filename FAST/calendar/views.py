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
		notes = [[f.strip() for f in line.split(':')] for line in form.information.data.split('\n')]
		notes = {note[0]: ':'.join(note[1:]) for note in notes}
		print(notes)
		event = EventObject(tag=form.tag.data,
							start_time=notes["Start Time"],
					 		end_time=notes["End Time"])
		event.assign(**notes)
		event_entry = Event(name=event.tag,
							obj=event,
							user_id=current_user.id)

		db.session.add(event_entry)
		db.session.commit()
		form = EventForm()
		return redirect(url_for("users.view_events"))
	return render_template("upload_event.html", form=form)

@calendar.route('/download_calendar', methods=["GET", "POST"])
@login_required
def download_calendar():
	return render_template("download_calendar.html")

@calendar.route('/help')
def help():
	return redirect(url_for('calendar.upload_event'))

@calendar.route('/cluster/<int:calendar_id>', methods=["GET", "POST"])
@login_required
def cluster(calendar_id):
	form = ClusterForm()
	calendar = Calendar.query.get_or_404(calendar_id)
	form.attribute.choices = [(note, note) for note in calendar.object.notes.keys()]

	if form.validate_on_submit():
		# Assign defaults
		form.shift = (form.shift.data if form.shift else 1)
		form.start.data = (form.start.data if form.start else "earliest")
		form.centers.data = (form.centers.data if form.centers else -1)
		calendar.object.cluster(attribute=form.attribute.data,
								shift=form.shift.data,
								start=form.start.data,
								centers=form.centers.data)

		return redirect(url_for("users.view_calendar", calendar_id=calendar_id))

	return render_template("cluster_calendar.html", form=form, calendar=calendar)
