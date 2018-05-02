import json
import unittest
from app import create_app, db
from app.models import User, UserType

class AuthenticationTestCase(unittest.TestCase):
    """ This will test authentication endpoints"""

    def setUp(self):
        self.app = create_app(config_name='testing')
        self.client = self.app.test_client
        self.user = json.dumps({
            'username': 'John',
            'email': 'john@doe.com', 
            'password': 'secret'
        })
        self.headers = {'Content-Type' : 'application/json'} 

        with self.app.app_context():
            db.create_all()

    def test_user_can_signup(self):
        res = self.client().post('/api/v1/auth/signup',
                                 data=self.user, headers=self.headers)
        self.assertEqual(res.status_code, 201)

    def test_user_can_login(self):
        res = self.client().post('/api/v1/auth/signup',
                                 data=self.user, headers=self.headers)
        res = self.client().post(
            '/api/v1/auth/login', 
            data=self.user,
            headers=self.headers
        )
        self.assertEqual(res.status_code, 200)
        self.assertIn(b'token', res.data)

    def test_user_can_logout(self):
        res = self.client().post('/api/v1/auth/signup',
                                 data=self.user, headers=self.headers)
        res = self.client().post(
            '/api/v1/auth/login', 
            data=self.user,
            headers=self.headers
        )
        self.assertEqual(res.status_code, 200)
        self.assertIn(b'token', res.data)

        json_result = json.loads(res.get_data(as_text=True))
        res = self.client().delete(
            '/api/v1/auth/logout',
            headers={
                'Accept': 'application/json',
                'Content-Type' : 'application/json',
                'Authorization': 'Bearer {}'.format(json_result['access_token'])
            }
        )
        self.assertEqual(res.status_code, 200)

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()


if __name__ == '__main__':
    unittest.main()
