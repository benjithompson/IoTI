"""Flask API"""

#imports
import os
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash

app = Flask(__name__)
app.config.from_object(__name__)

#Load default config and override config from an environment variable
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'ioti.db'),
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='default'
))

app.config.from_envvar('IOTI_SETTINGS')

def connect_db():
    """Connects to the specific database"""

    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv

"""The open_resource() method of the application object is a convenient helper function that will open a resource that the application provides. 
This function opens a file from the resource location (the flaskr/flaskr folder) and allows you to read from it. 
It is used in this example to execute a script on the database connection."""
def init_db():
    db = get_db()
    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()

"""The app.cli.command() decorator registers a new command with the flask script. When the command executes, 
Flask will automatically create an application context which is bound to the right application. 
Within the function, you can then access flask.g and other things as you might expect. When the script ends, 
the application context tears down and the database connection is released."""
@app.cli.command('initdb')
def initdb_command():
    """Initializes the database."""
    init_db()
    print('Initialized the database.')

def get_db():
    """Opens a new database connection if there is none yet for the current application context."""
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

#It’s executed every time the application context tears down:
@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()