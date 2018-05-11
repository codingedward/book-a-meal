import os
import json
import unittest
from app import create_app, db
from app.models import User, UserType


class BaseTest(unittest.TestCase):
    """ 
    This will hold the basic methods required by other tests, for 
    example authentication in order to test guarded endpoints
    """
    def loginCustomer(self):
        with self.app.app_context():
            user_email = 'customer@mail.com'
            user = User.query.filter_by(email=user_email).first()
            if not user:
                user = User(username='John', email='customer@mail.com',
                            password='secret')
                user.save()

            # log this user in for the auth token
            res = self.client().post(
                '/api/v1/auth/login',
                data=json.dumps({
                    'email': 'customer@mail.com',
                    'password': 'secret'
                }),
                headers={'Content-Type' : 'application/json'}
            )

            json_result = json.loads(res.get_data(as_text=True))
            return  {
                'Content-Type' : 'application/json',
                'Authorization': 'Bearer {}'.format(json_result['access_token'])
            }, user.id

    def loginCaterer(self):
        with self.app.app_context():
            # create a temporary caterer
            user = User(username="John", email="caterer@mail.com", 
                        password="secret", role=UserType.CATERER)
            user.save()

            # log this caterer in and obtain headers for the auth token
            res = self.client().post(
                '/api/v1/auth/login',
                data=json.dumps({
                    'email': 'caterer@mail.com',
                    'password': 'secret'
                }),
                headers={'Content-Type' : 'application/json'}
            )
            json_result = json.loads(res.get_data(as_text=True))
            return {
                'Content-Type' : 'application/json',
                'Authorization': 'Bearer {}'.format(json_result['access_token'])
            }, user.id

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()
