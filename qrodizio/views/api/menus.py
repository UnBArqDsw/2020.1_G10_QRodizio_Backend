from flask import Blueprint, jsonify, abort, request
from qrodizio.models.menus import Menu, Item
from qrodizio.builders import menus_builder
from qrodizio.ext.database import db
from qrodizio.utils.dbutils import add_commit_session, delete_commit_session

menus_bp = Blueprint("menus", __name__, url_prefix="/menus")


def _menu_to_dict(menu):
    """parses a menu and its items into a dict"""
    data = menu.to_dict()
    items_data = [item.to_dict() for item in menu.items]
    data["items"] = items_data

    return data


def _verify_and_update_is_daily(menu):
    """Let only the given menu to have is_daily as true
    any other menu with is_daily that is not false will have
    it set to false
    """
    menus = Menu.query.filter_by(is_daily=True)
    menus = [m for m in menus if m.id != menu.id]

    if len(menus) == 0:
        return

    for m in menus:
        m.is_daily = False

    db.session.bulk_save_objects(menus)
    db.session.commit()


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

    if menu.is_daily:
        _verify_and_update_is_daily(menu)

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
    
    add_commit_session(db, menu)

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
    
    add_commit_session(db, menu)
    
    if menu.is_daily:
        _verify_and_update_is_daily(menu)

    return jsonify({"menu": _menu_to_dict(menu)}), 202


@menus_bp.route("/<int:menu_id>", methods=["DELETE"])
def delete_menu(menu_id):
    menu = Menu.query.get_or_404(menu_id)
    delete_commit_session(db, menu)
    
    return jsonify({"success": "menu deleted"}), 202


@menus_bp.route("/<int:menu_id>/<int:item_id>", methods=["DELETE"])
def delete_item_menu(menu_id, item_id):
    menu = Menu.query.get_or_404(menu_id)
    item = Item.query.get_or_404(item_id)

    if item not in menu.items:
        return jsonify({"error": "Item does not belong to menu"}), 406

    delete_commit_session(db, item)
    
    return jsonify({"success": "menu item deleted"}), 202
