"""Forms"""

# Import Form and RecaptchaField (optional)
from flask_wtf import FlaskForm # , RecaptchaField

# Import Form elements such as TextField and BooleanField (optional)
from wtforms import TextField, PasswordField, BooleanField, StringField, validators# BooleanField

# Import Form validators
from wtforms.validators import InputRequired, Length, EqualTo


# Define the login form (WTForms)

class LoginForm(FlaskForm):
    username = TextField('Username', [
        InputRequired(message='Forgot your username?'),
        Length(min=4, max=25)])
    password = PasswordField('Password', [
        InputRequired(message='Must provide a password.')])

class RegistrationForm(FlaskForm):
    username = TextField('Username', [
        InputRequired(message='Forgot your username?')])
    password = PasswordField('New Password', [
        InputRequired(message='Input Required'), 
        EqualTo('confirm', message='Passwords must match'),
        Length(min=4, max=30)])
    confirm  = PasswordField('Repeat Password', [
        InputRequired(message='Repeat password.')])
