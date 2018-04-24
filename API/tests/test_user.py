import os
import json
import unittest
from app import create_app, db


class UserTestCase(unittest.TestCase):

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


