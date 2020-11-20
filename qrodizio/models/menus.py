from sqlalchemy_serializer import SerializerMixin
from qrodizio.ext.database import db


association_table = db.Table(  # Define an N to N association
    "Menu_and_Item_association",
    db.metadata,
    db.Column("menu_id", db.Integer, db.ForeignKey("menus.id")),
    db.Column("item_id", db.Integer, db.ForeignKey("items.id")),
)


class Menu(db.Model, SerializerMixin):
    __tablename__ = "menus"
    serialize_rules = ("-items",)  # prevent recursion error on to_dict

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), nullable=False)
    description = db.Column(db.String(140), nullable=True)
    is_daily = db.Column(db.Boolean, default=False)
    items = db.relationship(
        "Item",
        secondary=association_table,
        back_populates="menus",
    )

    def create(self):
        db.session.add(self)
        db.session.commit()

        return self


class Item(db.Model, SerializerMixin):
    __tablename__ = "items"
    serialize_rules = (
        "-menus",
        "-demands",
    )  # prevent recursion error on to_dict

    id = db.Column(db.Integer, primary_key=True)
    menus = db.relationship("Menu", secondary=association_table, back_populates="items")
    name = db.Column(db.String(80), nullable=False, unique=True, index=True)
    description = db.Column(db.String(140), nullable=True)
    value = db.Column(db.Float(2), nullable=False)
    demands = db.relationship(
        "Demand",
        cascade="all, delete-orphan",
    )

    def create(self):
        db.session.add(self)
        db.session.commit()

        return self
