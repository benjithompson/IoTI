import sys

# Import flask dependencies
from flask import Blueprint, request, render_template, \
                  flash, g, session, redirect, url_for, abort

from flask_login import login_required, current_user

# Import the database object from the main app module
from app import db

from marshmallow import Schema, fields, ValidationError, pre_load

# Import module models (i.e. User)
from app.mod_devices.models import Device

# Import module forms
from app.mod_devices.forms import DeviceRegistrationForm

#Device Schema to serialize data for jsonify
class DeviceSchema(Schema):
    """Marshmallow Device Table Schema to serialize for jsonify"""
    id         = fields.Int(dump_only=True)
    ipaddress  = fields.Str()
    name       = fields.Str()
    category   = fields.Str()
    date_added = fields.DateTime()
    owner      = fields.Str()
    val        = fields.Int()

    def format_device(self, device):
        return "id: {}, ip: {}, name: {}, category: {}, date_added: {}, owner: {}, val: {}".format(
            device.id,
            device.ipaddress,
            device.name,
            device.category,
            device.date_added,
            device.owner,
            device.val)

#Data Schema
class DataSchema(Schema):
    """MarshmallowData Table schema to serialize data for jsonify"""
    id    = fields.Int(dump_only=True)
    date  = fields.DateTime()
    value = fields.Int()

    def format_device(self, device):
        return "id: {}, date: {}, value: {}".format(
            device.id,
            device.date,
            device.value)

device_schema  = DeviceSchema()
devices_schema = DeviceSchema(many=True)
data_schema    = DataSchema()
datas_schema   = DataSchema(many=True)

# Define the blueprint: 'device', set its url prefix: app.url/device
mod_devices = Blueprint('devices', __name__, url_prefix='/devices')

# Set the route and accepted methods
@mod_devices.route('/', methods=['GET', 'POST'])
def show_devices():
    devices = Device.query.filter_by(owner=current_user.username).all()
    result = devices_schema.dump(devices)
    return render_template('devices/show_devices.html', devices=devices)

#From View
@mod_devices.route('/add', methods=['GET', 'POST'])
@login_required
def add_device():

    form = DeviceRegistrationForm(request.form)
    print(form.category.data)
    print(form.ip.data)
    if form.validate_on_submit() and request.method == 'POST':
        device = Device(name=form.name.data,
                        category=form.category.data,
                        ip=form.ip.data,
                        owner=current_user.username)
        # try:
        db.session.add(device)
        db.session.commit()
        print('submitted add(device)')
        # except:
            # print('sql exception')
            # db.session.rollback()
        return redirect(url_for('devices.show_devices'))
    return render_template('devices/register.html', form=form)

@mod_devices.route('/remove/', methods=['POST'])
@login_required
def remove_device():

    device_id = request.form['id']
    print('id: ' + device_id + ' requested removal from db entry', file=sys.stdout, flush=True)
    device = Device.query.get(device_id)
    db.session.delete(device)
    db.session.commit()

    flash('Entry was successfully removed')
    return redirect(url_for('devices.show_devices'))
