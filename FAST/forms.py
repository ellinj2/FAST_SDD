from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import (
	DataRequired,
)

class DataUploadForm(FlaskForm):
	title = StringField("Title", validators=[DataRequired(),])
	content = StringField("Events", validators=[DataRequired(),])

	submit = SubmitField("Upload Schedule")
