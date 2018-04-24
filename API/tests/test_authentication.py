import os
import json
import unittest
from app import create_app, db

class AuthenticationTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(config_name='testing')
        self.client = self.app.test_client
        self.user = {'name': 'John', 'email': 'john@doe.com', 
                     'password': 'secret'}

        with self.app.app_context():
            db.create_all()

    def test_user_can_signup(self):
        res = self.client().post('/users/auth', data=self.user)
        self.assertEqual(res.status_code, 201)

    def test_user_can_login(self):
        res = self.client().post('/users/auth', data=self.user)
