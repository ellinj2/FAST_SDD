from flask import render_template, Blueprint, redirect, url_for, request, flash
from FAST.forms import DataUploadForm
from flask_login import current_user, login_required, logout_user
from FAST import app
from FAST.calendar.forms import *
from FAST.calendar.models import *
from FAST.database import *
from werkzeug.utils import secure_filename
import os

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
	form = EventForm()
	print("here1")
	print(form.data)
	print(form.information)
	# if form.validate_on_submit():
	# 	print("here2")
	# 	notes = [[f.strip() for f in line.split(':')] for line in form.information.data.split('\n')]
	# 	notes = {note[0]: ':'.join(note[1:]) for note in notes}
	# 	print(notes)
	# 	event = EventObject(tag=form.tag.data,
	# 						start_time=notes["Start Time"],
	# 				 		end_time=notes["End Time"])
	# 	event.assign(**notes)
	# 	event_entry = Event(name=event.tag,
	# 						obj=event,
	# 						user_id=current_user.id)

	# 	db.session.add(event_entry)
	# 	db.session.commit()
	# 	form = EventForm()
	return render_template("upload_file.html", form=form)
	# if form.validate_on_submit():
    #     filename = secure_filename(form.file.data.filename)
    #     form.file.data.save('uploads/' + filename)
    #     return redirect(url_for('upload'))


	# if request.method == 'POST':
		# req = request.get_json()
		# form = DataUploadForm.from_json(req)
		# language = req['language']
		# print(language)
	# 	print("here")
	# return render_template("upload_file.html")