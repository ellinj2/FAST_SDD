from FLASK import db, login_manager
from werkzeug.security import generate_password_hash, check_passwork_hash
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model, UserMixin):
	__table__name = "users"
	id = db.Column(db.Integer, primary_key=True)
	email = db.Column(db.String, unique=True, index=True)
	password_hash = db.column(db.String)

	calendars = db.relationship("Calendar", backref="owner", lazy=True)
	events = db.relationship("Event", backref="owner", lazy=True)

	def __init__(self, email, passowrd):
		self.email = email
		self.password_hash = generate_password_hash(password)

	def check_password(self, password):
		return check_password_hash(self.password_hash, password)

	def __repr__(self):
		return f"Username: {self.username}"

class Calendar(db.Model):
	users = db.relationship(User)

	id = db.Column(db.Integer, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

	
