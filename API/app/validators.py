import re
from datetime import datetime, date
from flask import request
from flask_restless import ProcessingException
from app.models import (
    User, UserType, Meal, MenuType,
    Menu, MenuItem, Notification, Order
)
from flask_jwt_extended import get_jwt_identity


def clean_unexpected(request, expected):
    remove = [key for key in request.json if key not in expected]
    for key in remove:
        del request.json[key]


class Valid:
    @staticmethod
    def user(**kwargs):
        fields = request.json
        if not fields.get('username'):
            raise ProcessingException(
                description='Username is required', 
                code=400
            )

        if len(fields.get('username').strip()) < 3:
            raise ProcessingException(
                description=
                'Username must have at least 3 characters. Leading and' + \
                ' trailing spaces and tabs are ignored.',
                code=400
            )

        if fields.get('email') is None:
            raise ProcessingException(
                description='Email is required', 
                code=400
            )

        if fields.get('password') is None:
            raise ProcessingException(
                description='Password is required', 
                code=400
            )

        if fields.get('confirm_password') is None:
            raise ProcessingException(
                description='Password confirmation is required', 
                code=400
            )

        if fields.get('password').strip() !=  \
                fields.get('confirm_password').strip():
            raise ProcessingException(
                description='Confirmation password does not match', 
                code=400
            )

        if len(fields.get('password').strip()) < 6:
            raise ProcessingException(
                description=
                'Password must have at least 6 characters. Leading and' + \
                ' trailing spaces and tabs are ignored.',
                code=400
            )

        if not re.match(r"^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$",
                        fields['email']):
            raise ProcessingException(
                description='Please provide a valid email', 
                code=400
            )

        user = User.query.filter_by(email=fields['email']).first()
        if user:
            raise ProcessingException(
                description='This email has already been used', 
                code=400
            )

    @staticmethod
    def post_meal(**kwargs):
        clean_unexpected(request, ['name', 'cost', 'quantity', 'img_path'])

        fields = request.json
        if fields.get('name') is None:
            raise ProcessingException(
                description='Name is required', 
                code=400
            )

        if len(fields.get('name').strip()) == 0:
            raise ProcessingException(
                description='Invalid meal name', 
                code=400
            )

        if fields.get('cost') is None:
            raise ProcessingException(
                description='Cost is required', 
                code=400
            )

        if fields.get('img_path') is None:
            request.json['img_path'] = None

        try:
            float(fields.get('cost'))
        except:
            raise ProcessingException(
                description='Cost must be numeric', 
                code=400
            )

        meal = Meal.query.filter_by(name=fields['name']).first()
        if meal:
            raise ProcessingException(
                description='Meal name must be unique', 
                code=400
            )

    @staticmethod
    def put_meal(instance_id=None, **kwargs):
        clean_unexpected(request, ['name', 'cost', 'quantity', 'img_path'])

        fields = request.json
        if len(fields) == 0:
            raise ProcessingException(
                description="Nothing to update",
                code=400
            )

        if 'name' in fields:
            if len(fields.get('name').strip()) == 0:
                raise ProcessingException(
                    description='Invalid meal name', 
                    code=400
                )

            # check if another meal has the new name...
            meal = Meal.query.filter_by(name=fields['name']).first()
            if meal and  meal.id != instance_id:
                raise ProcessingException(
                    description='Meal name must be unique', 
                    code=400
                )

        if 'cost' in fields:
            try:
                float(fields.get('cost'))
            except:
                raise ProcessingException(
                    description='Cost must be numeric', 
                    code=400
                )

    @staticmethod
    def post_menu(**kwargs):
        clean_unexpected(request, ['category'])
        fields = request.json

        if fields.get('category') is None:
            raise ProcessingException(
                description='Category is required', 
                code=400
            )

        if fields.get('category') not in \
                [MenuType.BREAKFAST, MenuType.LUNCH, MenuType.SUPPER]:
            raise ProcessingException(
                description='Unknown meal type', 
                code=400
            )


    @staticmethod
    def put_menu(instance_id=None, **kwargs):
        clean_unexpected(request, ['category'])
        fields = request.json

        if fields.get('category') is None:
            raise ProcessingException(
                description='Nothing to update', 
                code=400
            )

        if fields.get('category') not in \
                [MenuType.BREAKFAST, MenuType.LUNCH, MenuType.SUPPER]:
            raise ProcessingException(
                description='Unknown meal type', 
                code=400
            )


    @staticmethod
    def post_menu_item(**kwargs):
        clean_unexpected(request, ['meal_id', 'menu_id'])
        fields = request.json

        if fields.get('meal_id') is None:
            raise ProcessingException(
                description='Meal id is required', 
                code=400
            )

        if fields.get('menu_id') is None:
            raise ProcessingException(
                description='Menu id is required', 
                code=400
            )

        meal = Meal.query.get(fields['meal_id'])
        if not meal:
            raise ProcessingException(
                description='No meal found for that meal_id', 
                code=400
            )

        menu = Menu.query.get(fields['menu_id'])
        if not menu:
            raise ProcessingException(
                description='No menu found for that menu_id', 
                code=400
            )

        menu_item = MenuItem.query.filter_by(menu_id=menu.id, 
                                             meal_id=meal.id).first()
        if menu_item:
            raise ProcessingException(
                description='This menu item already exists', 
                code=400
            )

    @staticmethod
    def put_menu_item(instance_id=None, **kwargs):
        clean_unexpected(request, ['meal_id', 'menu_id'])
        fields = request.json

        if len(fields) == 0:
            raise ProcessingException(
                description='Nothing to update', 
                code=400
            )

        if 'meal_id' in fields:
            meal = Meal.query.get(fields['meal_id'])
            if not meal:
                raise ProcessingException(
                    description='No meal found for that meal_id', 
                    code=400
                )

        if 'menu_id' in fields:
            menu = Menu.query.get(fields['menu_id'])
            if not menu:
                raise ProcessingException(
                    description='No menu found for that menu_id', 
                    code=400
                )

        # ensure the same menu item is not added twice...
        menu_item = MenuItem.query.filter_by(menu_id=menu.id, 
                                             meal_id=meal.id).first()
        if menu_item and instance_id != menu_item.id:
            raise ProcessingException(
                description='This menu item already exists', 
                code=400
            )

    @staticmethod
    def post_order(**kwargs):
        current_user = User.query.filter_by(email=get_jwt_identity()).first()
        request.json['user_id'] = current_user.id

        clean_unexpected(request, ['menu_item_id', 'user_id', 'quantity'])
        fields = request.json

        if fields.get('menu_item_id') is None:
            raise ProcessingException(
                description='Menu item id is required', 
                code=400
            )

        # set a default quantity
        if fields.get('quantity') is None:
            request.json['quantity'] = 1

        menu_item = MenuItem.query.get(fields['menu_item_id'])
        if menu_item is None:
            raise ProcessingException(
                description='No menu item found for that menu_item_id', 
                code=400
            )

        menu = Menu.query.get(menu_item.menu_id)
        if menu.day != datetime.utcnow().date():
            raise ProcessingException(
                description='This menu is expired', 
                code=400
            )


    @staticmethod
    def put_order(instance_id=None, **kwargs):
        current_user = User.query.filter_by(email=get_jwt_identity()).first()
        order = Order.query.get(instance_id)
        if order.user_id != current_user.id:
            raise ProcessingException(
                description='This user cannot edit this order', 
                code=401
            )

        clean_unexpected(request, ['menu_item_id', 'quantity'])
        fields = request.json

        if 'menu_item_id' in fields:
            menu_item = MenuItem.query.get(fields['menu_item_id'])
            if menu_item is None:
                raise ProcessingException(
                    description='No menu item found for that menu_item_id', 
                    code=400
                )

            menu = Menu.query.get(menu_item.menu_id)
            if menu.day != datetime.utcnow().date():
                raise ProcessingException(
                    description='This menu is expired', 
                    code=400
                )


    @staticmethod
    def post_notification(**kwargs):
        clean_unexpected(request, ['title', 'message', 'user_id'])
        fields = request.json

        if fields.get('title') is None or \
                len(fields.get('title').strip()) == 0:
            raise ProcessingException(
                description='Title is required', 
                code=400
            )

        if fields.get('message') is None or \
                len(fields.get('message').strip()) == 0:
            raise ProcessingException(
                description='Message is required', 
                code=400
            )

        if fields.get('user_id') is None:
            raise ProcessingException(
                description='User id is required', 
                code=400
            )

        user = User.query.get(fields['user_id'])
        if not user:
            raise ProcessingException(
                description='No user found for that user_id', 
                code=400
            )

    @staticmethod
    def put_notification(instance_id=None, **kwargs):
        clean_unexpected(request, ['title', 'message', 'user_id'])
        fields = request.json

        if 'user_id' in fields:
            user = User.query.get(fields['user_id'])
            if not user:
                raise ProcessingException(
                    description='No user found for that user_id', 
                    code=400
                )

        if 'title' in fields:
            if len(fields.get('title').strip()) == 0:
                raise ProcessingException(
                    description='Title is required', 
                    code=400
                )

        if 'message' in fields:
            if len(fields.get('message').strip()) == 0:
                raise ProcessingException(
                    description='Message is required', 
                    code=400
                )
