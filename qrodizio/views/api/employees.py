from flask import Blueprint, jsonify, abort

from qrodizio.models import Employee
from qrodizio.ext.authentication import auth_required

employees_bp = Blueprint("employees", __name__, url_prefix="/employees")


@employees_bp.route("/", methods=["GET"])
@auth_required
def get_employees(current_employee):
    employees_query = Employee.query.all()
    employees = [employee.to_dict() for employee in employees_query]

    return jsonify({"employees": employees}), 200


@employees_bp.route("/<employee_id>", methods=["GET"])
@auth_required
def get_single_employee(current_employee, employee_id):
    employee = Employee.query.filter_by(id=employee_id).first() or abort(404)
    return jsonify(employee.to_dict()), 200
