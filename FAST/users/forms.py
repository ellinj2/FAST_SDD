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
    """User Sign-up Form."""
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
    """User Log-in Form."""
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
    options = [('rand', "Random"),
               ('start', "Start-time Centered"),]
    heuristic = SelectField("Generation Heuristic", choices=options, validators=[DataRequired(),])
    name = StringField("Calendar Name", validators=[DataRequired(),])
    timeslots = TextAreaField("Time Slots", validators=[DataRequired()])
    submit = SubmitField("Generate Calendar")
