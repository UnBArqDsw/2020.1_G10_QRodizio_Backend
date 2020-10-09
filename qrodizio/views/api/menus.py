from flask import Blueprint, jsonify, abort
from qrodizio.models.menus import Menu

menus_bp = Blueprint("menus", __name__, url_prefix="/menus")


@menus_bp.route("/", methods= ["GET"])
def listar():
  menus_query = Menu.query.all()
  menus = [menus.to_dict() for menus in menus_query]

  return jsonify({"menus": menus}), 200

@menus_bp.route("/criar", methods= ["POST"])
def criar():  
  ...

@menus_bp.route("/editar", methods= ["PUT"])
def editar():  
  ... 

@menus_bp.route("/deletar", methods= ["DELETE"])
def deletar():  
  ...
