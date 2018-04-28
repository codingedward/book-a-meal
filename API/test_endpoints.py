import os
import json
import unittest
from app import create_app 
from app.model import MealType
from app.api import bam


class BaseTest(unittest.TestCase):
    def authenticate(self):
        self.app = create_app(config_name='testing')
        self.client = self.app.test_client
        self.user = json.dumps({
            'username': 'John', 
            'email': 'john@doe.com', 
            'password': 'secretservice'
        })
        res = self.client().post( 
            '/api/v1/auth/register', 
            data=self.user, 
            headers={'Content-Type' : 'application/json'}
        )
        res = self.client().post(
            '/api/v1/auth/login', 
            data=json.dumps({ 
                'email': 'john@doe.com', 
                'password': 'secretservice' 
            }), 
            headers={'Content-Type' : 'application/json'}
        )

        json_result = json.loads(res.get_data(as_text=True))
        self.customer_headers = {
            'Content-Type' : 'application/json', 
            'Authorization': 'Bearer {}'.format(json_result['access_token'])} 

        res = self.client().post(
            '/api/v1/auth/login',
            data=json.dumps({ 
                'email': os.getenv('DEFAULT_ADMIN_EMAIL'), 
                'password': os.getenv('DEFAULT_ADMIN_PASSWORD'), 
            }), 
            headers={'Content-Type' : 'application/json'}
        )
        json_result = json.loads(res.get_data(as_text=True))
        self.caterer_headers = {
            'Content-Type' : 'application/json', 
            'Authorization': 'Bearer {}'.format(json_result['access_token'])
        } 

    def tearDown(self):
        bam.clear()


class MealTestCase(BaseTest):
    """ This will test meal resource endpoints"""

    def setUp(self):
        self.app = create_app(config_name='testing')
        self.client = self.app.test_client
        self.meal = json.dumps({
            'name': 'Ugali',
            'img_path': '#',
            'cost': 200.0
        })
        self.authenticate()

    def test_meal_creation(self):
        res = self.client().post('/api/v1/meals',
                                 data=self.meal, headers=self.caterer_headers)
        json_result = json.loads(res.get_data(as_text=True))
        self.assertEqual(res.status_code, 201)
        self.assertEqual(json_result['name'], 'Ugali')
        self.assertEqual(json_result['cost'], 200)

    def test_can_get_all_meals(self):
        res = self.client().post('/api/v1/meals',
                                 data=self.meal, headers=self.caterer_headers)
        self.assertEqual(res.status_code, 201)
        res = self.client().get('/api/v1/meals')

        json_result = json.loads(res.get_data(as_text=True))
        self.assertEqual(res.status_code, 200)
        self.assertEqual(json_result['num_results'], 1)
        self.assertIn(b'objects', res.data)

    def test_can_get_meal_by_id(self):
        res = self.client().post('/api/v1/meals',
                                 data=self.meal, headers=self.caterer_headers)
        self.assertEqual(res.status_code, 201)
        json_result = json.loads(res.get_data(as_text=True))
        res = self.client().get(
            '/api/v1/meals/{}'.format(json_result['id'])
        )

        json_result = json.loads(res.get_data(as_text=True))
        self.assertEqual(res.status_code, 200)
        self.assertEqual(json_result['name'], 'Ugali')
        self.assertEqual(json_result['cost'], 200)

    def test_meal_can_be_updated(self):
        res = self.client().post('/api/v1/meals',
                                 data=self.meal, headers=self.caterer_headers)
        self.assertEqual(res.status_code, 201)
        res = self.client().patch(
            '/api/v1/meals/1',
            data=json.dumps({
                'name': 'Sembe',
                'img_path': '#',
                'cost': 300.0
            }),
            headers=self.caterer_headers
        )
        self.assertEqual(res.status_code, 200)
        res = self.client().get('/api/v1/meals/1', headers=self.caterer_headers)

        json_result = json.loads(res.get_data(as_text=True))
        self.assertEqual(res.status_code, 200)
        self.assertEqual(json_result['name'], 'Sembe')
        self.assertEqual(json_result['cost'], 300)

    def test_meal_deletion(self):
        res = self.client().post(
            '/api/v1/meals', 
            data=self.meal, 
            headers=self.caterer_headers
        )
        self.assertEqual(res.status_code, 201)
        res = self.client().delete('/api/v1/meals/1',
                                   headers=self.caterer_headers)
        self.assertEqual(res.status_code, 204)

        res = self.client().get('/api/v1/meals/1')
        self.assertEqual(res.status_code, 404)



