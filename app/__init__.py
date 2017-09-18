"""Init the app"""

# Import flask and template operators
from flask import Flask, render_template, redirect, url_for
# Import SQLAlchemy
from flask_sqlalchemy import SQLAlchemy

from flask_login import LoginManager

# Define the WSGI application object
app = Flask(__name__)

# Configurations
app.config.from_object('config')

# Define the database object which is imported
# by modules and controllers
db = SQLAlchemy(app)

#Init flask login manager
login_manager = LoginManager()
login_manager.init_app(app)

# Sample HTTP error handling
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

# handle login failed
@app.errorhandler(401)
def page_not_found(e):
    return redirect(url_for('auth.signin'))

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

# Import a module / component using its blueprint handler variable (mod_auth)
from app.mod_auth.controllers   import mod_auth   as auth_module
from app.mod_devices.controllers import mod_devices as devices_module
from app.mod_api.controllers   import mod_api   as api_module

# Register blueprint(s)
app.register_blueprint(auth_module)
app.register_blueprint(devices_module)
app.register_blueprint(api_module)
# ..

# Build the database:
# This will create the database file using SQLAlchemy
db.create_all()
