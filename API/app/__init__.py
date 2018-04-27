import json
from app.api import api
from instance.config import app_config
from flask import Flask




def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    app.register_blueprint(api)

    return app


