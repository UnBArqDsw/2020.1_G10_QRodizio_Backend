from flask import Blueprint, jsonify, abort, request
from qrodizio.ext.database import db
from qrodizio.models.tables import CostumerTable

costumer_tables_bp = Blueprint("costumer_tables", __name__, url_prefix="/costumer_tables")

@costumer_tables_bp.route("/", methods=["GET"])
def get_costumer_tables():
    costumer_tables_query = CostumerTable.query.all()
    costumer_tables = [costumer_table.to_dict(costumer_table) for costumer_table in costumer_tables_query]

    return jsonify({"costumer_tables": costumer_tables}), 200

@costumer_tables_bp.route("/<int:costumer_table_id>", methods=["GET"])
def get_single_costumer_table(costumer_table_id):
    costumer_table = CostumerTable.query.filter_by(id=costumer_table_id).first() or abort(404)
    return jsonify(costumer_table.to_dict()), 200