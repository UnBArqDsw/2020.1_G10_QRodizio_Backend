from sqlalchemy_serializer import SerializerMixin
from sqlalchemy_imageattach.entity import image_attachment
from qrodizio.ext.database import db
#from qrodizio.views.api import qrcode


association_costumer_table = db.Table(  # Define an N to N association
    "Costumer_Table_and_Client_association_teste",
    db.metadata,
    db.Column("costumer_table_id", db.Integer, db.ForeignKey("CostumerTable.id")),
    db.Column("client_id", db.Integer, db.ForeignKey("Client.id")),
)


class CostumerTable(db.Model, SerializerMixin):
    __tablename__ = "CostumerTable"

    id = db.Column(db.Integer, primary_key=True)
    costumers_quantity = db.Column(db.Integer)
    #qrcode = image_attachment("QRCodeTable")
    url = db.Column(db.String(255), unique=True, nullable=False)
    client = db.relationship("Client", secondary=association_costumer_table, backref="CostumerTable")

    def create(self):
        db.session.add(self)
        db.session.commit()

        return self

class Client(db.Model, SerializerMixin):
    __tablename__ = "Client"

    id = db.Column(db.Integer, primary_key=True)
   
    costumer_table = db.relationship("CostumerTable", secondary=association_costumer_table, backref="Client")
    
    def create(self):
        db.session.add(self)
        db.session.commit()

        return self