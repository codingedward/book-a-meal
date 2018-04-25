import sys
from flask import Flask
from flask_restless import APIManager
from flask_sqlalchemy import SQLAlchemy 
from instance.config import app_config


db = SQLAlchemy()

def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    db.init_app(app)

    with app.app_context():
        from app.models import Meal
        manager = APIManager(app, flask_sqlalchemy_db=db)
        manager.create_api(
            Meal,
            methods=['GET', 'POST', 'DELETE', 'PUT'],
            url_prefix='/api/v1'
        )

    return app
