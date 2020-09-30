from flask import Blueprint, jsonify

home_bp = Blueprint("home", __name__, url_prefix="/")

@home_bp.route("/", methods=["GET"])
def home():
    return jsonify({'status': 'api working '}), 200
