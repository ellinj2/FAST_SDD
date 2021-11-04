from flask import render_template, Blueprint
from flask_login import current_user, login_required, logout_user
from FAST import app

calendar = Blueprint("calendar", __name__)

@calendar.route('/upload_event', methods=["GET", "POST"])
def upload_event():
	return render_template("upload_event.html")

@calendar.route('/generate_claendar', methods=["GET", "POST"])
def generate_calendar():
	return render_template("generate_calendar.html")

@calendar.route('/download_calendar', methods=["GET", "POST"])
def download_calendar():
	return render_template("download_calendar.html")