class NotificationTestCase(BaseTest):
    """ This will test notification resource endpoints"""

    def setUp(self):
        self.app = create_app(config_name='testing')
        self.client = self.app.test_client
        self.headers = {'Content-Type' : 'application/json'} 
        bam.post_user({
            'username': 'john',
            'email': 'john@bam.com',
            'password': 'secret'
        })
        self.notification = json.dumps({
            'user_id': 1,
            'title': 'Hello there',
            'message': 'I have a message for you',
        })
        self.authenticate()


    def test_notification_creation(self):
        res = self.client().post('/api/v1/notifications',
                                 data=self.notification, 
                                 headers=self.caterer_headers)
        json_result = json.loads(res.get_data(as_text=True))

        self.assertEqual(res.status_code, 201)
        self.assertEqual(json_result['title'], 'Hello there')

    def test_can_get_all_notifications(self):
        res = self.client().post('/api/v1/notifications',
                                 data=self.notification, 
                                 headers=self.customer_headers)
        self.assertEqual(res.status_code, 201)
        res = self.client().get('/api/v1/notifications', 
                                headers=self.customer_headers)
        json_result = json.loads(res.get_data(as_text=True))
        self.assertEqual(res.status_code, 200)
        self.assertEqual(json_result['num_results'], 1)
        self.assertIn(b'objects', res.data)

    def test_can_get_notification_by_id(self):
        res = self.client().post('/api/v1/notifications',
                                 data=self.notification, 
                                 headers=self.customer_headers)
        self.assertEqual(res.status_code, 201)

        json_result = json.loads(res.get_data(as_text=True))
        res = self.client().get(
            '/api/v1/notifications/{}'.format(json_result['id']),
            headers=self.customer_headers
        )

        json_result = json.loads(res.get_data(as_text=True))
        self.assertEqual(res.status_code, 200)
        self.assertEqual(json_result['title'], 'Hello there')

    def test_notification_can_be_updated(self):
        res = self.client().post('/api/v1/notifications',
                                 data=self.notification, 
                                 headers=self.customer_headers)
        self.assertEqual(res.status_code, 201)

        res = self.client().patch(
            '/api/v1/notifications/1',
            data=json.dumps({
                'user_id': 1,
                'title': 'Hi',
                'message': 'I have a message for you',
            }),
            headers=self.caterer_headers
        )
        self.assertEqual(res.status_code, 200)

        res = self.client().get('/api/v1/notifications/1', 
                                headers=self.customer_headers)
        json_result = json.loads(res.get_data(as_text=True))

        self.assertEqual(res.status_code, 200)
        self.assertEqual(json_result['title'], 'Hi')

    def test_notification_deletion(self):
        res = self.client().post('/api/v1/notifications',
                                 data=self.notification, 
                                 headers=self.customer_headers)
        self.assertEqual(res.status_code, 201)

        res = self.client().delete('/api/v1/notifications/1',
                                   headers=self.customer_headers)
        self.assertEqual(res.status_code, 204)

        res = self.client().get('/api/v1/notifications/1',
                                headers=self.customer_headers)
        self.assertEqual(res.status_code, 404)


class OrderTestCase(BaseTest):
    """ This will test order resource endpoints"""

    def setUp(self):
        self.app = create_app(config_name='testing')
        self.client = self.app.test_client
        self.headers = {'Content-Type' : 'application/json'} 
        bam.post_meal({
            'name': 'Ugali',
            'img_path': '#',
            'cost': 200.0
        })
        bam.post_menu({
            'meal_id': 1,
            'category': MealType.BREAKFAST
        })
        bam.post_user({
            'username': 'john',
            'email': 'john@bam.com',
            'password': 'supersecret'
        })
        self.order = json.dumps({
            'menu_id': 1,
            'user_id': 1,
        })
        self.authenticate()

    def test_order_creation(self):
        res = self.client().post('/api/v1/orders', 
                                 data=self.order,
                                 headers=self.caterer_headers)
        json_result = json.loads(res.get_data(as_text=True))

        self.assertEqual(res.status_code, 201)
        self.assertEqual(json_result['user_id'], 1)

    def test_can_get_all_orders(self):
        res = self.client().post('/api/v1/orders', data=self.order,
                                 headers=self.caterer_headers)
        self.assertEqual(res.status_code, 201)
        res = self.client().get('/api/v1/orders', 
                                headers=self.caterer_headers)

        json_result = json.loads(res.get_data(as_text=True))
        self.assertEqual(res.status_code, 200)
        self.assertEqual(json_result['num_results'], 1)
        self.assertIn(b'objects', res.data)

    def test_can_get_order_by_id(self):
        res = self.client().post('/api/v1/orders', data=self.order,
                                 headers=self.caterer_headers)
        self.assertEqual(res.status_code, 201)

        json_result = json.loads(res.get_data(as_text=True))
        res = self.client().get(
            '/api/v1/orders/{}'.format(json_result['id']),
            headers=self.caterer_headers
        )
        json_result = json.loads(res.get_data(as_text=True))
        self.assertEqual(res.status_code, 200)
        self.assertEqual(json_result['user_id'], 1)

    def test_order_can_be_updated(self):
        res = self.client().post('/api/v1/orders', data=self.order,
                                 headers=self.caterer_headers)
        self.assertEqual(res.status_code, 201)
        bam.post_user({
            'username': 'john2',
            'email': 'john2@bam.com',
            'password': 'supersecret'
        })
        res = self.client().patch(
            '/api/v1/orders/1',
            data=json.dumps({
                'menu_id': 1,
                'user_id': 2,
            }),
            headers=self.caterer_headers
        )
        self.assertEqual(res.status_code, 200)

        res = self.client().get('/api/v1/orders/1', 
                                headers=self.caterer_headers)
        json_result = json.loads(res.get_data(as_text=True))

        self.assertEqual(res.status_code, 200)
        self.assertEqual(json_result['user_id'], 2)

    def test_order_deletion(self):
        res = self.client().post('/api/v1/orders', data=self.order,
                                 headers=self.caterer_headers)
        self.assertEqual(res.status_code, 201)

        res = self.client().delete('/api/v1/orders/1', 
                                   headers=self.caterer_headers)
        self.assertEqual(res.status_code, 204)
        res = self.client().get('/api/v1/orders/1', 
                                headers=self.caterer_headers)
        self.assertEqual(res.status_code, 404)


