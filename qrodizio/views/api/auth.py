import jwt
import datetime

from flask import Blueprint, jsonify, request
from qrodizio.ext.authentication import verify_password, get_secret_key, auth_required
from qrodizio.models.users import Employee, EmployeeRole
from qrodizio.builders import employee_builder

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


@auth_bp.route("/register", methods=["POST"])
@auth_required(role=EmployeeRole.manager)
def auth_register_employee(current_employee):
    name = request.json.get("name")
    password = request.json.get("password")
    email = request.json.get("email")
    role = request.json.get("role")

    if None in [name, password, email, role]:
        return jsonify({"error": "Missing paramenter"}), 400

    if Employee.query.filter_by(email=email).first() is not None:
        return jsonify({"error": "User already exists"}), 400

    employee = employee_builder(name=name, email=email, password=password, role=role)
    employee.create()

    return jsonify({"employee": employee.to_dict()}), 201


@auth_bp.route("/login", methods=["POST"])
def auth_loggin_employee():
    password = request.json.get("password")
    email = request.json.get("email")

    if None in [password, email]:
        return jsonify({"error": "Missing paramenter"}), 400

    employee = Employee.query.filter_by(email=email).first()

    if employee is None:
        return jsonify({"error": "User not found"}), 404

    check = verify_password(employee.password, password)

    if not check:
        return jsonify({"error": "Wrong password"}), 401

    payload = {
        "id": employee.id,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=8),
    }

    token = jwt.encode(payload, get_secret_key())
    user = employee.to_dict()

    return jsonify({"token": token.decode("utf-8"), "user": user}), 200
