from qrodizio.ext.database import db
from qrodizio.populate_data import (
    get_employees,
    get_menus,
    get_demands,
    get_costumer_tables,
)


def create_db():
    """Creates database"""
    db.create_all()


def drop_db():
    """Cleans database"""
    db.drop_all()


def populate_db():
    """Populate db with employees sample data"""
    employees = get_employees()

    db.session.bulk_save_objects(employees)
    db.session.commit()


def populate_menus():
    """Populate db with menus sample data"""
    menus = get_menus()

    # can't just bulk_save_objects
    # need to save each menu on database so item has a menu id to link
    for menu in menus:
        menu.create()  # save menu on database

        # then save its items, because now, Item has a menu id to make the relation
        db.session.bulk_save_objects(menu.items)
        db.session.commit()


def populate_demands():
    demands = get_demands()
    db.session.bulk_save_objects(demands)
    db.session.commit()


def populate_costumer_tables():
    costumer_tables = get_costumer_tables()
    db.session.bulk_save_objects(costumer_tables)
    db.session.commit()


def init_app(app):
    commands = [
        create_db,
        drop_db,
        populate_db,
        populate_menus,
        populate_demands,
        populate_costumer_tables,
    ]

    # add multiple commands in a bulk
    for command in commands:
        app.cli.add_command(app.cli.command()(command))
