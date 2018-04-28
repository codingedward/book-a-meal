import os
import re
from passlib.hash import bcrypt


class MealType:
    LUNCH = 1
    SUPPER = 2
    BREAKFAST = 3


class UserType:
    CATERER = 1
    CUSTOMER = 2


class BAM:
    def __init__(self):
        self.clear()

    @property
    def users(self):
        return self._users

    def post_user(self, user):
        self._users_index += 1
        user['id'] = self._users_index
        user['password'] = user['password']
        self._users_internal[self._users_index] = {
            'id': self._users_index,
            'email': user['email'],
            'password': user['password']
        }
        del user['password']
        self._users[self._users_index] = user

        return user

    def put_user(self, user, id):
        self._users[id] = user

    def get_user(self, id):
        return self._users.get(id)

    def get_internal_user_by_email(self, email):
        """
        The internal user has a password field
        """
        for u in self._users_internal.values():
            if u['email'] == email:
                return u

    def get_user_by_email(self, email):
        for u in self._users.values():
            if u['email'] == email:
                return u

    def get_users(self):
        return self._users

    def delete_user(self, id):
        del self._users[id]

    def validate_user_fails(self, fields):
        if not fields.get('username'):
            return True, ['Username is required']

        if not fields.get('email'):
            return True, ['Email is required']

        if not fields.get('password'):
            return True, ['Password is required']

        if len(fields.get('password')) < 6:
            return True, ['Password must be at least 6 characters']

        if not re.match(r"^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$",
                        fields['email']):
            return True, ['Please provide a valid email']

        for u in self._users.values():
            if u['email'] == fields['email']:
                return True, ['Email must be unique']

        return False, []

    @property
    def meals(self):
        return self._meals

    def post_meal(self, meal):
        self._meals_index += 1
        meal['id'] = self._meals_index
        self._meals[self._meals_index] = meal
        return meal

    def put_meal(self, meal, id):
        self._meals[id] = meal

    def get_meal(self, id):
        return self._meals.get(id)

    def get_meals(self):
        return self._meals

    def delete_meal(self, id):
        del self._meals[id]

    def validate_meal_fails(self, fields):
        if not fields.get('name'):
            return True, ['Name is required']

        if not fields.get('cost'):
            return True, ['Cost is required']
        try:
            float(fields.get('cost'))
        except ValueError:
            return True, ['Cost must be numeric']

        for m in self._meals.values():
            if m['name'] == fields['name']:
                return True, ['Meal name must be unique']

        return False, []

    @property
    def menus(self):
        return self._menus

    def post_menu(self, menu):
        self._menus_index += 1
        menu['id'] = self._menus_index
        self._menus[self._menus_index] = menu
        return menu

    def put_menu(self, menu, id):
        self._menus[id] = menu

    def get_menu(self, id):
        return self._menus.get(id)

    def get_menus(self):
        return self._menus

    def delete_menu(self, id):
        del self._menus[id]

    def validate_menu_fails(self, fields):
        if not fields.get('meal_id'):
            return True, ['Meal id is required']

        if not fields.get('category'):
            return True, ['Category is required']

        if fields.get('meal_id') not in self._meals.keys():
            return True, ['No meal found for that meal_id']

        if fields.get('category') not in [1, 2, 3]:
            return True, ['Unknown meal type']

        return False, []

    @property
    def orders(self):
        return self._orders

    def post_order(self, order):
        self._orders_index += 1
        order['id'] = self._orders_index
        self._orders[self._orders_index] = order
        return order

    def put_order(self, order, id):
        self._orders[id] = order

    def get_order(self, id):
        return self._orders.get(id)

    def get_orders(self):
        return self._orders

    def delete_order(self, id):
        del self._orders[id]

    def validate_order_fails(self, fields):
        if not fields.get('menu_id'):
            return True, ['Menu id is required']

        if not fields.get('user_id'):
            return True, ['User id is required']

        if fields.get('user_id') not in self._users.keys():
            return True, ['No user found for that user_id']

        if fields.get('menu_id') not in self._menus.keys():
            return True, ['No menu found for that menu_id']

        return False, []

    @property
    def notifications(self):
        return self._notifications

    def post_notification(self, notification):
        self._notifications_index += 1
        notification['id'] = self._notifications_index
        self._notifications[self._notifications_index] = notification
        return notification

    def put_notification(self, notification, id):
        self._notifications[id] = notification

    def get_notification(self, id):
        return self._notifications.get(id)

    def get_notifications(self):
        return self._notifications

    def delete_notification(self, id):
        del self._notifications[id]

    def validate_notification_fails(self, fields):
        if not fields.get('title'):
            return True, ['Title is required']

        if not fields.get('message'):
            return True, ['Message is required']

        if not fields.get('user_id'):
            return True, ['User id is required']

        if fields.get('user_id') not in self._users.keys():
            return True, ['No user found for that user_id']

        return False, []

    def clear(self):
        self._users = {}
        self._users_internal = {}
        self._users_index = 0
        self._meals = {}
        self._meals_index = 0
        self._menus = {}
        self._menus_index = 0
        self._orders = {}
        self._orders_index = 0
        self._notifications = {}
        self._notifications_index = 0
        # create default caterer
        self.post_user({
            'username': os.getenv('DEFAULT_ADMIN_USERNAME'),
            'email': os.getenv('DEFAULT_ADMIN_EMAIL'),
            'password': os.getenv('DEFAULT_ADMIN_PASSWORD'),
            'role': UserType.CATERER
        })
