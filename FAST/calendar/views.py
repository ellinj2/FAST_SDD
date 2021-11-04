from flask import render_template, Blueprint, redirect, url_for
from flask_login import current_user, login_required, logout_user
from FAST import app
from FAST.calendar.forms import *

calendar = Blueprint("calendar", __name__)

@calendar.route('/upload_event', methods=["GET", "POST"])
def upload_event():
	form = EventForm()
	return render_template("upload_event.html", form=form)

@calendar.route('/generate_claendar', methods=["GET", "POST"])
def generate_calendar():
	return render_template("generate_calendar.html")

@calendar.route('/download_calendar', methods=["GET", "POST"])
def download_calendar():
	return render_template("download_calendar.html")

@calendar.route('/help')
def help():
	return redirect(url_for('calendar.upload_event'))
