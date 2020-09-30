from flask import Blueprint, jsonify

employees_bp = Blueprint("employees", __name__, url_prefix="/employees")

@employees_bp.route("/", methods=["GET"])
def get_employees():
    employees = [
        {"id": 1, "name": "Fulano", "email": "fulano@email.com"},
        {"id": 2, "name": "Ciclano", "email": "ciclano@email.com"},
    ]

    return jsonify({"employees": employees}), 200
