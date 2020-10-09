from sqlalchemy_serializer import SerializerMixin
from qrodizio.ext.database import db


class Menu(db.Model):
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(255), nullable=False)
    #types = db.relationship('Type', backref= 'menu', lazy =True)

class Type(Menu, SerializerMixin):#Menu, SerializerMixin
    __table_args__ = {'extend_existing': True}
 
    id = db.Column(db.Integer, primary_key=True)
    menu_id = db.Column(db.Integer, db.ForeignKey('menu.id'), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    #itens = db.relationship('Item', backref= 'type', lazy =True)  
      
class Item(Type, SerializerMixin):#Type, SerializerMixin
    __table_args__ = {'extend_existing': True}
 
    id = db.Column(db.Integer, primary_key=True)
    type_id = db.Column(db.Integer, db.ForeignKey('type.id'), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    value = db.Column(db.Float(2), nullable=False)