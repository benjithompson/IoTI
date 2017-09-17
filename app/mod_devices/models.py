"""Authentication DB for Users"""

from app import db

class Device(db.Model):

    __tablename__ = 'device_devices'

    id         = db.Column(db.Integer, primary_key=True)
    ipaddress  = db.Column(db.String, unique=True)
    name       = db.Column(db.String(30), unique=False)
    desc       = db.Column(db.String(120), unique=False)
    date_added = db.Column(db.String(20), default=db.func.current_timestamp())
    owner      = db.Column(db.String(20), unique=False)
    datas      = db.relationship('Data', backref='device_devices', lazy='dynamic')

    def __init__(self, ipaddress, name=None, desc=None):
        self.ipaddress = ipaddress
        self.name      = name
        self.desc      = desc

    def __repr__(self):
        return '<Device: ipaddress={0.ipaddress!r}, name={0.name!r}, desc={0.desc!r}, date_added={0.date_added!r}>'.format(self)

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
