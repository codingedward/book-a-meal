import os
import json
import unittest
from app import create_app, db


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


