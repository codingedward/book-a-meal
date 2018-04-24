import os
import json
import unittest
from app import create_app, db
from app.models import MealType


class MenuTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(config_name='testing')
        self.client = self.app.test_client

        res = self.client().post(
            '/meals', 
            data={ 
                'name': 'Ugali', 
                'img_path': '#', 
                'cost': 200.0
            }
        )

        json_result = json.loads(res.data.decode('utf-8').replace("'", "\""))
        self.meal_id = json_result['id']

        with self.app.app_context():
            db.create_all()

    def test_menu_creation(self):
        res = self.client().post(
            '/menus',
            data={
                'meal_id': self.meal_id,
                'category': MealType.BREAKFAST,
            }
        )
        res.assertEqual(res.status_code, 201)
        res.assertIn('id', res.data)


    def test_can_get_all_menus(self):
        res = self.client().post(
            '/menus',
            data={
                'meal_id': self.meal_id,
                'category': MealType.BREAKFAST,
            }
        )
        res.assertEqual(res.status_code, 201)

        res = self.client().get('/menus')
        self.assertEqual(res.status_code, 200)

    def test_can_get_menu_by_id(self):
        res = self.client().post(
            '/menus',
            data={
                'meal_id': self.meal_id
                'category': MealType.BREAKFAST,
            }
        )
        res.assertEqual(res.status_code, 201)

        json_result = json.loads(res.data.decode('utf-8').replace("'", "\""))
        res = self.client().get(
            '/menus/{}'.format(json_result['id'])
        )
        self.assertEqual(res.status_code, 200)
        self.assertIn('id', res.data)

    def test_menu_can_be_updated(self):
        res = self.client().post(
            '/menus',
            data={
                'meal_id': self.meal_id,
                'category': MealType.BREAKFAST,
            }
        )
        res.assertEqual(res.status_code, 201)

        json_result = json.loads(res.data.decode('utf-8').replace("'", "\""))
        res = self.client().put(
            '/menus/1',
            data={
                'meal_id': json_result['id'],
                'category': MealType.LUNCH,
            }
        )
        self.assertEqual(res.status_code, 200)

    def test_menu_deletion(self):
        res = self.client().post(
            '/menus',
            data={
                'meal_id': self.meal_id,
                'category': MealType.BREAKFAST,
            }
        )
        res.assertEqual(res.status_code, 201)

        res = self.client().delete('/menus/1')
        self.assertEqual(res.status_code, 200)

        res = self.client().get('/menus/1')
        self.assertEqual(res.status_code, 404)

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()


