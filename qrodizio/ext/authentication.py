import bcrypt
import jwt

from functools import wraps
from flask import request, jsonify

from qrodizio.models import Employee

_secret_key = None


def init_app(app):
    global _secret_key
    _secret_key = app.config["SECRET_KEY"]


def get_secret_key():
    return _secret_key


def hash_password(password):
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())


def verify_password(password_hash, password):
    hash_check = bcrypt.hashpw(password.encode("utf-8"), password_hash)
    return hash_check.decode("utf-8") == password_hash.decode("utf-8")


def auth_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        token = None

        if "authorization" in request.headers:
            token = request.headers["authorization"]

        if token is None:
            return jsonify({"error": "User unauthorized"}), 401

        if "Bearer" not in token:
            return jsonify({"error": "User unauthorized"}), 401

        try:
            pure_token = token.replace("Bearer ", "")
            decoded = jwt.decode(pure_token, get_secret_key())
            current_employee = Employee.query.get(decoded["id"])

            return f(current_employee=current_employee, *args, **kwargs)
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "expired token"}), 401
        except Exception:
            return jsonify({"error": "invalid token"}), 401

    return wrapper
