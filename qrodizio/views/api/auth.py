import jwt
import datetime

from flask import Blueprint, jsonify, request
from qrodizio.ext.authentication import (
    hash_password,
    verify_password,
    get_secret_key,
)
from qrodizio.models import Employee

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


@auth_bp.route("/register", methods=["POST"])
def auth_register_employee():
    name = request.json.get("name")
    password = request.json.get("password")
    email = request.json.get("email")

    if None in [name, password, email]:
        return jsonify({"error": "Missing paramenter"}), 400

    if Employee.query.filter_by(email=email).first() is not None:
        return jsonify({"error": "User already exists"}), 400

    employee = Employee(name=name, email=email)
    employee.password = hash_password(password)
    employee.create()

    return jsonify({"employee": employee.to_dict()}), 201


@auth_bp.route("/loggin", methods=["POST"])
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

    return jsonify({"token": token.decode("utf-8")})
