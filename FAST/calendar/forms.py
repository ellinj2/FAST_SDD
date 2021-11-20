from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, SelectField, IntegerField
from wtforms.validators import (
    DataRequired,
)
from flask_wtf.file import FileField, FileRequired, FileAllowed

class EventForm(FlaskForm):
    """
    Form to handle Event generation

    Fields:
    - tag : Pseudo-unique String associated to Event
    - information : String holding Key : Value information for the Event
    - submit : Submission to push the Form back to the handler
    """
    tag = StringField("Tag", validators=[DataRequired()])
    information = TextAreaField("Description", validators=[DataRequired()])

    submit = SubmitField("Create Event")

class UploadForm(FlaskForm):
    """
    Form to handle uploading data

    Fields:
    - file : JSON holding JSON data in the structure >>>
        {
            "Evenets": [
                {
                    "Name": String,
                    "Start Time": String,
                    "End Time" : String,
                    Keys : Values
                },
            ]
        }
    - submit : Submission to push the Form back to the handler
    """
    file = FileField("", validators=[
            FileRequired(),
            FileAllowed(['json'], "JSON files only!")
        ])

    submit = SubmitField("Upload file")

class ClusterForm(FlaskForm):
    """
    Form to handle clustering of Calendars

    Fields:
    - attribute : Selection for which Event attribute to cluster around
    - shift : Integer for the time slot distance between two Events in the same cluster
    - start : Selection for how to select the first time slot
    - centers : Number of clusters to use
    - submit : Submission to push the Form back to the handler
    """
    attribute = SelectField("Clustering Attribute", validators=[DataRequired()])
    shift = IntegerField("Time slots between Events")
    start = SelectField("Starting time method")
    centers = IntegerField("Number of clusters")

    submit = SubmitField("Cluster")

class AntiClusterForm(FlaskForm):
    """
    Form to handle anti-clustering of Calendars

    Fields:
    - attribute : Selection for which Event attribute to anti-cluster around
    - shift : Integer for the time slot distance between two Events in the same anti-cluster
    - start : Selection for how to select the first time slot
    - centers : Number of clusters to use
    - submit : Submission to push the Form back to the handler
    """
    attribute = SelectField("Anti-Clustering Attribute", validators=[DataRequired()])
    shift = IntegerField("Time slots between Events")
    start = SelectField("Starting time method")
    centers = IntegerField("Number of clusters")

    submit = SubmitField("Cluster")