class MenuTestCase(BaseTest):
    """ This will test menu resource endpoints"""

    def setUp(self):
        self.app = create_app(config_name='testing')
        self.client = self.app.test_client
        meal = bam.post_meal({
            'name': 'Ugali',
            'img_path': '#',
            'cost': 200.0
        })
        self.menu = json.dumps({
            'meal_id': meal['id'],
            'category': MealType.BREAKFAST
        })
        self.headers = {'Content-Type' : 'application/json'} 
        self.authenticate()


    def test_menu_creation(self):
        res = self.client().post('/api/v1/menus',
                                 data=self.menu, 
                                 headers=self.caterer_headers)

        json_result = json.loads(res.get_data(as_text=True))
        self.assertEqual(res.status_code, 201)
        self.assertEqual(json_result['category'], MealType.BREAKFAST)

    def test_can_get_all_menus(self):
        res = self.client().post('/api/v1/menus',
                                 data=self.menu,
                                 headers=self.caterer_headers)
        self.assertEqual(res.status_code, 201)
        res = self.client().get('/api/v1/menus')

        json_result = json.loads(res.get_data(as_text=True))
        self.assertEqual(res.status_code, 200)
        self.assertEqual(json_result['num_results'], 1)
        self.assertIn(b'objects', res.data)

    def test_can_get_menu_by_id(self):
        res = self.client().post('/api/v1/menus',
                                 data=self.menu, headers=self.caterer_headers)
        self.assertEqual(res.status_code, 201)
        json_result = json.loads(res.get_data(as_text=True))
        res = self.client().get(
            '/api/v1/menus/{}'.format(json_result['id']),
            headers=self.caterer_headers
        )

        json_result = json.loads(res.get_data(as_text=True))
        self.assertEqual(res.status_code, 200)
        self.assertEqual(json_result['category'], MealType.BREAKFAST)

    def test_menu_can_be_updated(self):
        res = self.client().post('/api/v1/menus',
                                 data=self.menu, 
                                 headers=self.caterer_headers)
        self.assertEqual(res.status_code, 201)
        res = self.client().patch(
            '/api/v1/menus/1',
            data=json.dumps({
                'meal_id': 1,
                'category': MealType.LUNCH
            }),
            headers=self.caterer_headers
        )

        self.assertEqual(res.status_code, 200)
        res = self.client().get('/api/v1/menus/1', 
                                headers=self.caterer_headers)

        json_result = json.loads(res.get_data(as_text=True))
        self.assertEqual(res.status_code, 200)
        self.assertEqual(json_result['category'], MealType.LUNCH)

    def test_menu_deletion(self):
        res = self.client().post('/api/v1/menus',
                                 data=self.menu, headers=self.caterer_headers)
        self.assertEqual(res.status_code, 201)

        res = self.client().delete('/api/v1/menus/1',
                                   headers=self.caterer_headers)

        self.assertEqual(res.status_code, 204)
        res = self.client().get('/api/v1/menus/1', headers=self.caterer_headers)
        self.assertEqual(res.status_code, 404)

class AuthenticationTestCase(BaseTest):
    def setUp(self):
        self.app = create_app(config_name='testing')
        self.client = self.app.test_client
        self.headers = {'Content-Type' : 'application/json'} 
        self.user = json.dumps({
            'username': 'Jane', 
            'email': 'jane@doe.com', 
            'password': 'secretservice'
        })

    def test_user_can_signup(self):
        res = self.client().post('/api/v1/auth/signup', 
                                 data=self.user,
                                 headers=self.headers)
        self.assertEqual(res.status_code, 201)
        self.assertIn(b'Jane', res.data)

    def test_user_can_login(self):
        res = self.client().post('/api/v1/auth/login', 
                                 data=self.user,
                                 headers=self.headers)
        self.assertEqual(res.status_code, 200)
        self.assertIn(b'token', res.data)

    def test_user_can_logout(self):
        res = self.client().post('/api/v1/auth/login', 
                                 data=self.user,
                                 headers=self.headers)
        json_result = json.loads(res.get_data(as_text=True))
        headers = {
            'Content-Type' : 'application/json', 
            'Authorization': 'Bearer {}'.format(json_result['access_token'])} 
        res = self.client().delete('/api/v1/auth/logout', 
                                   headers=headers)
        self.assertEqual(res.status_code, 200)

    def tearDown(self):
        with self.app.app_context():
            bam.clear()

if __name__ == '__main__':
    unittest.main()
