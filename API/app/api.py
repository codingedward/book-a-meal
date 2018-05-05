from flask_restless import APIManager
from app.validators import (
    validate_post_meal, validate_put_meal, validate_menu,
    validate_notification, validate_user, validate_post_menu_item,
    validate_post_order, validate_put_order, validate_put_menu_item
)
from app.models import Meal, User, Notification, Menu, Order, MenuItem
from app.auth import auth, caterer_auth, customer_auth

manager = APIManager()
meal_api = manager.create_api_blueprint(
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
    }
)

menu_api = manager.create_api_blueprint(
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
    }
)

menu_item_api = manager.create_api_blueprint(
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
    }
)

order_api = manager.create_api_blueprint(
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
    }
)

notification_api = manager.create_api_blueprint(
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
    }
)

