from flask import Blueprint, jsonify, abort, request
from qrodizio.ext.authentication import auth_required
from qrodizio.models.demands import Demand, DemandStatus
from qrodizio.builders import demand_builder
from qrodizio.ext.database import db
from qrodizio.utils.dbutils import dbFacade



demands_bp = Blueprint("demands", __name__, url_prefix="/demands")


# TODO: temporary route while issue is under development. MUST be removed later
@demands_bp.route("/", methods=["GET"])
def list_all_demands():
    demand_query = Demand.query.all()

    demands = [demand.to_dict() for demand in demand_query]

    return jsonify({"demands": demands}), 200


@demands_bp.route("/status", methods=["GET"])
def list_all_demand_status():
    status = [d.name for d in DemandStatus]

    return jsonify({"status": status}), 200


@demands_bp.route("/<demand_status>", methods=["GET"])
def list_demands_by_status(demand_status):
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
    if (request.json) == None:
        return jsonify({"Error": 0}), 500
    demand = demand_builder(**request.json)
    demand.create()
    return jsonify({"demand": demand.to_dict()}), 201


@demands_bp.route("/<demand_id>/status", methods=["PUT"])
def change_status_demand(demand_id):
    demand = Demand.query.get_or_404(demand_id)
    status = request.json["status"]

    demand.status = status
    dbFacade.add_commit_session(db, demand)

    return jsonify({"demand": demand.to_dict()}), 202

@demands_bp.route("/<demand_id>", methods=["DELETE"])
def delete_demand(demand_id):
    demand = Demand.query.get_or_404(demand_id)
    dbFacade.delete_commit_session(db, demand)

    return jsonify({"sucess":"deleted demand"}), 202

@demands_bp.route("/<demand_id>/cancel", methods=["PUT"])
def cancel_demand(demand_id):
    demand = Demand.query.get_or_404(demand_id)

    if demand.status != DemandStatus.waiting:
        return jsonify({"error": "Demand status is not waiting"}), 406

    demand.status = DemandStatus.canceled
    dbFacade.add_commit_session(db, demand)

    return jsonify({"success": "demand canceled"}), 202

