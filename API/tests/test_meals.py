import json
import unittest
from app import create_app, db
from tests.base import BaseTest


class MealTestCase(BaseTest):
    """ This will test meal resource endpoints """

    def setUp(self):
        self.app = create_app(config_name='testing')
        self.client = self.app.test_client
        self.meal = json.dumps({
            'name': 'Ugali',
            'img_path': '#',
            'cost': 200.0
        })
        self.headers = {'Content-Type' : 'application/json'} 

        with self.app.app_context():
            db.create_all()

    def test_meal_creation(self):
        caterer_header, _ = self.loginCaterer()
        res = self.client().post('/api/v1/meals',
                                 data=self.meal, headers=caterer_header)
        json_result = json.loads(res.get_data(as_text=True))
        self.assertEqual(res.status_code, 201)
        self.assertEqual(json_result['name'], 'Ugali')
        self.assertEqual(json_result['cost'], 200)

    def test_can_get_all_meals(self):
        caterer_header, id = self.loginCaterer()
        res = self.client().post('/api/v1/meals',
                                 data=self.meal, headers=caterer_header)
        self.assertEqual(res.status_code, 201)
        res = self.client().get('/api/v1/meals', headers=caterer_header)

        json_result = json.loads(res.get_data(as_text=True))
        self.assertEqual(res.status_code, 200)
        self.assertEqual(json_result['num_results'], 1)
        self.assertIn(b'objects', res.data)

    def test_can_get_meal_by_id(self):
        caterer_header, id = self.loginCaterer()
        res = self.client().post('/api/v1/meals',
                                 data=self.meal, headers=caterer_header)
        self.assertEqual(res.status_code, 201)
        json_result = json.loads(res.get_data(as_text=True))
        res = self.client().get(
            '/api/v1/meals/{}'.format(json_result['id']),
            headers=caterer_header
        )

        json_result = json.loads(res.get_data(as_text=True))
        self.assertEqual(res.status_code, 200)
        self.assertEqual(json_result['name'], 'Ugali')
        self.assertEqual(json_result['cost'], 200)

    def test_meal_can_be_updated(self):
        caterer_header, id = self.loginCaterer()
        res = self.client().post('/api/v1/meals',
                                 data=self.meal, headers=caterer_header)
        self.assertEqual(res.status_code, 201)
        res = self.client().put(
            '/api/v1/meals/1',
            data=json.dumps({
                'name': 'Sembe',
                'img_path': '#',
                'cost': 300.0
            }),
            headers=caterer_header
        )
        self.assertEqual(res.status_code, 200)
        res = self.client().get('/api/v1/meals/1', headers=caterer_header)

        json_result = json.loads(res.get_data(as_text=True))
        self.assertEqual(res.status_code, 200)
        self.assertEqual(json_result['name'], 'Sembe')
        self.assertEqual(json_result['cost'], 300)

    def test_meal_deletion(self):
        caterer_header, id = self.loginCaterer()
        res = self.client().post('/api/v1/meals',
                                 data=self.meal, headers=caterer_header)
        self.assertEqual(res.status_code, 201)
        res = self.client().delete('/api/v1/meals/1',
                                   headers=caterer_header)
        self.assertEqual(res.status_code, 204)

        res = self.client().get('/api/v1/meals/1', headers=caterer_header)
        self.assertEqual(res.status_code, 404)


if __name__ == '__main__':
    unittest.main()
