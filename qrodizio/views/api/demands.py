from flask import Blueprint, jsonify, abort
from qrodizio.ext.authentication import auth_required
from qrodizio.models.demands import Demand, DemandStatus
from qrodizio.ext.database import db


demands_bp = Blueprint("demands", __name__, url_prefix="/demands")


@demands_bp.route("/", methods=["GET"])
def list_all_demands():
    demand_query = Demand.query.all()

    demands = [demand.to_dict() for demand in demand_query]

    return jsonify({"demands": demands}), 200


@demands_bp.route("/<demand_status>", methods=["GET"])
@auth_required()
def list_demands_by_status(current_employee, demand_status):
    demand_query = Demand.query.filter_by(status=demand_status)

    demands = [demand.to_dict() for demand in demand_query]

    return jsonify({"demands": demands}), 200


"""
TODO: After Table is code is done
@demands_bp.route("/<int:table_id>", methods=["GET"])
def list_table_demands(demand_status):
    pass
"""


@demands_bp.route("/<demand_id>", methods=["GET"])
def get_single_demand(demand_id):
    demand_query = Demand.query.get_or_404(demand_id)
    return jsonify({"demand": demand_query.to_dict()}), 200


@demands_bp.route("/", methods=["POST"])
def new_demand():
    demand = demand_builder(**request.json)
    demand.create()

    return jsonify({"demand": demand.to_dict()}), 201


@demands_bp.route("/<demand_id>/status", methods=["PUT"])
@auth_required()
def change_status_demand(current_employee, demand_id):
    demand = Demand.query.get_or_404(demand_id)
    status = request.json["status"]

    demand.status = status
    db.session.add(demand)
    db.session.commit()

    return jsonify({"demand": demand.to_dict()}), 202


@demands_bp.route("/<demand_id>/cancel", methods=["PUT"])
def cancel_demand(demand_id):
    demand = Demand.query.get_or_404(demand_id)

    if demand.status != DemandStatus.waiting:
        return jsonify({"error": "Demand status is not waiting"}), 406

    demand.status = DemandStatus.canceled
    db.session.add(demand)
    db.session.commit()

    return jsonify({"success": "demand canceled"}), 202
