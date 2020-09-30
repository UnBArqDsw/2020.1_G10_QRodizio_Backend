from flask import Blueprint, jsonify, abort

from qrodizio.models import Employee

employees_bp = Blueprint("employees", __name__, url_prefix="/employees")

@employees_bp.route("/", methods=["GET"])
def get_employees():
    employees_query = Employee.query.all() or abort(204)
    employees = [employee.to_dict() for employee in employees_query]

    return jsonify({"employees": employees}), 200
