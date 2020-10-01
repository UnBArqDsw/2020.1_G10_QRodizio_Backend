from flask import Blueprint, jsonify, abort

from qrodizio.models import Employee

employees_bp = Blueprint("employees", __name__, url_prefix="/employees")


@employees_bp.route("/", methods=["GET"])
def get_employees():
    employees_query = Employee.query.all()
    employees = [employee.to_dict() for employee in employees_query]

    return jsonify({"employees": employees}), 200


@employees_bp.route("/<employee_id>", methods=["GET"])
def get_single_employee(employee_id):
    employee = Employee.query.filter_by(id=employee_id).first() or abort(404)
    return jsonify(employee.to_dict()), 200
