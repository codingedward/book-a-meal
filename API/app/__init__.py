import sys
from flask import (
    Flask, Blueprint, jsonify, send_from_directory, abort, make_response
)
from flask_restless import APIManager, ProcessingException
from flask_sqlalchemy import SQLAlchemy 
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity, get_raw_jwt
)
from instance.config import app_config
from werkzeug.exceptions import HTTPException, default_exceptions


db = SQLAlchemy()


# these imports require the db
from app.validators import (
    validate_post_meal, validate_put_meal, validate_menu,
    validate_notification, validate_user, 
    validate_post_menu_item,  validate_post_order, validate_put_order,
    validate_put_menu_item, AuthorizationError
)
from app.error_handlers import post_get, post_delete
from app.auth import auth, caterer_auth, customer_auth
from app.models import Meal, User, Notification, Menu, Order, MenuItem


def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    db.init_app(app)
    app.register_blueprint(auth)
    jwt = JWTManager(app)

    @jwt.token_in_blacklist_loader
    def check_token_in_blacklist(decrypted_token):
        return Blacklist.query.filter_by(
                    token=get_raw_jwt()['jti']).first() is not None

    # jsonify http errors
    for code in default_exceptions.keys():
        @app.errorhandler(code)
        def handle_error(ex):
            return jsonify({'message': str(ex)}), code

    @app.errorhandler(AuthorizationError)
    def handle_authorization_error(err):
        return jsonify({'message': str(err)}), 401

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
                'POST': [caterer_auth, validate_post_meal],
                'GET_MANY': [caterer_auth],
                'GET_SINGLE': [caterer_auth],
                'PUT_SINGLE': [caterer_auth, validate_put_meal],
                'DELETE_SINGLE': [caterer_auth],
                'DELETE_MANY': [caterer_auth],
            },
            postprocessors={
                'DELETE_SINGLE': [post_delete],
                'DELETE_MANY': [post_delete],
                'GET_SINGLE': [post_get]
            }
        )

        manager.create_api(
            Menu,
            methods=['GET', 'POST', 'DELETE', 'PUT'],
            url_prefix='/api/v1',
            collection_name='menu',
            preprocessors={
                'POST': [caterer_auth, validate_menu],
                'GET_SINGLE': [customer_auth],
                'GET_MANY': [customer_auth],
                'PUT_SINGLE': [caterer_auth, validate_menu],
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
                'POST': [caterer_auth, validate_post_menu_item],
                'GET_SINGLE': [customer_auth],
                'GET_MANY': [customer_auth],
                'PUT_SINGLE': [caterer_auth, validate_put_menu_item],
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
                'POST': [customer_auth, validate_post_order],
                'GET_SINGLE': [customer_auth],
                'GET_MANY': [caterer_auth],
                'PUT_SINGLE': [customer_auth, validate_put_order],
                'DELETE_SINGLE': [customer_auth],
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
                'POST': [caterer_auth, validate_notification],
                'GET_SINGLE': [customer_auth],
                'GET_MANY': [customer_auth],
                'PUT_SINGLE': [caterer_auth, validate_notification],
                'DELETE_SINGLE': [customer_auth],
                'DELETE_MANY': [customer_auth],
            },
            postprocessors={
                'DELETE_SINGLE': [post_delete],
                'DELETE_MANY': [post_delete]
            }
        )

    return app
