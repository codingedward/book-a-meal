import sys
from flask import (
    Flask, Blueprint, jsonify, send_from_directory, abort, make_response
)
from flask_restless import APIManager
from flask_sqlalchemy import SQLAlchemy 
from flask_jwt_extended import JWTManager
from instance.config import app_config


db = SQLAlchemy()


# these imports require the db
from app.validators import Valid, AuthorizationError
from app.error_handlers import errors_handler, blacklist_handler
from app.auth import auth, caterer_auth, default_auth
from app.models import Meal, User, Notification, Menu, Order, MenuItem
from app.customize_routes import (
    single_for_user, many_for_user, todays, post_delete, check_exists
)


def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    db.init_app(app)
    app.register_blueprint(auth)
    errors_handler(app)
    jwt = JWTManager(app)
    blacklist_handler(jwt)

    @app.route('/')
    def docs():
        return send_from_directory('../docs', 'index.html')

    with app.app_context():
        """ we need to have our api routes while the app is running """

        manager = APIManager(app, flask_sqlalchemy_db=db)
        manager.create_api(
            Meal,
            methods=['GET', 'POST', 'DELETE', 'PUT'],
            url_prefix='/api/v1',
            preprocessors={
                'POST': [caterer_auth, Valid.post_meal],
                'GET_MANY': [default_auth],
                'GET_SINGLE': [default_auth, check_exists(Meal)],
                'PUT_SINGLE': [caterer_auth, Valid.put_meal,
                               check_exists(Meal)],
                'DELETE_SINGLE': [caterer_auth],
                'DELETE_MANY': [caterer_auth],
            },
            postprocessors={
                'DELETE_SINGLE': [post_delete],
                'DELETE_MANY': [post_delete],
            }
        )

        manager.create_api(
            Menu,
            methods=['GET', 'POST', 'DELETE', 'PUT'],
            url_prefix='/api/v1',
            collection_name='menu',
            preprocessors={
                'POST': [caterer_auth, Valid.menu],
                'GET_SINGLE': [default_auth, check_exists(Menu)],
                'GET_MANY': [default_auth, todays],
                'PUT_SINGLE': [caterer_auth, Valid.menu,
                               check_exists(Menu)],
                'DELETE_SINGLE': [caterer_auth],
                'DELETE_MANY': [caterer_auth],
            },
            postprocessors={
                'DELETE_SINGLE': [post_delete],
                'DELETE_MANY': [post_delete]
            }
        )

        manager.create_api(
            MenuItem,
            methods=['GET', 'POST', 'DELETE', 'PUT'],
            url_prefix='/api/v1',
            preprocessors={
                'POST': [caterer_auth, Valid.post_menu_item],
                'GET_SINGLE': [default_auth, check_exists(MenuItem)],
                'GET_MANY': [default_auth],
                'PUT_SINGLE': [caterer_auth, Valid.put_menu_item,
                               check_exists(MenuItem)],
                'DELETE_SINGLE': [caterer_auth],
                'DELETE_MANY': [caterer_auth],
            },
            postprocessors={
                'DELETE_SINGLE': [post_delete],
                'DELETE_MANY': [post_delete]
            }
        )

        manager.create_api(
            Order,
            methods=['GET', 'POST', 'DELETE', 'PUT'],
            url_prefix='/api/v1',
            preprocessors={
                'POST': [default_auth, Valid.post_order],
                'GET_SINGLE': [default_auth, check_exists(Order), 
                               single_for_user(Order)],
                'GET_MANY': [default_auth, many_for_user],
                'PUT_SINGLE': [default_auth, Valid.put_order,
                               check_exists(Order)],
                'DELETE_SINGLE': [default_auth],
                'DELETE_MANY': [caterer_auth],
            },
            postprocessors={
                'DELETE_SINGLE': [post_delete],
                'DELETE_MANY': [post_delete]
            }
        )

        manager.create_api(
            Notification,
            methods=['GET', 'POST', 'DELETE', 'PUT'],
            url_prefix='/api/v1',
            preprocessors={
                'POST': [caterer_auth, Valid.notification],
                'GET_SINGLE': [default_auth, check_exists(Notification)],
                'GET_MANY': [default_auth],
                'PUT_SINGLE': [caterer_auth, Valid.notification,
                               check_exists(Notification)],
                'DELETE_SINGLE': [default_auth],
                'DELETE_MANY': [default_auth],
            },
            postprocessors={
                'DELETE_SINGLE': [post_delete],
                'DELETE_MANY': [post_delete]
            }
        )

    return app
