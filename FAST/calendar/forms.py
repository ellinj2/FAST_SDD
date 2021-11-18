from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import (
    DataRequired,
)
from flask_wtf.file import FileField, FileRequired, FileAllowed

class EventForm(FlaskForm):
    tag = StringField("Tag", validators=[DataRequired()])
    information = TextAreaField("Description", validators=[DataRequired()])

    submit = SubmitField("Create Event")

class UploadForm(FlaskForm):
    file = FileField("JSON file", validators=[
            FileRequired(),
            FileAllowed(['json'], "JSON files only!")
        ])

    submit = SubmitField("Upload file")
