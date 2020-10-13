from flask import Blueprint, jsonify, abort

from qrodizio.models import Employee
from qrodizio.ext.authentication import auth_required
import qrcode
from flask import send_file
import base64
from io import BytesIO



qrcode_bp = Blueprint("qrcode", __name__, url_prefix="/qrcode")


@qrcode_bp.route("/", methods=["GET"])
def get_qrcode():    
    image = qrcode.make('Some data here')
    #img = qrcode.make('Some data here', image_factory=PymagingImage)    
    buffered = BytesIO()
    image.save(buffered, format="JPEG")
    some_dict = {}
    some_dict["imagedata"] = base64.b64encode(buffered.getvalue()).decode("ascii")
    return jsonify(some_dict), 200


# @employees_bp.route("/<employee_id>", methods=["GET"])
# @auth_required()
# def get_single_employee(current_employee, employee_id):
#     employee = Employee.query.filter_by(id=employee_id).first() or abort(404)
#     return jsonify(employee.to_dict()), 200
