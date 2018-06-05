"""Test the base model methods"""


import unittest
from app import create_app, db
from app.models import User


class BaseModelTest(unittest.TestCase):
    """Test the basemodel methods by testing a user model"""

    def setUp(self):
        """Create an application"""
        self.app = create_app(config_name='testing')
        with self.app.app_context():
            db.create_all()

    def test_model_saving(self):
        """Test model creation"""
        with self.app.app_context():
            user = User(username='John', email='test@mail.com', password='secret')
            user.save()
            user = User.query.get(1)
            self.assertEqual(user.username, 'John')

    def test_model_delete(self):
        """Test model deletion"""
        with self.app.app_context():
            user = User(username='John', email='test@mail.com', password='secret')
            user.save()
            user.delete()
            user = User.query.get(1)
            self.assertEqual(user, None)

    def tearDown(self):
        """Drop database"""
        with self.app.app_context():
            db.session.remove()
            db.drop_all()


