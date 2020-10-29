from sqlalchemy_serializer import SerializerMixin
from qrodizio.ext.database import db

class payment(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  created_on = db.Column(db.DateTime, default=db.func.now())
  table_session = db.relationship("TableSession", back_populates="demands")
  demand_user = db.relationship("Demand", back_populates="demands")
  

  def create(self):
    db.session.add(self)
        db.session.commit()

        return self
