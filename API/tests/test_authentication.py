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
            'password': 'secret',
            'confirm_password': 'secret'
        })
        self.headers = {'Content-Type' : 'application/json'} 
        with self.app.app_context():
            db.create_all()

    def test_user_can_signup(self):
        res = self.client().post('/api/v1/auth/signup',
                                 data=self.user, headers=self.headers)
        self.assertEqual(res.status_code, 201)

    def test_cannot_signup_without_username(self):
        res = self.client().post(
            '/api/v1/auth/signup', 
            data=json.dumps({
                'email': 'john@doe.com', 
                'password': 'secret',
                'confirm_password': 'secret'
            }),
            headers=self.headers
        )
        self.assertEqual(res.status_code, 400)
        self.assertIn(b'Username', res.data)

    def test_cannot_signup_without_email(self):
        res = self.client().post(
            '/api/v1/auth/signup', 
            data=json.dumps({
                'username': 'John',
                'password': 'secret',
                'confirm_password': 'secret'
            }),
            headers=self.headers
        )
        self.assertEqual(res.status_code, 400)
        self.assertIn(b'Email', res.data)

    def test_cannot_signup_without_password(self):
        res = self.client().post(
            '/api/v1/auth/signup', 
            data=json.dumps({
                'username': 'John',
                'email': 'john@doe.com', 
                'confirm_password': 'secret'
            }),
            headers=self.headers
        )
        self.assertEqual(res.status_code, 400)
        self.assertIn(b'Password', res.data)

    def test_cannot_signup_without_password_confirmation(self):
        res = self.client().post(
            '/api/v1/auth/signup', 
            data=json.dumps({
                'username': 'John',
                'email': 'john@doe.com', 
                'password': 'secret',
            }),
            headers=self.headers
        )
        self.assertEqual(res.status_code, 400)
        self.assertIn(b'Password confirmation', res.data)

    def test_cannot_signup_without_password_matching(self):
        res = self.client().post(
            '/api/v1/auth/signup', 
            data=json.dumps({
                'username': 'John',
                'email': 'john@doe.com', 
                'password': 'secret',
                'confirm_password': 'secre'
            }),
            headers=self.headers
        )
        self.assertEqual(res.status_code, 400)

    def test_cannot_signup_with_wrong_email(self):
        res = self.client().post(
            '/api/v1/auth/signup', 
            data=json.dumps({
                'username': 'John',
                'email': 'johndoe.com', 
                'password': 'secret',
                'confirm_password': 'secret'
            }),
            headers=self.headers
        )
        self.assertEqual(res.status_code, 400)
        self.assertIn(b'provide a valid email', res.data)

    def test_cannot_signup_with_short_username(self):
        res = self.client().post(
            '/api/v1/auth/signup', 
            data=json.dumps({
                'username': 'Jo',
                'email': 'john@doe.com', 
                'password': 'secret',
                'confirm_password': 'secret'
            }),
            headers=self.headers
        )
        self.assertEqual(res.status_code, 400)
        self.assertIn(b'Username', res.data)

    def test_cannot_signup_with_short_password(self):
        res = self.client().post(
            '/api/v1/auth/signup', 
            data=json.dumps({
                'username': 'John',
                'email': 'john@doe.com', 
                'password': 'sec',
                'confirm_password': 'sec'
            }),
            headers=self.headers
        )
        self.assertEqual(res.status_code, 400)
        self.assertIn(b'least 6 characters', res.data)

    def test_user_cannot_login_without_email(self):
        res = self.client().post('/api/v1/auth/signup',
                                 data=self.user, headers=self.headers)
        res = self.client().post(
            '/api/v1/auth/login', 
            data=json.dumps({
                'password': 'secret',
            }),
            headers=self.headers
        )
        self.assertEqual(res.status_code, 400)
        self.assertIn(b'Email is required', res.data)

    def test_user_cannot_login_without_password(self):
        res = self.client().post('/api/v1/auth/signup',
                                 data=self.user, headers=self.headers)
        res = self.client().post(
            '/api/v1/auth/login', 
            data=json.dumps({
                'email': 'john@doe.com', 
            }),
            headers=self.headers
        )
        self.assertEqual(res.status_code, 400)
        self.assertIn(b'Password is required', res.data)

    def test_user_cannot_login_with_wrong_credentials(self):
        res = self.client().post('/api/v1/auth/signup',
                                 data=self.user, headers=self.headers)
        res = self.client().post(
            '/api/v1/auth/login', 
            data=json.dumps({
                'email': 'john@doe.com', 
                'password': 'pass', 
            }),
            headers=self.headers
        )
        self.assertEqual(res.status_code, 400)
        self.assertIn(b'Invalid credentials', res.data)

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
        self.assertIn(b'logged out', res.data)

    def test_can_get_user(self):
        res = self.client().post('/api/v1/auth/signup',
                                 data=self.user, headers=self.headers)
        res = self.client().post(
            '/api/v1/auth/login', 
            data=self.user,
            headers=self.headers
        )
        json_result = json.loads(res.get_data(as_text=True))
        res = self.client().get(
            '/api/v1/auth/get',
            data=self.user,
            headers={
                'Content-Type' : 'application/json',
                'Authorization': 'Bearer {}'.format(json_result['access_token'])
            }
        )
        json_result = json.loads(res.get_data(as_text=True))
        self.assertEqual(res.status_code, 200)
        self.assertEqual(json_result['user']['email'], 'john@doe.com')

    def test_cannot_access_unauthorized_endpoint(self):
        res = self.client().post('/api/v1/auth/signup',
                                 data=self.user, headers=self.headers)
        res = self.client().post(
            '/api/v1/auth/login', 
            data=self.user,
            headers=self.headers
        )
        json_result = json.loads(res.get_data(as_text=True))
        res = self.client().post(
            '/api/v1/notifications',
            data=json.dumps({
                'title': 'Title',
                'message': 'Message'
            }),
            headers={
                'Content-Type' : 'application/json',
                'Authorization': 'Bearer {}'.format(json_result['access_token'])
            }
        )
        self.assertEqual(res.status_code, 401)
        self.assertIn(b'Unauthorized access', res.data)

    def test_cannot_access_protected_endpoint_without_authentication(self):
        res = self.client().get('/api/v1/auth/get')
        self.assertEqual(res.status_code, 401)
        self.assertIn(b'Missing Authorization Header', res.data)


    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()


if __name__ == '__main__':
    unittest.main()
