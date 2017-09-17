#/usr/bin/env python3

"""Flask API"""

#imports
from datetime import datetime
from flask import Blueprint, Flask, render_template, session

# Define the blueprint: 'auth', set its url prefix: app.url/api
mod_api = Blueprint('api', __name__, url_prefix='/api')

# @app.route('/api/v1.0/')
# def api_v1():
#     """Gets the meta data in json format"""
#     pass

# @app.route('/api/v1.0/devices/', methods=['GET'])
# def devices():
#     """Get all of the registered devices"""
#     devices = Device.query.all()
#     #serialize the queryset
#     result = devices_schema.dump(devices)
#     return jsonify({'devices': result.data})

# @app.route('/api/v1.0/devices/<int:id>', methods=['GET'])
# def device(id):
#     try:
#         device = Device.query.get(id)
#     except IntegrityError:
#         return jsonify({"message": "Device could not be found."}), 400
#     device_result = device_schema.dump(device)
#     return jsonify({'device': device_result.data})

# @app.route('f', methods=['GET', 'POST'])
# def deviceData(id):

#     #Add data to device 'id'
#     if request.method == 'POST':
#         device = Device.query.get(id)
#         if request.is_json():
#             request_data = request.get_json()
#             data_array = json.loads(request_data)
#             data = Data(value = data_array)
#         else:
#             return jsonify({"message": "Request not formatted as json"}), 500
#     else:
#         try:
#             device = Device.query.get(id)
#         except IntegrityError:
#             return jsonify({"message": "Device could not be found."}), 400  

#     return jsonify({'device data': device_result.data})

# """Views"""

# @app.route('/api/', methods=['GET'])
# def show_api_home():
#     return render_template('api_v1.0_home.html')

# @app.route('/api/help', methods=['GET'])
# def show_api_help():
#     return render_template('api_v1.0_help.html')

#===========================================================================
#INDEX
@mod_api.route('/')
def home():
    return render_template('api/home.html', heading='api')
