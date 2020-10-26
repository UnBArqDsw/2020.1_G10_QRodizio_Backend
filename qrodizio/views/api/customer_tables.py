from flask import Blueprint, jsonify, abort, request
from qrodizio.ext.database import db
from qrodizio.models.tables import CustomerTable, TableSession
from qrodizio.util import customer_tables_builder

tables_bp = Blueprint("tables", __name__, url_prefix="/tables")


def _table_to_dict(customer_table):
    """parses a customer table and its clients into a dict"""
    data = customer_table.to_dict()

    sessions = TableSession.query.filter_by(table_id=customer_table.id)
    last_session = sessions.order_by(TableSession.id.desc()).first()

    data["last_session"] = last_session.to_dict()
    del data["last_session"]["table"]
    data["total_demands"] = len(last_session.demands)

    return data


@tables_bp.route("/", methods=["GET"])
def get_tables():
    tables_query = CustomerTable.query.all()
    tables = [_table_to_dict(table) for table in tables_query]

    return jsonify({"tables": tables}), 200


@tables_bp.route("/<int:customer_table_id>", methods=["GET"])
def get_single_customer_table(customer_table_id):
    table = CustomerTable.query.get_or_404(customer_table_id)

    return jsonify(_table_to_dict(table)), 200


@tables_bp.route("/", methods=["POST"])
def create_customer_table():
    customers_quantity = request.json.get("customers_quantity")
    qrcode = request.json.get("qrcode")
    url = request.json.get("url")
    client = request.json.get("client")
    status = request.json.get("status")
    code = request.json.get("code")

    customer_table = customer_tables_builder(
        customers_quantity=customers_quantity,
        qrcode=qrcode,
        url=url,
        client=client,
        status=status,
        code=code,
    )
    customer_table.create()

    return jsonify({"customer_table": _customer_table_to_dict(customer_table)}), 201


@tables_bp.route("/<int:customer_table_id>", methods=["DELETE"])
def delete_customer_table(customer_table_id):
    customer_table = CustomerTable.query.get_or_404(customer_table_id)
    db.session.delete(customer_table)
    db.session.commit()
    return jsonify({"success": "table deleted"}), 202
