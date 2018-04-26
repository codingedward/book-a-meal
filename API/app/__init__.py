import sys
from flask_jwt import JWT
from flask_restless import APIManager
from flask_sqlalchemy import SQLAlchemy 
from flask import Flask, jsonify, request

from instance.config import app_config


db = SQLAlchemy()


def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    db.init_app(app)

    from app.models import Meal, User

    def authenticate(email, password):
        user = User.query.filter_by(email=email).first()
        if user and user.validate_password(password):
            return user

    def identity(payload):
        return User.query.get(payload['id'], None)

    with app.app_context():

        @app.route('/api/v1/auth/register', methods=['POST'])
        def register():
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
            methods=['GET', 'POST', 'DELETE', 'PUT'],
            url_prefix='/api/v1'
        )

    return app
