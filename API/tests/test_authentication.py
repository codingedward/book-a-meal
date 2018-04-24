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
