# Imports
from FAST import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from FAST.calendar.models import *

@login_manager.user_loader
def load_user(user_id):
	"""
	Support login for db
	"""
	return User.query.get(user_id)

class User(db.Model, UserMixin):
	"""
	Database table for user data

	Columns:
	- __tablename__ - reference for relational interactions
	- id : Unique number to reference Users
	- email : Unique login hanlder for Useres
	- password_hash : Hashed passwords for the User
	- calendars : Relation to Calendar table to track Calendars generated by User
	- events : Relation to Event table to track Events generated by User

	Functions:
	- __init__(User, String, String) : Generates User row
	- check_password(User, String) : Compares input password to hashed storage
	- __repr__(User) : String representation of a User
	"""
	__tablename__ = "users"
	id = db.Column(db.Integer, primary_key=True)
	email = db.Column(db.String, unique=True, index=True)
	password_hash = db.Column(db.String)

	calendars = db.relationship("Calendar", backref="owner", lazy=True)
	events = db.relationship("Event", backref="owner", lazy=True)

	def __init__(self, email, password):
		self.email = email
		self.password_hash = generate_password_hash(password)

	def check_password(self, password):
		return check_password_hash(self.password_hash, password)

	def __repr__(self):
		return f"Username: {self.username}"

class Calendar(db.Model):
	"""
	Database table for user data

	Columns:
	- __tablename__ - reference for relational interactions
	- id : Unique number to reference Calendars
	- user_id : Integer for the ID of the User that created the Calendar
	- name : Pseudo-unique String associated to the Calendar
	- obj : CalendarObject as Pickle for the Python Object storing Calendar information

	Functions:
	- __init__(User, String, String) : Generates Calendar row
	- __repr__(User) : String representation of an Event
	"""
	__tablename__ = "calendars"
	id = db.Column(db.Integer, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

	name = db.Column(db.String, nullable=False)
	obj = db.Column(db.PickleType(), nullable=False)

	def __init__(self, name, obj, user_id):
		self.name = name
		self.obj = obj
		self.user_id = user_id

	def __repr__(self):
		return f"Calendar ID: {self.id}\nName: {self.name}"

class Event(db.Model):
	"""
	Database table for user data

	Columns:
	- __tablename__ - reference for relational interactions
	- users : Relation to Users associated with the Event
	- name : Pseudo-unique String associated to the Event
	- obj : EventObject as Pickle for the Python Object storing Event information

	Functions:
	- __init__(User, String, String) : Generates Event row
	- __repr__(User) : String representation of a Event
	"""
	__tablename__ = "events"
	users = db.relationship(User)

	id = db.Column(db.Integer, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

	name = db.Column(db.String, nullable=False)
	obj = db.Column(db.PickleType(), nullable=False)

	def __init__(self, name, obj, user_id):
		self.name = name
		self.obj = obj
		self.user_id = user_id

	def __repr__(self):
		return f"Event ID: {self.id}\nName: {self.name}"
