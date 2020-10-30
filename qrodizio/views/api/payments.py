from flask import Blueprint, jsonify, abort, request
from qrodizio.ext.authentication import auth_required
from qrodizio.models.payments import PaymentsDemand
from qrodizio.ext.database import db


payments_bp = Blueprint("payments", __name__, url_prefix="/payments")



@payments_bp.route("/", methods=["GET"])
def list_all_payments():
    payment_query = PaymentsDemand.query.all()

    payments = [payment.to_dict() for payment in payment_query]

    return jsonify({"payments": payments}), 200

@payments_bp.route("/<payment_id>", methods=["PUT"])
def change_payMethod(payMethod, payment_id):
    payment = PaymentsDemand.query.get_or_404(demand_id)
    payMethod = request.json["payMethod"]

    payment.payMethod = payMethod
    db.session.add(payment)
    db.session.commit()

    return jsonify({"payment": payment.to_dict()}), 202

