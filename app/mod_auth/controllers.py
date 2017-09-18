# Import flask dependencies
from flask import Blueprint, request, render_template, \
                  flash, g, session, redirect, url_for, abort

from flask_login import login_required, login_user, logout_user, LoginManager

# Import password / encryption helper tools
from werkzeug import check_password_hash, generate_password_hash

# Import the database object from the main app module
from app import db

# Import module forms
from app.mod_auth.forms import LoginForm, RegistrationForm

# Import module models (i.e. User)
from app.mod_auth.models import User

# Define the blueprint: 'auth', set its url prefix: app.url/auth
mod_auth = Blueprint('auth', __name__, url_prefix='/auth')

# Set the route and accepted methods
@mod_auth.route('/signin/', methods=['GET', 'POST'])
def signin():

    # If sign in form is submitted
    form = LoginForm(request.form)
    # Verify the sign in form
    if form.validate_on_submit() and request.method == 'POST':
        user = User.query.filter_by(username=form.username.data).first()
        if user is None:
            print('no username "{0}"'.format(form.username.data))
            abort(401)
        if check_password_hash(user.password, form.password.data):
            # session['username'] = user.username
            # session['signed_in'] = True
            login_user(user)
            flash('Welcome %s' % user.username)
            return redirect(url_for('devices.show_devices'))

        flash('Wrong username or password', 'error-message')

    return render_template('auth/signin.html', form=form)

# Set the route and accepted methods
@mod_auth.route('/signout/', methods=['GET', 'POST'])
@login_required
def signout():

    # session.pop('username', None)
    # session['signed_in'] = False
    logout_user()
    return redirect(url_for('auth.signin'))


# Set the route and accepted methods
@mod_auth.route('/register/', methods=['GET', 'POST'])
def register():

    form = RegistrationForm(request.form)
    if form.validate_on_submit() and request.method == 'POST':

        #check if user exists
        exists = db.session.query(db.exists().where(User.username == form.username.data)).scalar()
        print(exists)
        if exists:
            flash('Username already exists')
            return render_template('auth/register.html', form=form)
        else:
            try:
                user = User(form.username.data,
                            form.password.data)
                db.session.add(user)
                db.session.commit()
                flash('Thanks for registering')
                LoginManager.login_message('Please login')
                return redirect(url_for('auth.signin'))
            except:
                print('sql exception')
                db.session.rollback()

    return render_template('auth/register.html', form=form)