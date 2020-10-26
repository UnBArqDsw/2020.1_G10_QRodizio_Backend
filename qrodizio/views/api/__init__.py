from .home import home_bp
from .employees import employees_bp
from .auth import auth_bp
from .menus import menus_bp
from .qrcode import qrcode_bp
from .demands import demands_bp
from .customer_tables import tables_bp
from .tables_sessions import sessions_bp


def init_app(app):
    app.register_blueprint(home_bp)
    app.register_blueprint(employees_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(menus_bp)
    app.register_blueprint(qrcode_bp)
    app.register_blueprint(demands_bp)
    app.register_blueprint(tables_bp)
    app.register_blueprint(sessions_bp)
