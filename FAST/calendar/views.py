from flask import render_template, Blueprint, redirect, url_for, request, flash
from FAST.forms import DataUploadForm
from flask_login import current_user, login_required, logout_user
from FAST import app
from FAST.calendar.forms import *
from FAST.calendar.models import *
from FAST.database import *
from werkzeug.utils import secure_filename
import os
import json
from sqlalchemy.orm.attributes import flag_modified

# Registered Blueprint
calendar = Blueprint("calendar", __name__)

@calendar.route('/upload_event', methods=["GET", "POST"])
@login_required
def upload_event():
	"""
	Route to handle generation of a new Event
	"""
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
	"""
	TO-DO : Implement downloading data
	"""
	return render_template("download_calendar.html")

@calendar.route('/help')
def help():
	"""
	TO-DO : Implement help dashboard
	"""
	return redirect(url_for('calendar.upload_event'))

@calendar.route('/upload_file', methods=["GET", "POST"])
@login_required
def upload_file():
	"""
	Route to handle uploading a file to generate Events
	"""
	form = UploadForm()
	if form.validate_on_submit():
		file = form.file.data
		json_data = json.loads(file.read())
		for event_data in json_data["Events"]:
			event = EventObject(
					tag=event_data["Name"],
					start_time=event_data["Start Time"],
					end_time=event_data["End Time"]
				)
			event.assign(**{key: event_data[key] for key in event_data if key not in ["Start Time", "End Time"]})
			event_entry = Event(
					name=event.tag,
					obj=event,
					user_id=current_user.id
				)
			db.session.add(event_entry)
			db.session.commit()

		return redirect(url_for("users.view_events"))

	return render_template("upload_file.html", form=form)

@calendar.route('/cluster/<int:calendar_id>', methods=["GET", "POST"])
@login_required
def cluster(calendar_id):
	"""
	Route to handle clustering a Calendar

	Inputs:
	- calendar_id : Int unique identifier for a Calendar entry in the database
	"""
	form = ClusterForm()
	calendar = Calendar.query.get_or_404(calendar_id)
	notes = set([note for events in calendar.obj.events.values()
					for event in events
					for note in event.notes.keys()])
	form.attribute.choices = [(note, note) for note in sorted(notes)]
	form.start.choices = [(option, option) for option in sorted(CalendarObject.KNOWN_START_BEHAVIOR)]

	if form.validate_on_submit():
		# Assign defaults
		shift = (form.shift.data if form.shift else 1)
		start = (form.start.data if form.start else "earliest")
		centers = (form.centers.data if form.centers else -1)
		obj_ = calendar.obj
		obj_.cluster(attribute=form.attribute.data,
								shift=shift,
								start=start,
								centers=centers)
		flag_modified(calendar, 'obj')
		db.session.commit()

		return redirect(url_for("users.view_calendar", calendar_id=calendar_id))

	return render_template("cluster_calendar.html", form=form, calendar=calendar.obj)

@calendar.route('/anti-cluster/<int:calendar_id>', methods=["GET", "POST"])
@login_required
def antiCluster(calendar_id):
	"""
	Route to handle anti-clustering of a Calendar

	Inputs:
	- calendar_id : Int unique identifier for a Calendar entry in the database
	"""
	form = AntiClusterForm()
	calendar = Calendar.query.get_or_404(calendar_id)
	notes = set([note for events in calendar.obj.events.values()
					for event in events
					for note in event.notes.keys()])
	form.attribute.choices = [(note, note) for note in sorted(notes)]
	form.start.choices = [(option, option) for option in sorted(CalendarObject.KNOWN_START_BEHAVIOR)]
	if form.validate_on_submit():
		# Assign defautls
		shift = (form.shift.data if form.shift else 1)
		start = (form.start.data if form.start else "earliest")
		centers = (form.centers.data if form.centers else -1)
		obj_ = calendar.obj
		obj_.antiCluster(attribute=form.attribute.data,
									shift=shift,
									start=start,
									centers=centers)

		flag_modified(calendar, 'obj')
		db.session.commit()

		return redirect(url_for("users.view_calendar", calendar_id=calendar_id))

	return render_template("anticluster_calendar.html", form=form, calendar=calendar.obj)
