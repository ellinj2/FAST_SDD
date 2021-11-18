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

@calendar.route('/upload_file', methods=["GET", "POST"])
@login_required
def upload_file():
	form = UploadForm()
	if form.validate_on_submit():
		file = form.file.data
		json_data = json.loads(file.read())
		event = EventObject(
				tag=json_data["Name"],
				start_time=json_data["Start Time"],
				end_time=json_data["End Time"]
			)
		event.assign(**{key: json_data[key] for key in json_data if key not in ["Start Time", "End Time"]})
		event_entry = Event(
				name=event.tag,
				obj=event,
				user_id=current_user.id
			)
		db.session.add(event_entry)
		db.session.commit()

		return redirect(url_for("users.view_events"))

	return render_template("upload_file.html", form=form)
