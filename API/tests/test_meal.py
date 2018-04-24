import os
import json
import unittest
from app import create_app, db


class MealTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(config_name='testing')
        self.client = self.app.test_client
        self.meal = {'name': 'Ugali', 'img_path': '#', 'cost': 200.0}

        with self.app.app_context():
            db.create_all()

    def test_meal_creation(self):
        res = self.client().post('/meals', data=self.meal)
        self.assertEqual(res.status_code, 201)
        self.assertIn('id', res.data.keys())

    def test_can_get_all_meals(self):
        res = self.client().post('/meals', data=self.meal)
        self.assertEqual(res.status_code, 201)
        res = self.client().get('/meals')
        self.assertEqual(res.status_code, 200)

    def test_can_get_meal_by_id(self):
        res = self.client().post('/meals', data=self.meal)
        self.assertEqual(res.status_code, 201)
        json_result = json.loads(res.data.decode('utf-8').replace("'", "\""))
        res = self.client().get(
            '/meals/{}'.format(json_result['id'])
        )
        self.assertEqual(res.status_code, 200)
        self.assertIn('id', res.data)

    def test_meal_can_be_updated(self):
        res = self.client().post('/meals', data=self.meal)
        self.assertEqual(res.status_code, 201)
        res = self.client().put(
            '/meals/1',
            data={
                'name': 'Sembe',
                'img_path': '#',
                'cost': 200.0
            }
        )
        self.assertEqual(res.status_code, 200)
        res = self.client().get('/meals/1')
        self.assertEqual('Sembe', res.data)

    def test_meal_deletion(self):
        res = self.client().post('/meals', data=self.meal)
        self.assertEqual(res.status_code, 201)
        res = self.client().delete('/meals/1')
        self.assertEqual(res.status_code, 200)

        res = self.client().get('/meals/1')
        self.assertEqual(res.status_code, 404)

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()


