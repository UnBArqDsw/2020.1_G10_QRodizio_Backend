from qrodizio.ext.database import db
from qrodizio.populate_data import get_employees


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


def init_app(app):
    # add multiple commands in a bulk
    for command in [create_db, drop_db, populate_db]:
        app.cli.add_command(app.cli.command()(command))
