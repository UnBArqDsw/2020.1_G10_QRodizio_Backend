import enum
import uuid

from qrodizio.ext.database import db
from sqlalchemy_serializer import SerializerMixin


class Customer:
    id = uuid.uuid1()
    name = ""


class DemandStatus(enum.Enum):
    waiting = 0
    processing = 1
    done = 2
    canceled = 3


class Demand(db.Model):
    id =  db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer, nullable=False, default=1)
    status = db.Column(db.Enum(DemandStatus), nullable=False, default=DemandStatus.waiting)
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'))
    item = db.relationship("Item", back_populates="demands")
    customer = db.Column(db.String(160), nullable=False) # c.name + '|' + c.id

    def create(self):
        db.sessioForeignKeyn.add(self)
        db.session.commit()

        return self
    
    def total_value(self):
        return self.item.value * self.quantity
