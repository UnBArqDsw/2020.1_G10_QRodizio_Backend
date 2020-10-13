import enum

from sqlalchemy_serializer import SerializerMixin
from qrodizio.ext.database import db


class User(db.Model):
    __abstract__ = True

    # created_on = db.Column(db.DateTime, default=db.func.now())
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)

    def create(self):
        db.session.add(self)
        db.session.commit()

        return self

    def __repr__(self):
        return "" % self.id


class EmployeeRole(enum.Enum):
    basic = 0
    manager = 1


class Employee(User, SerializerMixin):
    __tablename__ = "employees"
    serialize_rules = ("-password",)

    name = db.Column(db.String(255), nullable=False)
    role = db.Column(db.Enum(EmployeeRole), nullable=False, default=EmployeeRole.basic)
