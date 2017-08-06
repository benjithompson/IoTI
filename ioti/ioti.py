"""Flask API"""

#imports
import os, sys
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
    PASSWORD='admin'
))

app.config.from_envvar('IOTI_SETTINGS')

#===========================================================================
#INDEX
@app.route('/')
def show_index():
    db = get_db()
    cur = db.execute('select * from entries order by id desc')
    entries = cur.fetchall()
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in', category='message')
            return redirect(url_for('show_entries'))
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out', category='message')
    return redirect(url_for('show_entries'))

#===========================================================
#DB
def connect_db():
    """Connects to the specific database"""

    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv

"""The open_resource() method of the application object is a convenient helper function that will open a
resource that the application provides.This function opens a file from the resource location (the flaskr/flaskr folder)
and allows you to read from it. It is used in this example to execute a script on the database connection."""
def init_db():
    db = get_db()
    with ioti.app.open_resource('schema.sql', mode='r') as f:
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

#===================================================================
#API

@app.route('/api/v1.0/', methods=['GET'])
def show_api():
    return redirect(url_for('show_api_v1.0'))

#===================================================================
#ENTRIES

@app.route('/entries')
def show_entries():
    db = get_db()
    cur = db.execute('select * from entries order by id desc')
    entries = cur.fetchall()
    return render_template('show_entries.html', entries=entries)

@app.route('/entries/add', methods=['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)
    print('title: ' + request.form['title'] + ' text: ' + request.form['text'], file=sys.stdout, flush=True)
    if request.form['title'] != '' or request.form['text'] != '':
        db = get_db()
        db.execute('insert into entries (title, text) values (?, ?)',
                   [request.form['title'], request.form['text']])
        db.commit()
        flash('New entry was successfully posted')
    else:
        flash('Entry Empty')
    return redirect(url_for('show_entries'))

@app.route('/entries/remove', methods=['POST'])
def remove_entry():
    if not session.get('logged_in'):
        abort(401)
    print('id: ' + request.form['id'] + ' requested removal from db entry', file=sys.stdout, flush=True)
    db = get_db()
    db.execute('DELETE FROM entries WHERE id = (?)',
               [request.form['id']])
    db.commit()
    
    flash('Entry was successfully removed')
    return redirect(url_for('show_entries'))
