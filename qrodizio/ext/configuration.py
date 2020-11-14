from importlib import import_module

from dynaconf import FlaskDynaconf

_config = {}

def load_extensions(app, **config):
    for extension in app.config.EXTENSIONS:
        # Split data in form `extension.path:factory_function`
        module_name, factory = extension.split(":")
        # Dynamically import extension module.
        ext = import_module(module_name)
        # Invoke factory passing app.
        getattr(ext, factory)(app)


def init_app(app, **config):
    FlaskDynaconf(app, **config)
    global _config
    _config = app.config


def get_config(key):
    global _config
    return _config[key]

