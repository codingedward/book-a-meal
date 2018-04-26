import sys
from flask_restless import APIManager
from flask_sqlalchemy import SQLAlchemy 
from flask import Flask, jsonify, request
from flask_jwt import JWT, jwt_required, current_identity

from instance.config import app_config


db = SQLAlchemy()

@jwt_required()
def customer_auth(**kwargs):
    """ 
    We use this empty function to as a preprocessor in JWT restless
    in order to include the @jwt_required decorator. That way, we
    can gaurd our API endpoints.
    """
    pass

@jwt_required()
def caterer_auth(**kwargs):
    """ 
    This is similar to auth_func with the extra requirement of a user 
    being a caterer
    """
    if not current_identity.is_caterer():
        raise ProcessingException(detail='This user is not a caterer', 
                                  status=400)


def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    db.init_app(app)

    from app.models import Meal, User, Notification, Menu, Order
    """
    requires to be imported under create_app to avoid circular imports
    """

    def authenticate(email, password):
        """ this gets called by the JWT scheme to authenticate user """
        user = User.query.filter_by(email=email).first()
        if user and user.validate_password(password):
            return user

    def identity(payload):
        """ given a payload return user """
        return User.query.get(payload['identity'])

    with app.app_context():
        """ we need to have our api routes while the app is running """

        @app.route('/api/v1/auth/register', methods=['POST'])
        def register():
            """ 
            This is the only endpoint we need to create ourselves as all the others
            are provided by flask-restless

            Authentication is handled by flask-jwt
            """
            if not request.is_json: 
                return jsonify({'message': 'Request should be JSON'}), 400
            username = request.json.get('username')
            if not username:
                return jsonify({'message': 'Name is required'}), 400
            email = request.json.get('email')
            if not email:
                return jsonify({'message': 'Email is required'}), 400
            password = request.json.get('password')
            if not password:
                return jsonify({'message': 'Password is required'}), 400

            user = User(username=username, email=email, password=password)
            user.save()
            return jsonify({'message': 'User successfully registered'}), 201
            

        jwt = JWT(app, authenticate, identity)
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
