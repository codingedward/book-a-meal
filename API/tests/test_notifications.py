import json
import unittest
from app import create_app, db
from tests.base import BaseTest


class NotificationTestCase(BaseTest):
    """ This will test notification resource endpoints"""

    def setUp(self):
        self.app = create_app(config_name='testing')
        self.client = self.app.test_client
        self.headers = {'Content-Type' : 'application/json'} 
        self.notification = {
            'title': 'Hello there',
            'message': 'I have a message for you',
        }

        with self.app.app_context():
            db.create_all()

    def test_notification_creation(self):
        caterer_header, _ = self.loginCaterer()
        customer_header, id = self.loginCustomer()
        self.notification['user_id'] = id
        res = self.client().post('/api/v1/notifications',
                                 data=json.dumps(self.notification), 
                                 headers=caterer_header)
        json_result = json.loads(res.get_data(as_text=True))

        self.assertEqual(res.status_code, 201)
        self.assertEqual(json_result['title'], 'Hello there')

    def test_can_get_all_notifications(self):
        caterer_header, _ = self.loginCaterer()
        customer_header, id = self.loginCustomer()
        self.notification['user_id'] = id
        res = self.client().post('/api/v1/notifications',
                                 data=json.dumps(self.notification), 
                                 headers=caterer_header)
        self.assertEqual(res.status_code, 201)

        customer_header, _ = self.loginCustomer()
        res = self.client().get('/api/v1/notifications', headers=customer_header)

        json_result = json.loads(res.get_data(as_text=True))
        self.assertEqual(res.status_code, 200)
        self.assertEqual(json_result['num_results'], 1)
        self.assertIn(b'objects', res.data)

    def test_can_get_notification_by_id(self):
        caterer_header, _ = self.loginCaterer()
        customer_header, id = self.loginCustomer()
        self.notification['user_id'] = id
        res = self.client().post('/api/v1/notifications',
                                 data=json.dumps(self.notification), 
                                 headers=caterer_header)
        self.assertEqual(res.status_code, 201)

        json_result = json.loads(res.get_data(as_text=True))
        res = self.client().get(
            '/api/v1/notifications/{}'.format(json_result['id']),
            headers=customer_header
        )

        json_result = json.loads(res.get_data(as_text=True))
        self.assertEqual(res.status_code, 200)
        self.assertEqual(json_result['title'], 'Hello there')

    def test_notification_can_be_updated(self):
        caterer_header, _ = self.loginCaterer()
        customer_header, id = self.loginCustomer()
        self.notification['user_id'] = id
        res = self.client().post('/api/v1/notifications',
                                 data=json.dumps(self.notification), 
                                 headers=caterer_header)
        self.assertEqual(res.status_code, 201)

        self.notification['title'] = 'Hi'
        res = self.client().put(
            '/api/v1/notifications/1',
            data=json.dumps(self.notification), 
            headers=caterer_header
        )
        self.assertEqual(res.status_code, 200)
        res = self.client().get('/api/v1/notifications/1', 
                                headers=customer_header)
        json_result = json.loads(res.get_data(as_text=True))

        self.assertEqual(res.status_code, 200)
        self.assertEqual(json_result['title'], 'Hi')

    def test_notification_deletion(self):
        caterer_header, _ = self.loginCaterer()
        customer_header, id = self.loginCustomer()
        self.notification['user_id'] = id
        res = self.client().post('/api/v1/notifications',
                                 data=json.dumps(self.notification), 
                                 headers=caterer_header)
        self.assertEqual(res.status_code, 201)

        customer_header, _ = self.loginCustomer()
        res = self.client().delete('/api/v1/notifications/1',
                                   headers=customer_header)
        self.assertEqual(res.status_code, 200)

        res = self.client().get('/api/v1/notifications/1',
                                headers=caterer_header)
        self.assertEqual(res.status_code, 404)


if __name__ == '__main__':
    unittest.main()
