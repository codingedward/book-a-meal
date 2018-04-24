import os
import json
import unittest
from app import create_app, db


class NotificationTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(config_name='testing')
        self.client = self.app.test_client

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


