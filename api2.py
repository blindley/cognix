from flask import Blueprint, request, jsonify

api2 = Blueprint('api2', __name__)

@api2.route('/api2', methods=['POST'])
def index():
    req_data = request.get_json()
    return jsonify({"what you sad": req_data})
