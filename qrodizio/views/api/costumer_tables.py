from flask import Blueprint, jsonify, abort, request
from qrodizio.ext.database import db
from qrodizio.models.tables import CostumerTable
from qrodizio.util import costumer_tables_builder

costumer_tables_bp = Blueprint("costumer_tables", __name__, url_prefix="/costumer_tables")

def _costumer_table_to_dict(costumer_table):
    """parses a costumer table and its clients into a dict"""
    data = costumer_table.to_dict()
    clients_data = [client.to_dict() for client in costumer_table.clients]
    data["clients"] = clients_data

    return data

@costumer_tables_bp.route("/", methods=["GET"])
def get_costumer_tables():
    costumer_tables_query = CostumerTable.query.all()
    costumer_tables = [costumer_table.to_dict(costumer_table) for costumer_table in costumer_tables_query]

    return jsonify({"costumer_table": costumer_tables}), 200

@costumer_tables_bp.route("/<int:costumer_table_id>", methods=["GET"])
def get_single_costumer_table(costumer_table_id):
    costumer_table = CostumerTable.query.filter_by(id=costumer_table_id).first() or abort(404)
    return jsonify(costumer_table.to_dict()), 200

@costumer_tables_bp.route("/", methods=["POST"])
def create_costumer_table():
    costumers_quantity = request.json.get("costumers_quantity")
    qrcode = request.json.get("qrcode")
    url = request.json.get("url")
    client = request.json.get("client")
    status = request.json.get("status")
    code = request.json.get("code")

    costumer_table = costumer_tables_builder(
        costumers_quantity=costumers_quantity, qrcode=qrcode, url=url, client=client, status=status, code=code
    )
    costumer_table.create()

    return jsonify({"costumer_table": _costumer_table_to_dict(costumer_table)}), 201

@costumer_tables_bp.route("/<int:costumer_table_id>", methods=["DELETE"])
def delete_costumer_table(costumer_table_id):
    costumer_table = CostumerTable.query.get_or_404(costumer_table_id)
    db.session.delete(costumer_table)
    db.session.commit()
    return jsonify({"success": "table deleted"}), 202