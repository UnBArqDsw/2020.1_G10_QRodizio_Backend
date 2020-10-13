import pytest

from qrodizio.app import create_app, minimal_app
from qrodizio.ext.commands import populate_db, populate_menus
from qrodizio.ext.database import db


@pytest.fixture(scope="session")
def min_app():
    app = minimal_app(FORCE_ENV_FOR_DYNACONF="testing")
    return app


@pytest.fixture(scope="session")
def app():
    app = create_app(FORCE_ENV_FOR_DYNACONF="testing")

    with app.app_context():
        db.create_all(app=app)
        populate_db()
        populate_menus()
        yield app
        db.drop_all(app=app)


# @pytest.fixture(scope="session")
# def populate_test(app):
#    with app.app_context():
#        return populate_db()
