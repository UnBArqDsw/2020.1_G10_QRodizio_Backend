from flask import Blueprint, jsonify, abort, request
from qrodizio.ext.authentication import auth_required
from qrodizio.models.payments import PaymentsDemand
from qrodizio.builders import payments_demand_builder
from qrodizio.ext.database import db


payments_bp = Blueprint("payments", __name__, url_prefix="/payments")

def _payment_to_dict(payment):
    """parses a payment into a dict"""
    data = payment.to_dict()
    payments = PaymentsDemand.query.filter_by(payment_id = payments_demands.id)

    data["payments"] = payments.to_dict()

    return data

@payments_bp.route("/", methods=["GET"])
def list_all_payments():
    payment_query = PaymentsDemand.query.all()

    payments = [payment.to_dict() for payment in payment_query]

    return jsonify({"payments": payments}), 200


@payments_bp.route("/<int:payment_id>", methods=["GET"])
def get_single_payment(payment_id):
    payment_query = PaymentsDemand.query.get_or_404(payment_id)
    return jsonify({"payments": payment_query.to_dict()}), 200
  
  

@payments_bp.route("/<int:payment_id>", methods=["PUT"])
def edit_pay_method(payment_id):
    payment = PaymentsDemand.query.get_or_404(payment_id)
    pay_method = request.json.get("pay_method")
    session_id = payment.session_id
    table_id = payment.table_id
    
    payment = payments_demand_builder(
        id=payment_id, pay_method=pay_method, session_id=session_id, table_id=table_id
    )
    db.session.add(payment)
    db.session.commit()

    return jsonify({"payment": payment.to_dict()}), 202

    
