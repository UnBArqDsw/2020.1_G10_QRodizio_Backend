from flask import Blueprint, jsonify, abort, request

from qrodizio.ext.database import db
from qrodizio.ext.authentication import auth_required
from qrodizio.models.users import Employee, EmployeeRole
from qrodizio.builders import employee_builder
from qrodizio.utils.dbutils import dbFacade

employees_bp = Blueprint("employees", __name__, url_prefix="/employees")


@employees_bp.route("/", methods=["GET"])
@auth_required()
def get_employees(current_employee):
    employees_query = Employee.query.all()
    employees = [employee.to_dict() for employee in employees_query]

    return jsonify({"employees": employees}), 200


@employees_bp.route("/<employee_id>", methods=["GET"])
@auth_required()
def get_single_employee(current_employee, employee_id):
    employee = Employee.query.filter_by(id=employee_id).first() or abort(404)
    return jsonify(employee.to_dict()), 200


@employees_bp.route("/<employee_id>", methods=["DELETE"])
@auth_required(role=EmployeeRole.manager)
def delete_employee(current_employee, employee_id):
    employee = Employee.query.get_or_404(employee_id)

    dbFacade.delete_commit_session(db, employee)

    return jsonify({"deleted": "employee deleted"}), 202


@employees_bp.route("/<employee_id>", methods=["PUT"])
@auth_required()
def update_employee(current_employee, employee_id):
    if (  # only manager can edit other employees
        current_employee.id != employee_id
        and current_employee.role != EmployeeRole.manager
    ):
        return (
            jsonify({"error": "You're not a manager, cant edit other employees"}),
            403,
        )

    employee = Employee.query.get_or_404(employee_id)

    employee = employee_builder(employee=employee, **request.json)
    dbFacade.add_commit_session(db, employee)
    
    return jsonify({"success": "employee updated"}), 200
