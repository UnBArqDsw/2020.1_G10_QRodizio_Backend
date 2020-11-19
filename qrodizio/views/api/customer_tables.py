from flask import Blueprint, jsonify, request, redirect

from qrodizio.ext.database import db
from qrodizio.ext.configuration import get_config

from qrodizio.models.tables import CustomerTable, TableSession
from qrodizio.builders import customer_tables_builder, table_session_builder
from qrodizio.utils.dbutils import dbFacade

tables_bp = Blueprint("tables", __name__, url_prefix="/tables")


def _get_table_last_session(customer_table_id: int) -> TableSession:
    """Given a table id, query for its last session
    may return None
    """
    sessions = TableSession.query.filter_by(table_id=customer_table_id)
    last_session = sessions.order_by(TableSession.id.desc()).first()

    return last_session


def _table_to_dict(customer_table):
    """parses a customer table and its clients into a dict"""
    data = customer_table.to_dict()

    last_session = _get_table_last_session(customer_table.id)

    if last_session:
        data["last_session"] = last_session.to_dict()
        del data["last_session"]["table"]

    data["total_demands"] = len(last_session.demands) if last_session else 0

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


@tables_bp.route("/<int:customer_table_id>/qrcode", methods=["GET"])
def get_customer_table_qrcode(customer_table_id):
    """Get the qrcode from a table"""
    table = CustomerTable.query.get_or_404(customer_table_id)

    return jsonify({"qrcode": table.qrcode}), 200


@tables_bp.route("/", methods=["POST"])
def create_customer_table():
    customer_table = customer_tables_builder(**request.json)
    customer_table.create()

    return jsonify({"customer_table": _table_to_dict(customer_table)}), 201


@tables_bp.route("/<int:customer_table_id>", methods=["DELETE"])
def delete_customer_table(customer_table_id):
    customer_table = CustomerTable.query.get_or_404(customer_table_id)
    
    dbFacade.delete_commit_session(db, customer_table)

    return jsonify({"success": "table deleted"}), 202


@tables_bp.route("/<int:customer_table_id>/session", methods=["GET"])
def customer_table_get_session_or_create(customer_table_id):
    customer_table = CustomerTable.query.get_or_404(customer_table_id)

    last_session = _get_table_last_session(customer_table.id)  # may return None

    if last_session == None or last_session.closed:  # create a new session
        data = {
            "closed": False,
            "demands": [],
            "table": customer_table,
            "table_id": customer_table.id,
            "url": None,  # url will be generated on .create()
        }
        last_session = table_session_builder(**data)
        last_session.create()

    front_base_url = get_config("FRONT_BASE_URL")

    redirect_to_url = f"{front_base_url}/table/{last_session.url}"

    return redirect(redirect_to_url, code=302)
