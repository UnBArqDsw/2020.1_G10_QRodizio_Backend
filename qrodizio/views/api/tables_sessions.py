from flask import Blueprint, jsonify, abort, request
from qrodizio.ext.database import db
from qrodizio.models.tables import CustomerTable, TableSession
from qrodizio.models.demands import Demand

from qrodizio.ext.authentication import auth_required
from qrodizio.builders import customer_tables_builder
from qrodizio.builders import tables_sessions_builder

sessions_bp = Blueprint("sessions", __name__, url_prefix="/sessions")


def _session_to_dict(session, has_demads=False):
    data = session.to_dict()

    if has_demads:
        data["demands"] = [demand.to_dict() for demand in session.demands]

    return data


@sessions_bp.route("/", methods=["GET"])
def list_demands():
    query = TableSession.query.filter_by(closed=False).all()
    sessions = [_session_to_dict(session) for session in query]

    return jsonify({"sessions": sessions}), 200


@sessions_bp.route("/<int:id>", methods=["GET"])
def get_single_demand_by_id(id):
    query = TableSession.query.get_or_404(id)
    session = _session_to_dict(query, has_demads=True)

    return jsonify({"session": session}), 200

@sessions_bp.route("/", methods=["POST"])
def create_session():
    url = request.json.get("url")
    closed = request.json.get("closed")
    table_id = request.json.get("table_id")

    table_sessions = tables_sessions_builder(
        url=url,
        closed=closed,
        table_id=table_id
    )
    table_sessions.create()

    return jsonify({"table_sessions": "ok"}), 201

@sessions_bp.route("/url/<url>", methods=["GET"])
def get_single_demand_by_url(url):
    query = TableSession.query.filter_by(url=url).first()

    if query == None:
        return jsonify({"error": "Session not found"}), 404

    session = _session_to_dict(query, has_demads=True)

    return jsonify({"session": session}), 200

@sessions_bp.route("/<int:id>", methods=["PUT"])
def update_table_session(id):
    table = TableSession.query.get_or_404(id)
    status = request.json["closed"]
    
    table.closed = status
    db.session.add(table)
    db.session.commit()

    return jsonify({"table": table.to_dict()}), 200

@sessions_bp.route("/<int:id>/close", methods=["GET"])
def end_session_and_get_total(id):
    demand_query = Demand.query.filter_by(session_id=id)
    demands = [demand.to_dict() for demand in demand_query]
    total = 0
    for demand in demands: 
        total = total + (demand['item']['value'] * demand['quantity'])
    
    return jsonify({"table": total}), 200

    