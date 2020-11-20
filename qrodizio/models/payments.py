import enum

from sqlalchemy_serializer import SerializerMixin
from qrodizio.ext.database import db

class PaymentType(enum.Enum):
    money = 0
    card = 1
    both = 2


class PaymentsDemand(db.Model, SerializerMixin):
    __tablename__ = "payments_demands"
    serialize_rules = ("-session","-table",)

    id = db.Column(db.Integer, primary_key=True)
    created_on = db.Column(db.DateTime, default=db.func.now())
    table_id = db.Column(db.Integer, db.ForeignKey("customer_tables.id"), nullable=False)
    table = db.relationship("CustomerTable", back_populates="payments")
    pay_method = db.Column(db.Enum(PaymentType), nullable=False, default=PaymentType.money)
    session_id = db.Column(db.Integer, db.ForeignKey("tables_sessions.id"), nullable=False)
    session = db.relationship("TableSession", back_populates="payment")
    #demands = db.relationship("Demand", backref="paymentsDemands") # 1 to n
    #customer_tables = db.relationship("CustomerTable", backref="paymentsDemands")
    #payment = db.relationship("CustomerPayment", back_populates="paymentsDemand")

    def total_value(self):
        return self.session.get_total()

    def create(self):
        db.session.add(self)
        db.session.commit()

        return self
  
# class customerPayment(db.Model, SerializerMixin):
#     __tablename__ = "customer_payment"

#     id = db.Column(db.Integer, primary_key=True)
#     payMethod = db.Column(db.String(80), nullable=False)
#     sessions = db.relationship("PaymentSession")

#     def create(self):
#         db.session.add(self)
#         db.session.commit()

#         return self
