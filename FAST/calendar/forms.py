from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import (
    DataRequired,
)

class EventForm(FlaskForm):
    tag = StringField("Tag", validators=[DataRequired()])
    information = TextAreaField("Description", validators=[DataRequired()])

    submit = SubmitField("Create Event")
