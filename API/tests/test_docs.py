"""Test access to documentation"""


import unittest
from app import create_app


class DocsTest(unittest.TestCase):
    """Test API documentation access"""
    def setUp(self):
        """Create an application"""
        self.app = create_app(config_name='testing')
        self.client = self.app.test_client

    def test_can_get_docs(self):
        """Test can get an application"""
        res = self.client().get('/')
        self.assertEqual(res.status_code, 200)
        self.assertIn(b'Andela Book A Meal', res.data)

    def test_can_handle_http_error(self):
        """Test can handle missing endpoint"""
        res = self.client().get('/non-existent')
        self.assertIn(b'Not Found', res.data)
