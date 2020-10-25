from sqlalchemy_serializer import SerializerMixin
from qrodizio.ext.database import db


class CustomerTable(db.Model, SerializerMixin):
    __tablename__ = "customer_tables"
    serialize_rules = ("-demands",)

    id = db.Column(db.Integer, primary_key=True)
    qrcode = db.Column(db.String(255), unique=True, nullable=False)
    demands = db.relationship("Demand")

    def create(self):
        db.session.add(self)
        db.session.commit()

        return self
