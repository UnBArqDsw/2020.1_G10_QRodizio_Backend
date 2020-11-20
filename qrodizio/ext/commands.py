from qrodizio.ext.database import db
from qrodizio.populate_data import (
    get_employees,
    get_menus,
    get_demands,
    get_customer_tables,
    get_payments_demand,
)


def drop_and_populate():
    """Creates database"""
    db.drop_all()
    db.create_all()
    populate_all


def create_db():
    """Creates database"""
    db.create_all()


def drop_db():
    """Cleans database"""
    db.drop_all()


def populate_employees():
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


def populate_customer_tables():
    customer_tables = get_customer_tables()

    for table in customer_tables:
        table.create()  # session needs table.id

        db.session.bulk_save_objects(table.sessions)
        db.session.commit()

    db.session.bulk_save_objects(customer_tables)
    db.session.commit()

def populate_payments():
    payments = get_payments_demand()
    db.session.bulk_save_objects(payments)
    db.session.commit()


def populate_all():
    populate_employees()
    populate_customer_tables()
    populate_menus()
    populate_demands()
    populate_payments()


def dev_populate():
    drop_db()
    create_db()
    populate_all()


def init_app(app):
    commands = [
        create_db,
        drop_and_populate,
        drop_db,
        populate_employees,
        populate_menus,
        populate_demands,
        populate_customer_tables,
        populate_payments,
        populate_all,
        dev_populate,
    ]

    # add multiple commands in a bulk
    for command in commands:
        app.cli.add_command(app.cli.command()(command))
