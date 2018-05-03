import re
from flask import request
from app.models import (
    User, UserType, Meal, MenuType,
    Menu, MenuItem, Notification, Order
)


class ValidationError(Exception):
    """ Base class is enough """
    errors = []
    def __init__(self, error):
        self.errors.append(error)

    def __str__(self):
        return str(self.errors[0])

class AuthorizationError(ValidationError):
    """ Base class is enough """
    pass

def validate_user(**kwargs):
    fields = request.json
    if not fields.get('username'):
        raise ValidationError('Username is required')

    if not fields.get('email'):
        raise ValidationError('Email is required')

    if not fields.get('password'):
        raise ValidationError('Password is required')

    if not fields.get('confirm_password'):
        raise ValidationError('Password confirmation is required')

    if fields.get('password').strip() !=  \
            fields.get('confirm_password').strip():
        raise ValidationError('Confirmation password does not match')

    if len(fields.get('password').strip()) < 6:
        raise ValidationError(
            'Password must have at least 6 characters. Leading and' + \
            ' trailing spaces and tabs are ignored.'
        )

    if not re.match(r"^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$",
                    fields['email']):
        raise ValidationError('Please provide a valid email')

    user = User.query.filter_by(email=fields['email']).first()
    if user:
        raise ValidationError('Email must be unique')


def validate_meal(**kwargs):
    fields = request.json
    if not fields.get('name'):
        raise ValidationError('Name is required')

    if not fields.get('cost'):
        raise ValidationError('Cost is required')

    try:
        float(fields.get('cost'))
    except ValueError:
        raise ValidationError('Cost must be numeric')

    meal = Meal.query.filter_by(name=fields['name']).first()
    if meal:
        raise ValidationError('Meal name must be unique')


def validate_menu(**kwargs):
    fields = request.json
    if not fields.get('category'):
        raise ValidationError('Category is required')

    if fields.get('category') not in \
            [MenuType.BREAKFAST, MenuType.LUNCH, MenuType.SUPPER]:
        raise ValidationError('Unknown meal type')


def validate_menu_item(**kwargs):
    fields = request.json
    if not fields.get('meal_id'):
        raise ValidationError('Meal id is required')

    if not fields.get('menu_id'):
        raise ValidationError('Menu id is required')

    meal = Meal.query.get(fields['meal_id'])
    if not meal:
        raise ValidationError('No meal found for that meal_id')

    menu = Menu.query.get(fields['menu_id'])
    if not menu:
        raise ValidationError('No menu found for that menu_id')


def validate_order(**kwargs):
    fields = request.json
    print(request.json)
    if not fields.get('menu_item_id'):
        raise ValidationError('Menu item id is required')

    if not fields.get('user_id'):
        raise ValidationError('User id is required')

    menu_item = MenuItem.query.get(fields['menu_item_id'])
    if not menu_item:
        raise ValidationError('No menu item found for that menu_item_id')

    user = User.query.get(fields['user_id'])
    if not user:
        raise ValidationError('No user found for that user_id')


def validate_notification(**kwargs):
    fields = request.json
    if not fields.get('title'):
        raise ValidationError('Title is required')

    if not fields.get('message'):
        raise ValidationError('Message is required')

    if not fields.get('user_id'):
        raise ValidationError('User id is required')

    user = User.query.get(fields['user_id'])
    if not user:
        raise ValidationError('No user found for that user_id')
