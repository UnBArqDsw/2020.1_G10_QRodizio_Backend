import enum

from qrodizio.ext.database import db
from sqlalchemy_serializer import SerializerMixin
from qrodizio.models.payments import PaymentsDemand

class DemandStatus(enum.Enum):
    waiting = 0
    processing = 1
    done = 2
    canceled = 3


class Demand(db.Model, SerializerMixin):
    __tablename__ = "demands"
    id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer, nullable=False, default=1)
    status = db.Column(
        db.Enum(DemandStatus), nullable=False, default=DemandStatus.waiting
    )
    item_id = db.Column(db.Integer, db.ForeignKey("items.id"), nullable=False)
    item = db.relationship("Item", back_populates="demands")
    session_id = db.Column(
        db.Integer, db.ForeignKey("tables_sessions.id"), nullable=False
    )
    table_session = db.relationship("TableSession", back_populates="demands")
    customer = db.Column(db.String(120), nullable=False)
    demands = db.Column(
        db.Integer, db.ForeignKey("paymentsDemand.id"), nullable=False
    )
    def create(self):
        db.session.add(self)
        db.session.commit()

        return self

    def total_value(self):
        return self.item.value * self.quantity
