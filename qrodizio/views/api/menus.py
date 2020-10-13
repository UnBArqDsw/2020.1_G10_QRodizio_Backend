from flask import Blueprint, jsonify, abort, request
from qrodizio.models.menus import Menu, Item
from qrodizio.util import menus_builder
from qrodizio.ext.database import db

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
    name = request.json.get("name")
    description = request.json.get("description", None)
    is_daily = request.json.get("is_daily", False)
    items = request.json.get("items")

    menu = menus_builder(
        name=name, description=description, is_daily=is_daily, items=items
    )
    menu.create()

    return jsonify({"menu": _menu_to_dict(menu)}), 201


@menus_bp.route("/<int:menu_id>", methods=["POST"])
def add_item_menu(menu_id):
    menu = Menu.query.get_or_404(menu_id)
    name = menu.name
    description = menu.description
    is_daily = menu.is_daily
    items = request.json.get("items")

    menu = menus_builder(
        id=menu_id, name=name, description=description, is_daily=is_daily, items=items
    )
    db.session.add(menu)
    db.session.commit()

    return jsonify({"menu": _menu_to_dict(menu)}), 202


@menus_bp.route("/<int:menu_id>", methods=["PUT"])
def edit_menu(menu_id):
    menu = Menu.query.get_or_404(menu_id)
    name = request.json.get("name", None)
    description = request.json.get("description", None)
    is_daily = request.json.get("is_daily", False)
    items = request.json.get("items", [])

    menu = menus_builder(
        id=menu_id, name=name, description=description, is_daily=is_daily, items=items
    )
    db.session.add(menu)
    db.session.commit()

    return jsonify({"menu": _menu_to_dict(menu)}), 202


@menus_bp.route("/<int:menu_id>", methods=["DELETE"])
def delete_menu(menu_id):
    menu = Menu.query.get_or_404(menu_id)
    db.session.delete(menu)
    db.session.commit()
    return jsonify({"success": "menu deleted"}), 202


@menus_bp.route("/<int:menu_id>/<int:item_id>", methods=["DELETE"])
def delete_item_menu(menu_id, item_id):
    menu = Menu.query.get_or_404(menu_id)
    item = Item.query.get_or_404(item_id)

    if item not in menu.items:
        return jsonify({"error": "Item does not belong to menu"}), 406

    db.session.delete(item)
    db.session.commit()
    return jsonify({"success": "menu item deleted"}), 202
