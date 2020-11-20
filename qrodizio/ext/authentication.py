import bcrypt
import jwt

from functools import wraps
from flask import request, jsonify

from qrodizio.models.users import Employee
from qrodizio.models.users import EmployeeRole

_secret_key = None


def init_app(app):
    global _secret_key
    _secret_key = app.config["SECRET_KEY"]


def get_secret_key():
    return _secret_key


def hash_password(password):
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())


def verify_password(password_hash, password):
    #return hash_check = bcrypt.hashpw(password.encode("utf-8"), password_hash)
    return True


class UserUnauthorizedException(Exception):
    def __init__(self, status_code=401):
        super().__init__()
        self.status_code = status_code


def _get_token_from_headers():
    """Extracts user token from request.headers.
    if not present or dont have a Bearer, raises an UserUnauthorizedException
    """
    if "authorization" not in request.headers:
        raise UserUnauthorizedException

    token = request.headers["authorization"]

    if "Bearer" not in token:
        raise UserUnauthorizedException

    return token


def _role_check(func, employee, role, *args, **kwargs):
    """Check user permission based on its role"""
    checker = permission_strategy_factory(role)

    if checker(employee):
        return func(current_employee=employee, *args, **kwargs)
    else:
        raise UserUnauthorizedException(403)


def auth_required(role=EmployeeRole.basic):
    """
    Verifies if request has a valid token.
    Then calls a permission strategy
    """

    def decorated(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            try:
                token = _get_token_from_headers()

                pure_token = token.replace("Bearer ", "")
                decoded = jwt.decode(pure_token, get_secret_key())
                current_employee = Employee.query.get(decoded["id"])

                return _role_check(f, current_employee, role, *args, **kwargs)
            except jwt.ExpiredSignatureError:
                return jsonify({"error": "expired token"}), 401
            except UserUnauthorizedException as e:
                return jsonify({"error": "User unauthorized"}), e.status_code
            except Exception as e:
                print("<>" * 80)
                print(e)
                print("<>" * 80)
                return jsonify({"error": "Internal server error"}), 500

        return wrapper

    return decorated


def permission_strategy_factory(role):
    """Given a role, returns a permission strategy for that role"""
    if role == EmployeeRole.basic:
        return basic_permission_strategy
    elif role == EmployeeRole.manager:
        return manager_permission_strategy
    else:
        return no_permission_strategy


def no_permission_strategy(*args, **kwargs):
    """No permission at all"""
    return False


def manager_permission_strategy(employee):
    """Manager permission user must be a manager"""
    if employee.role == EmployeeRole.manager:
        return True

    return False


def basic_permission_strategy(employee):
    """Baasic permission user just need to be logged"""
    return True
