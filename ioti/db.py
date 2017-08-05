import os
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash, current_app

def connect_db():
    """Connects to the specific database"""

    rv = sqlite3.connect(current_app.config(['DATABASE']))
    rv.row_factory = sqlite3.Row
    return rv

def get_db():
    """Opens a new database connection if there is none yet for the current app context"""

    #g is a general purpose variable associated w/ the current app context
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

#It’s executed every time the application context tears down:
@current_app.teardown_appcontext
def close_db(error):
    """closes the database again at the end of the request"""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()