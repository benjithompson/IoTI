"""Device Forms"""

# Import Form and RecaptchaField (optional)
from flask_wtf import FlaskForm # , RecaptchaField

# Import Form elements such as TextField and BooleanField (optional)
from wtforms import TextField, SelectField, validators# BooleanField

# Import Form validators
from wtforms.validators import InputRequired, Length, EqualTo

choices = [('data','data'), ('sensor', 'sensor'), ('display','display')]
# Define the Add Device form (WTForms)

class DeviceRegistrationForm(FlaskForm):
    name = TextField('Name', [
        InputRequired(message='Add Name')])
    category = SelectField(u'Category', choices=choices)
    ip  = TextField('IP', [
        InputRequired(message='Add IP Address'),
        validators.IPAddress(ipv4=True, message='Enter valid IP address (0.0.0.0)')])
