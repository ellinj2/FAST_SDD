"""Sign-up & log-in forms."""
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, TextAreaField
from wtforms.validators import (
    DataRequired,
    Email,
    EqualTo,
    Length,
    Optional
)


class SignupForm(FlaskForm):
    """
    User Sign-up Form

    Fields:
    - email : Unique String to identify a User
    - password : Secure login verification String
    - confirm : Verify the input password (MUST MATCH password FIELD)
    - submit : Submission to push the Form back to the handler
    """
    email = StringField(
        'Email',
        validators=[
            Email(message='Enter a valid email.'),
            DataRequired()
        ]
    )
    password = PasswordField(
        'Password',
        validators=[
            DataRequired(),
        ]
    )
    confirm = PasswordField(
        'Confirm Your Password',
        validators=[
            DataRequired(),
            EqualTo('password', message='Passwords must match.')
        ]
    )
    submit = SubmitField('Register')


class LoginForm(FlaskForm):
    """
    User Log-in Form

    Fields:
    - email : Unique String to identify a User
    - password : Secure login verification String
    - submit : Submission to push the Form back to the handler
    """
    email = StringField(
        'Email',
        validators=[
            DataRequired(),
            Email(message='Enter a valid email.')
        ]
    )
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')

class CalendarForm(FlaskForm):
    """
    Calendar generation Form

    Fields:
    - heuristic : List of (String, String) pairs of heuristics
    - name : Pseudo-unique String to identify a selected Calendar
    - timslots : new-line separated Strings used to assign Events to times (must be MM:DD:YYYY:HH:MM:SS)
    - submit : Submission to push the Form back to the handler
    """
    options = [('rand', "Random"),
               ('start', "Start-time Centered"),]
    heuristic = SelectField("Generation Heuristic", choices=options, validators=[DataRequired(),])
    name = StringField("Calendar Name", validators=[DataRequired(),])
    timeslots = TextAreaField("Time Slots", validators=[DataRequired()])
    submit = SubmitField("Generate Calendar")
