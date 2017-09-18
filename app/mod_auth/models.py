"""Authentication DB for Users"""

from app import db
from app import login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash

class Base(db.Model, UserMixin):

    __abstract__  = True

    id            = db.Column(db.Integer, autoincrement=True, primary_key=True)
    date_created  = db.Column(db.DateTime,  default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime,  default=db.func.current_timestamp(),
                                           onupdate=db.func.current_timestamp())

# Define a User model
class User(Base):

    __tablename__ = 'auth_user'

    username = db.Column(db.String(128), unique=True, nullable=False)
    password = db.Column(db.String(192),  nullable=False)
    devices  = db.relationship('Device', backref='auth_user', lazy='dynamic')

    # New instance instantiation procedure
    def __init__(self, username, password):
        self.username = username
        self.password = generate_password_hash(password)

    def __repr__(self):
        return '<User %r>' % (self.username)


# callback to reload the user object        
@login_manager.user_loader
def load_user(id):
    return User.query.filter_by(id=id).first()
