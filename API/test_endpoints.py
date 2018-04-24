import os
import json
import unittest
from app import create_app, db


class AuthenticationTestCase(unittest.TestCase):
    """ Will test authentication """
    def setUp(self):
        self.app = create_app(config_name='testing')
        self.client = self.app.test_client
        self.user = {'name': 'John', 'email': 'john@doe.com', 
                     'password': 'secret'}

        with self.app.app_context():
            db.create_all()

    def test_user_can_signup(self):
        res = self.client().post('/users/auth/signup', data=self.user)
        self.assertEqual(res.status_code, 201)

    def test_user_can_login(self):
        res = self.client().post('/users/auth/login', data=self.user)
        self.assertEqual(res.status_code, 201)
        self.assertIn('token', res.data)

    def test_user_can_logout(self):
        res = self.client().post('/user/autho/logout')
        self.assertEqual(res.status_code, 201)

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()


class MealTestCase(unittest.TestCase):
    """ Will test meal model"""
    def setUp(self):
        self.app = create_app(config_name='testing')
        self.client = self.app.test_client
        self.meal = {'name': 'Ugali', 'img_path': '#', 'cost': 200.0}

        with self.app.app_context():
            db.create_all()

    def test_meal_creation(self):
        res = self.client().post('/meals', data=self.meal)
        self.assertEqual(res.status_code, 201)
        self.assertIn('id', res.data.keys())

    def test_can_get_all_meals(self):
        res = self.client().post('/meals', data=self.meal)
        self.assertEqual(res.status_code, 201)
        res = self.client().get('/meals')
        self.assertEqual(res.status_code, 200)

    def test_can_get_meal_by_id(self):
        res = self.client().post('/meals', data=self.meal)
        self.assertEqual(res.status_code, 201)
        json_result = json.loads(res.data.decode('utf-8').replace("'", "\""))
        res = self.client().get(
            '/meals/{}'.format(json_result['id'])
        )
        self.assertEqual(res.status_code, 200)
        self.assertIn('id', res.data)

    def test_meal_can_be_updated(self):
        res = self.client().post('/meals', data=self.meal)
        self.assertEqual(res.status_code, 201)
        res = self.client().put(
            '/meals/1',
            data={
                'name': 'Sembe',
                'img_path': '#',
                'cost': 200.0
            }
        )
        self.assertEqual(res.status_code, 200)
        res = self.client().get('/meals/1')
        self.assertEqual('Sembe', res.data)

    def test_meal_deletion(self):
        res = self.client().post('/meals', data=self.meal)
        self.assertEqual(res.status_code, 201)
        res = self.client().delete('/meals/1')
        self.assertEqual(res.status_code, 200)

        res = self.client().get('/meals/1')
        self.assertEqual(res.status_code, 404)

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()


