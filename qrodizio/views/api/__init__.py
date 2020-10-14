from .home import home_bp
from .employees import employees_bp
from .auth import auth_bp
from .menus import menus_bp
from .qrcode import qrcode_bp


def init_app(app):
    app.register_blueprint(home_bp)
    app.register_blueprint(employees_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(menus_bp)
    app.register_blueprint(qrcode_bp)
