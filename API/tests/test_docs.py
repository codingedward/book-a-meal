import unittest
from app import create_app


class DocsTest(unittest.TestCase):
    def setUp(self):
        self.app = create_app(config_name='testing')
        self.client = self.app.test_client

    def test_can_get_docs(self):
        res = self.client().get('/')
        self.assertEqual(res.status_code, 200)
        self.assertIn(b'Andela Book A Meal', res.data)

    def test_can_handle_http_error(self):
        res = self.client().get('/non-existent')
        self.assertIn(b'Not Found', res.data)