class MenuTestCase(unittest.TestCase):
    """ Will test menu model"""
    def setUp(self):
        self.app = create_app(config_name='testing')
        self.client = self.app.test_client

        # create a temporary meal
        res = self.client().post(
            '/meals', 
            data={ 
                'name': 'Ugali', 
                'img_path': '#', 
                'cost': 200.0
            }
        )

        json_result = json.loads(res.data.decode('utf-8').replace("'", "\""))
        self.meal_id = json_result['id']

        with self.app.app_context():
            db.create_all()

    def test_menu_creation(self):
        res = self.client().post(
            '/menus',
            data={
                'meal_id': self.meal_id,
                'category': MealType.BREAKFAST,
            }
        )
        res.assertEqual(res.status_code, 201)
        res.assertIn('id', res.data)


    def test_can_get_all_menus(self):
        res = self.client().post(
            '/menus',
            data={
                'meal_id': self.meal_id,
                'category': MealType.BREAKFAST,
            }
        )
        res.assertEqual(res.status_code, 201)

        res = self.client().get('/menus')
        self.assertEqual(res.status_code, 200)

    def test_can_get_menu_by_id(self):
        res = self.client().post(
            '/menus',
            data={
                'meal_id': self.meal_id,
                'category': MealType.BREAKFAST,
            }
        )
        res.assertEqual(res.status_code, 201)

        json_result = json.loads(res.data.decode('utf-8').replace("'", "\""))
        res = self.client().get(
            '/menus/{}'.format(json_result['id'])
        )
        self.assertEqual(res.status_code, 200)
        self.assertIn('id', res.data)

    def test_menu_can_be_updated(self):
        res = self.client().post(
            '/menus',
            data={
                'meal_id': self.meal_id,
                'category': MealType.BREAKFAST,
            }
        )
        res.assertEqual(res.status_code, 201)

        json_result = json.loads(res.data.decode('utf-8').replace("'", "\""))
        res = self.client().put(
            '/menus/1',
            data={
                'meal_id': json_result['id'],
                'category': MealType.LUNCH,
            }
        )
        self.assertEqual(res.status_code, 200)

    def test_menu_deletion(self):
        res = self.client().post(
            '/menus',
            data={
                'meal_id': self.meal_id,
                'category': MealType.BREAKFAST,
            }
        )
        res.assertEqual(res.status_code, 201)

        res = self.client().delete('/menus/1')
        self.assertEqual(res.status_code, 200)

        res = self.client().get('/menus/1')
        self.assertEqual(res.status_code, 404)

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()


class NotificationTestCase(unittest.TestCase):
    """ Will test notification model"""
    def setUp(self):
        self.app = create_app(config_name='testing')
        self.client = self.app.test_client

        # create a temporary user
        res = self.client().post(
            '/users', 
            data={ 
                'username': 'John',
                'email': 'john@doe.com',
                'password': 'secret'
            }
        )

        json_result = json.loads(res.data.decode('utf-8').replace("'", "\""))
        self.user_id = json_result['id']
        self.notification = {
            'user_id':  self.user_id,
            'title': 'Hello there',
            'message': 'I have a message for you',
        }

        with self.app.app_context():
            db.create_all()

    def test_notification_creation(self):
        res = self.client().post( '/notifications', data=self.notification)
        res.assertEqual(res.status_code, 201)
        res.assertIn('id', res.data)


    def test_can_get_all_notifications(self):
        res = self.client().post( '/notifications', data=self.notification)
        res.assertEqual(res.status_code, 201)

        res = self.client().get('/notifications')
        self.assertEqual(res.status_code, 200)

    def test_can_get_notification_by_id(self):
        res = self.client().post( '/notifications', data=self.notification)
        res.assertEqual(res.status_code, 201)

        json_result = json.loads(res.data.decode('utf-8').replace("'", "\""))
        res = self.client().get(
            '/notifications/{}'.format(json_result['id'])
        )
        self.assertEqual(res.status_code, 200)
        self.assertIn('id', res.data)

    def test_notification_can_be_updated(self):
        res = self.client().post( '/notifications', data=self.notification)
        res.assertEqual(res.status_code, 201)

        res = self.client().put(
            '/notifications/1',
            data={
                'user_id': self.user_id,
                'title': 'Hello again',
                'message': 'I have a message for you',
            }
        )
        self.assertEqual(res.status_code, 200)
        self.assertIn('Hello again', res)

    def test_notification_deletion(self):
        res = self.client().post( '/notifications', data=self.notification)
        res.assertEqual(res.status_code, 201)

        res = self.client().delete('/notifications/1')
        self.assertEqual(res.status_code, 200)

        res = self.client().get('/notifications/1')
        self.assertEqual(res.status_code, 404)

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()


