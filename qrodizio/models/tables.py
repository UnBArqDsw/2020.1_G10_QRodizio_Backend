from sqlalchemy_serializer import SerializerMixin
from uuid import uuid1

from qrodizio.ext.database import db
from qrodizio.qrcode import qrcode_builder, qrcode_table_url_builder


class TableSession(db.Model, SerializerMixin):
    __tablename__ = "tables_sessions"
    serialize_rules = ("-demands",)

    id = db.Column(db.Integer, primary_key=True)
    created_on = db.Column(db.DateTime, default=db.func.now())
    url = db.Column(db.String(80), unique=True, nullable=False)
    demands = db.relationship("Demand")
    closed = db.Column(db.Boolean, default=False)
    table_id = db.Column(
        db.Integer, db.ForeignKey("customer_tables.id"), nullable=False
    )
    table = db.relationship("CustomerTable", back_populates="sessions")
    payment = db.relationship("PaymentsDemand")

    def get_total(self):
        value = 0

        for demand in self.demands:
            value += demand.total_value()

        return self.value

    def create(self):
        if self.url == None:
            self.url = self.generate_url()

        db.session.add(self)
        db.session.commit()

        return self

    def generate_url(self):
        part = str(uuid1())
        return f"{self.table_id}-{part}"


class CustomerTable(db.Model, SerializerMixin):
    __tablename__ = "customer_tables"
    serialize_rules = (
        "-sessions",
        "-qrcode",
        "-payment",
    )

    id = db.Column(db.Integer, primary_key=True)
    qrcode = db.Column(db.Text, nullable=True)
    identifier = db.Column(db.String(80), unique=True, nullable=False)
    sessions = db.relationship("TableSession")
    payments = db.relationship("PaymentsDemand")

    def create(self):
        db.session.add(self)
        db.session.commit()

        url = qrcode_table_url_builder(self.id)
        self.qrcode = qrcode_builder(url)

        db.session.add(self)
        db.session.commit()

        return self
