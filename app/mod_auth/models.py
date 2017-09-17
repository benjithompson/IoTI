"""Authentication DB for Users"""

from app import db
from werkzeug.security import generate_password_hash

class Base(db.Model):

    __abstract__  = True

    id            = db.Column(db.Integer, autoincrement=True, primary_key=True)
    date_created  = db.Column(db.DateTime,  default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime,  default=db.func.current_timestamp(),
                                           onupdate=db.func.current_timestamp())

# Define a User model
class User(Base):

    __tablename__ = 'auth_user'

    username     = db.Column(db.String(128), unique=True, nullable=False)
    password = db.Column(db.String(192),  nullable=False)

    # New instance instantiation procedure
    def __init__(self, username, password):
        self.username     = username
        self.password = generate_password_hash(password)

    def __repr__(self):
        return '<User %r>' % (self.username)