class OrderTestCase(unittest.TestCase):
    """ Will test order model"""
    def setUp(self):
        self.app = create_app(config_name='testing')
        self.client = self.app.test_client

        res = self.client().post(
            '/meals', 
            data={ 
                'name': 'Ugali', 
                'img_path': '#', 
                'cost': 200.0
            }
        )

        json_result = json.loads(res.data.decode('utf-8').replace("'", "\""))
        self.meal_id = json_result['id']

        res = self.client().post(
            '/users', 
            data={ 
                'username': 'John',
                'email': 'john@doe.com',
                'password': 'secret'
            }
        )

        json_result = json.loads(res.data.decode('utf-8').replace("'", "\""))
        self.user_id = json_result['id']
        self.order = {
            'meal_id': self.meal_id,
            'user_id': self.user_id,
        }

        with self.app.app_context():
            db.create_all()

    def test_order_creation(self):
        res = self.client().post( '/orders', data=self.order)
        res.assertEqual(res.status_code, 201)
        res.assertIn('id', res.data)


    def test_can_get_all_orders(self):
        res = self.client().post( '/orders', data=self.order)
        res.assertEqual(res.status_code, 201)

        res = self.client().get('/orders')
        self.assertEqual(res.status_code, 200)

    def test_can_get_order_by_id(self):
        res = self.client().post( '/orders', data=self.order)
        res.assertEqual(res.status_code, 201)

        json_result = json.loads(res.data.decode('utf-8').replace("'", "\""))
        res = self.client().get(
            '/orders/{}'.format(json_result['id'])
        )
        self.assertEqual(res.status_code, 200)
        self.assertIn('id', res.data)

    def test_order_can_be_updated(self):
        res = self.client().post( '/orders', data=self.order)
        res.assertEqual(res.status_code, 201)

        json_result = json.loads(res.data.decode('utf-8').replace("'", "\""))
        res = self.client().post(
            '/meals', 
            data={ 
                'name': 'Ugali Skuma', 
                'img_path': '#', 
                'cost': 200.0
            }
        )
        json_result = json.loads(res.data.decode('utf-8').replace("'", "\""))

        res = self.client().put(
            '/orders/1',
            data={
                'meal_id': json_result['id'],
                'user_id': self.user_id
            }
        )
        self.assertEqual(res.status_code, 200)

    def test_order_deletion(self):
        res = self.client().post( '/orders', data=self.order)
        res.assertEqual(res.status_code, 201)

        res = self.client().delete('/orders/1')
        self.assertEqual(res.status_code, 200)

        res = self.client().get('/orders/1')
        self.assertEqual(res.status_code, 404)

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()


class UserTestCase(unittest.TestCase):
    """ Will test user model"""

    def setUp(self):
        self.app = create_app(config_name='testing')
        self.client = self.app.test_client
        self.user = {'username': 'John', 'email': 'john2@doe.com', 
                     'password': 'secret'}

        with self.app.app_context():
            db.create_all()

    def test_user_creation(self):
        res = self.client().post('/users', data=self.user)
        self.assertEqual(res.status_code, 201)
        self.assertIn('id', res.data)

    def test_can_get_all_users(self):
        res = self.client().post('/users', data=self.user)
        self.assertEqual(res.status_code, 201)
        res = self.client().get('/users')
        self.assertEqual(res.status_code, 200)

    def test_can_get_user_by_id(self):
        res = self.client().post('/users', data=self.user)
        self.assertEqual(res.status_code, 201)
        json_result = json.loads(res.data.decode('utf-8').replace("'", "\""))
        res = self.client().get(
            '/users/{}'.format(json_result['id'])
        )
        self.assertEqual(res.status_code, 200)
        self.assertIn('id', res.data)

    def test_user_can_be_updated(self):
        res = self.client().post('/users', data=self.user)
        self.assertEqual(res.status_code, 201)

        res = self.client().put(
            '/users/1',
            data={
                'username': 'Doe',
            }
        )
        self.assertEqual(res.status_code, 200)
        res = self.client().get('/users/1')
        self.assertEqual('Doe', res.data)

    def test_user_deletion(self):
        res = self.client().post('/users', data=self.user)
        self.assertEqual(res.status_code, 201)
        res = self.client().delete('/users/1')
        self.assertEqual(res.status_code, 200)

        res = self.client().get('/users/1')
        self.assertEqual(res.status_code, 404)

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()


if __name__ == '__main__':
    unittest.main()

