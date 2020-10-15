from sqlalchemy_serializer import SerializerMixin
from qrodizio.ext.database import db


class CostumerTable(db.Model, SerializerMixin):
    __tablename__ = "costumer_tables"

    id = db.Column(db.Integer, primary_key=True)
    costumers = db.Column(db.Integer)

    def create(self):
        db.session.add(self)
        db.session.commit()

        return self
        
