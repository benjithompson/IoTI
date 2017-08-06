"""Flask API"""

#imports
import os, sys
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema, fields, ValidationError, pre_load

app = Flask(__name__)
app.config.from_object(__name__)

#Load default config and override config from an environment variable
app.config.update(dict(
    SQLALCHEMY_DATABASE_URI = 'sqlite:///ioti.db',
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='admin'
))
app.config.from_envvar('IOTI_SETTINGS')
db = SQLAlchemy(app)

#Models
class Device(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True)
    desc = db.Column(db.String(120), unique=False)

    # def __init__(self, name, desc):
    #     self.name = name
    #     self.desc = desc

    # # def __repr__(self):
    # #     return '<Devices: name={0.name!r}, desc={0.desc!r}>'.format(self)
    

#Schema
class DeviceSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()
    desc = fields.Str()

    def format_device(self, device):
        return "Name: {}, Desc: {}".format(device.name, device.desc)
 
device_schema = DeviceSchema()
devices_schema = DeviceSchema(many=True)

#===========================================================================
#API

@app.route('/api/v1.0/devices/', methods=['GET'])
def devices():
    devices = Device.query.all()
    #serialize the queryset
    result = devices_schema.dump(devices)
    return jsonify({'devices': result.data})

@app.route('/api/v1.0/devices/<int:id>')
def device(id):
    try:
        device = Device.query.get(id)
    except IntegrityError:
        return jsonify({"message": "Device could not be found."}), 400
    device_result = device_schema.dump(device)
    return jsonify({'device': device_result.data})

#===========================================================================
#VIEWS======================================================================
#===========================================================================


@app.route('/api/v1.0/', methods=['GET'])
def show_api():
    return render_template('show_api_v1.0.html')



#===========================================================================
#INDEX
@app.route('/')
def show_index():
    return render_template('index.html')


@app.route('/login/', methods=['GET', 'POST'])
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
            return redirect(url_for('show_devices'))
    return render_template('login.html', error=error)

@app.route('/logout/')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out', category='message')
    return redirect(url_for('show_devices'))

#===================================================================
#devices

@app.route('/devices/')
def show_devices():
    devices = Device.query.all()
    result = devices_schema.dump(devices)
    return render_template('show_devices.html', devices=devices)


#From View
@app.route('/devices/add', methods=['POST'])
def add_device():
    if not session.get('logged_in'):
        abort(401)
    name = request.form['name']
    desc = request.form['desc']
    print('name: \'{}\', desc: \'{}\''.format(name, desc, file=sys.stdout))
    if request.form['name'] != '' or request.form['desc'] != '':
        device = Device(name=name, desc=desc)
        db.session.add(device)
        db.session.commit()
        flash('New entry was successfully posted')
    else:
        flash('Entry Empty')
    return redirect(url_for('show_devices'))

@app.route('/devices/remove', methods=['POST'])
def remove_device():
    if not session.get('logged_in'):
        abort(401)
    device_id = request.form['id']
    print('id: ' + device_id + ' requested removal from db entry', file=sys.stdout, flush=True)
    device = Device.query.get(device_id)
    db.session.delete(device)
    db.session.commit()
    
    flash('Entry was successfully removed')
    return redirect(url_for('show_devices'))

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True, port=5000)