from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, SelectField, IntegerField
from wtforms.validators import (
    DataRequired,
)
from flask_wtf.file import FileField, FileRequired, FileAllowed

class EventForm(FlaskForm):
    tag = StringField("Tag", validators=[DataRequired()])
    information = TextAreaField("Description", validators=[DataRequired()])

    submit = SubmitField("Create Event")

class UploadForm(FlaskForm):
    file = FileField("", validators=[
            FileRequired(),
            FileAllowed(['json'], "JSON files only!")
        ])

    submit = SubmitField("Upload file")

class ClusterForm(FlaskForm):
    attribute = SelectField("Clustering Attribute", validators=[DataRequired()])
    shift = IntegerField("Time slots between Events")
    start = SelectField("Starting time method")
    centers = IntegerField("Number of clusters")

    submit = SubmitField("Cluster")

class AntiClusterFOrm(FlaskForm):
    attribute = SelectField("Anti-Clustering Attribute", validators=[DataRequired()])
    shift = IntegerField("Time slots between Events")
    start = SelectField("Starting time method")
    centers = IntegerField("Number of clusters")

    submit = SubmitField("Cluster")    
