from .home import home_bp
from .employees import employees_bp


def init_app(app):
    app.register_blueprint(home_bp)
    app.register_blueprint(employees_bp)
