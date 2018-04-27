import json
from flask import Flask
from app.api import api, bam
from flask_jwt import JWT
from passlib.hash import bcrypt
from collections import namedtuple
from instance.config import app_config

def authenticate(email, password):
    user = bam.get_internal_user_by_email(email)
    if user and bcrypt.verify(password, user['password']):
        return namedtuple('User', user.keys())(*user.values())

def identity(payload):
    user_id = payload['identity']
    return bam.get_user(user_id)



def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    jwt = JWT(app, authenticate, identity)
    app.register_blueprint(api)

    return app


