"""Authentication DB for Users"""

from app import db

class Device(db.Model):

    __tablename__ = 'device_devices'

    id         = db.Column(db.Integer, primary_key=True)
    ip         = db.Column(db.String, unique=False)
    name       = db.Column(db.String(30), unique=False)
    category   = db.Column(db.String(120), unique=False)
    date_added = db.Column(db.String(20), default=db.func.current_timestamp())
    owner      = db.Column(db.String(20), db.ForeignKey('auth_user.username'))
    datas      = db.relationship('Data', backref='device_devices', lazy='dynamic')

    def __init__(self, ip, owner=owner, name=None, category=None):
        self.ip       = ip
        self.name     = name
        self.category = category
        self.owner    = owner

    def __repr__(self):
        return '<Device: ipaddress={0.ipaddress!r}, name={0.name!r}, category={0.category!r}, date_added={0.date_added!r}>'.format(self)

class Data(db.Model):

    __tablename__ = 'device_data'
    
    id        = db.Column(db.Integer, primary_key=True)
    date      = db.Column(db.DateTime, default=db.func.current_timestamp())
    value     = db.Column(db.Float)
    device_id = db.Column(db.Integer, db.ForeignKey('device_devices.id'))

    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return '<Data: date={0.date!r}, value={0.value!r}'.format(self)
