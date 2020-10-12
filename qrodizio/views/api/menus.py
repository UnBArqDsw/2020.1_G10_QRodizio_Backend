from flask import Blueprint, jsonify, abort
from qrodizio.models.menus import Menu

menus_bp = Blueprint("menus", __name__, url_prefix="/menus")


def _menu_to_dict(menu):
    """parses a menu and its items into a dict"""
    data = menu.to_dict()
    items_data = [item.to_dict() for item in menu.items]
    data["items"] = items_data

    return data


@menus_bp.route("/", methods=["GET"])
def list_menus():
    menus_query = Menu.query.all()
    menus = [_menu_to_dict(menu) for menu in menus_query]

    return jsonify({"menus": menus}), 200


@menus_bp.route("/<int:menu_id>", methods=["GET"])
def get_single_menu(menu_id):
    menu_query = Menu.query.get(menu_id)

    if menu_query == None:
        return jsonify({"error": "Not found"}), 404

    menu = _menu_to_dict(menu_query)

    return jsonify({"menu": menu}), 200


@menus_bp.route("/", methods=["POST"])
def create_menus():
    return jsonify({"error": "Not Implemented"}), 501


@menus_bp.route("/", methods=["PUT"])
def edit_menu():
    return jsonify({"error": "Not Implemented"}), 501


@menus_bp.route("/", methods=["DELETE"])
def delete_menu():
    return jsonify({"error": "Not Implemented"}), 501
