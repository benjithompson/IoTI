import sys

# Import flask dependencies
from flask import Blueprint, request, render_template, \
                  flash, g, session, redirect, url_for, abort

# Import the database object from the main app module
from app import db

from marshmallow import Schema, fields, ValidationError, pre_load

# Import module models (i.e. User)
from app.mod_devices.models import Device

#Device Schema to serialize data for jsonify
class DeviceSchema(Schema):
    """Marshmallow Device Table Schema to serialize for jsonify"""
    id         = fields.Int(dump_only=True)
    ipaddress  = fields.Str()
    name       = fields.Str()
    desc       = fields.Str()
    date_added = fields.DateTime()
    owner      = fields.Str()
    val        = fields.Int()

    def format_device(self, device):
        return "id: {}, ip: {}, name: {}, desc: {}, date_added: {}, owner: {}, val: {}".format(
            device.id,
            device.ipaddress,
            device.name,
            device.desc,
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
    devices = Device.query.all()
    result = devices_schema.dump(devices)
    return render_template('device/show_devices.html', devices=devices)

# #From View
# @mod_device.route('/add', methods=['POST'])
# def add_device():
#     if not session.get('logged_in'):
#         abort(401)
#     name = request.form['name']
#     desc = request.form['desc']
#     ipaddress = request.form['ipaddress']
#     date_added = request.form['date_added']
#     owner = request.form['owner']
#     val = request.form['val']

#     print('name: \'{}\', desc: \'{}\''.format(name, desc, file=sys.stdout))
#     if request.form['name'] != '' or request.form['desc'] != '':
#         device = Device(name=name,
#                         desc=desc,
#                         ipaddress=ipaddress)
#         db.session.add(device)
#         db.session.commit()
#         flash('New entry was successfully posted')
#     else:
#         flash('Entry Empty')
#     return redirect(url_for('device/show_devices'))

# @mod_device.route('/remove/', methods=['POST'])
# def remove_device():
#     if not session.get('logged_in'):
#         abort(401)
#     device_id = request.form['id']
#     print('id: ' + device_id + ' requested removal from db entry', file=sys.stdout, flush=True)
#     device = Device.query.get(device_id)
#     db.session.delete(device)
#     db.session.commit()

#     flash('Entry was successfully removed')
#     return redirect(url_for('device/show_devices'))