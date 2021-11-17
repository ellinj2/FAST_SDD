from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, SelectField
from wtforms.validators import (
    DataRequired,
)

class EventForm(FlaskForm):
    tag = StringField("Tag", validators=[DataRequired()])
    information = TextAreaField("Description", validators=[DataRequired()])

    submit = SubmitField("Create Event")

class ClusterForm(FlaskForm):
    attribute = SelectField("Clustering Attribute", validators=[DataRequired()])
    shift = IntegerField("Time slots between Events")
    start = SelectField("Starting time method")
    centers = IntegerField("Number of clusters")

    submit = SubmitField("Cluster")
