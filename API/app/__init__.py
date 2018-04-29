import json
from flask import Flask
from flask_jwt_extended import JWTManager
from app.api import api, bam, blacklist
from instance.config import app_config


def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    app.register_blueprint(api)

    jwt = JWTManager(app)

    @jwt.token_in_blacklist_loader
    def check_token_in_blacklist(decrypted_token):
        """ Check if token is in blacklist """
        return decrypted_token['jti'] in blacklist

    return app
