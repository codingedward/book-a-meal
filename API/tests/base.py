import json
import unittest
from app import create_app, db
from app.models import User, UserType


class BaseTest(unittest.TestCase):
    """This will hold the basic methods required by other tests, for
    example authentication in order to test guarded endpoints
    """
    def loginCustomer(self, email='customer@mail.com'):
        """Logs a user in and returns their id and access token """
        with self.app.app_context():
            user = User.query.filter_by(email=email).first()
            if not user:
                user = User(username='John', email=email,
                            password='secret')
                user.save()

            # log this user in for the auth token
            res = self.client().post(
                '/api/v1/auth/login',
                data=json.dumps({
                    'email': email,
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
        """Logs a caterer in and returns their id and access token """
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
        """Drop database"""
        with self.app.app_context():
            db.session.remove()
            db.drop_all()
