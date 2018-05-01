import sys
from flask import Flask, Blueprint
from flask_restless import APIManager
from flask_sqlalchemy import SQLAlchemy 
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity, get_raw_jwt
)
from instance.config import app_config

db = SQLAlchemy()

from app.auth import auth, caterer_auth, customer_auth
from app.models import Meal, User, Notification, Menu, Order


def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    db.init_app(app)
    app.register_blueprint(auth)

    jwt = JWTManager(app)

    @jwt.token_in_blacklist_loader
    def check_token_in_blacklist(decrypted_token):
        return False

    with app.app_context():
        """ we need to have our api routes while the app is running """

        manager = APIManager(app, flask_sqlalchemy_db=db)

        manager.create_api(
            Meal,
            methods=['GET', 'POST', 'DELETE', 'PATCH'],
            url_prefix='/api/v1',
            preprocessors={
                'POST': [caterer_auth],
                'PATCH_SINGLE': [caterer_auth],
                'DELETE_SINGLE': [caterer_auth],
                'DELETE_MANY': [caterer_auth],
            }
        )

        manager.create_api(
            Notification,
            methods=['GET', 'POST', 'DELETE', 'PATCH'],
            url_prefix='/api/v1',
            preprocessors={
                'POST': [caterer_auth],
                'GET_ONE': [customer_auth],
                'GET_MANY': [customer_auth],
                'PATCH_SINGLE': [caterer_auth],
                'DELETE_SINGLE': [customer_auth],
                'DELETE_MANY': [customer_auth],
            }
        )

        manager.create_api(
            Menu,
            methods=['GET', 'POST', 'DELETE', 'PATCH'],
            url_prefix='/api/v1',
            preprocessors={
                'POST': [caterer_auth],
                'GET_ONE': [customer_auth],
                'GET_MANY': [customer_auth],
                'PATCH_SINGLE': [caterer_auth],
                'DELETE_SINGLE': [caterer_auth],
                'DELETE_MANY': [caterer_auth],
            }
        )

        manager.create_api(
            Order,
            methods=['GET', 'POST', 'DELETE', 'PATCH'],
            url_prefix='/api/v1',
            preprocessors={
                'POST': [caterer_auth],
                'GET_ONE': [caterer_auth],
                'GET_MANY': [caterer_auth],
                'PATCH_SINGLE': [caterer_auth],
                'DELETE_SINGLE': [caterer_auth],
                'DELETE_MANY': [caterer_auth],
            }
        )

    return app
