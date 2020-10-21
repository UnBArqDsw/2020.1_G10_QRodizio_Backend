from sqlalchemy_serializer import SerializerMixin
from sqlalchemy_imageattach.entity import image_attachment
from qrodizio.ext.database import db
#from qrodizio.views.api import qrcode


association_costumer_table = db.Table(  # Define an N to N association
    "Costumer_Table_and_Client_association_teste",
    db.metadata,
    db.Column("costumer_table_id", db.Integer, db.ForeignKey("costumer_table.id")),
    db.Column("client_id", db.Integer, db.ForeignKey("client.id")),
)


class CostumerTable(db.Model, SerializerMixin):
    __tablename__ = "costumer_table"
    serialize_rules = ("-clients",)  # prevent recursion error on to_dict

    id = db.Column(db.Integer, primary_key=True)
    costumers_quantity = db.Column(db.Integer)
    #qrcode = image_attachment("QRCodeTable")
    url = db.Column(db.String(255), unique=True, nullable=False)
    status = db.Column(db.Boolean, default=False)
    code = db.Column(db.Integer, default=False)
    clients = db.relationship("Client", secondary=association_costumer_table, backref="costumer_table")

    def create(self):
        db.session.add(self)
        db.session.commit()

        return self

class Client(db.Model, SerializerMixin):
    __tablename__ = "client"
    serialize_rules = ("-costumer_tables",)  # prevent recursion error on to_dict

    id = db.Column(db.Integer, primary_key=True)
   
    costumer_tables = db.relationship("CostumerTable", secondary=association_costumer_table, backref="client")
    
    def create(self):
        db.session.add(self)
        db.session.commit()

        return self