from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class ContentDatabase(db.Model):
	id = db.Column(db.String, primary_key = True)
	title = db.Column(db.String)
	content = db.Column(db.String)
