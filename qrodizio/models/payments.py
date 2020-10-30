from sqlalchemy_serializer import SerializerMixin
from qrodizio.ext.database import db



class PaymentsDemand(db.Model, SerializerMixin):
    
    __tablename__ = "paymentsDemand"

    id = db.Column(db.Integer, primary_key=True)
    created_on = db.Column(db.DateTime, default=db.func.now())
    demands = db.relationship("Demand") # 1 to n
    table_id = db.Column(db.Integer, db.ForeignKey("customer_tables.id"), nullable=False)
    customer_tables = db.relationship("CustomerTable", backref="paymentsDemand")
    payMethod = db.Column(db.String(80), nullable=False)
   
   
   #payment = db.relationship("CustomerPayment", back_populates="paymentsDemand")

    def create(self):
        db.session.add(self)
        db.session.commit()

        return self
  
# class CostumerPayment(db.Model, SerializerMixin):
#     __tablename__ = "costumer_payment"

#     id = db.Column(db.Integer, primary_key=True)
#     payMethod = db.Column(db.String(80), nullable=False)
#     sessions = db.relationship("PaymentSession")

#     def create(self):
#         db.session.add(self)
#         db.session.commit()

#         return self
