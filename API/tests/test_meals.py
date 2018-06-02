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

    def test_meal_creation_without_img(self):
        caterer_header, _ = self.loginCaterer()
        res = self.client().post(
            '/api/v1/meals',
            data=json.dumps({
                'name': 'Beef',
                'cost': 200.0
            }),
            headers=caterer_header
        )
        json_result = json.loads(res.get_data(as_text=True))
        self.assertEqual(res.status_code, 201)
        self.assertEqual(json_result['name'], 'Beef')
        self.assertEqual(json_result['cost'], 200)

    def test_cannot_create_meal_without_unique_name(self):
        caterer_header, _ = self.loginCaterer()
        res = self.client().post(
            '/api/v1/meals',
            data=json.dumps({
                'name': 'Beef',
                'cost': 200.0
            }),
            headers=caterer_header
        )
        json_result = json.loads(res.get_data(as_text=True))
        self.assertEqual(res.status_code, 201)
        self.assertEqual(json_result['name'], 'Beef')
        self.assertEqual(json_result['cost'], 200)

        res = self.client().post(
            '/api/v1/meals',
            data=json.dumps({
                'name': 'Beef',
                'cost': 200.0
            }),
            headers=caterer_header
        )
        self.assertEqual(res.status_code, 400)
        self.assertIn(b'Meal name must be unique', res.data)

    def test_cannot_create_meal_without_name(self):
        caterer_header, _ = self.loginCaterer()
        res = self.client().post(
            '/api/v1/meals',
            data=json.dumps({
                'img_path': '#',
                'cost': 200.0
            }),
            headers=caterer_header
        )
        self.assertEqual(res.status_code, 400)
        self.assertIn(b'Name is required', res.data)

    def test_cannot_create_meal_with_empty_name(self):
        caterer_header, _ = self.loginCaterer()
        res = self.client().post(
            '/api/v1/meals',
            data=json.dumps({
                'img_path': '#',
                'name': '',
                'cost': 200.0
            }),
            headers=caterer_header
        )
        self.assertEqual(res.status_code, 400)
        self.assertIn(b'Invalid meal name', res.data)

    def test_cannot_create_meal_without_cost(self):
        caterer_header, _ = self.loginCaterer()
        res = self.client().post(
            '/api/v1/meals',
            data=json.dumps({
                'name': 'Ugali',
                'img_path': '#',
            }),
            headers=caterer_header
        )
        self.assertEqual(res.status_code, 400)

    def test_cannot_create_meal_without_numeric_cost(self):
        caterer_header, _ = self.loginCaterer()
        res = self.client().post(
            '/api/v1/meals',
            data=json.dumps({
                'name': 'Ugali',
                'img_path': '#',
                'cost': 'hi'
            }),
            headers=caterer_header
        )
        self.assertEqual(res.status_code, 400)

    def test_cannot_create_meal_with_same_name(self):
        caterer_header, _ = self.loginCaterer()
        res = self.client().post('/api/v1/meals',
                                 data=self.meal, headers=caterer_header)
        json_result = json.loads(res.get_data(as_text=True))
        self.assertEqual(res.status_code, 201)
        self.assertEqual(json_result['name'], 'Ugali')
        self.assertEqual(json_result['cost'], 200)

        res = self.client().post('/api/v1/meals',
                                 data=self.meal, headers=caterer_header)
        self.assertEqual(res.status_code, 400)

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

    def test_cannnot_get_meal_with_wrong_index(self):
        caterer_header, id = self.loginCaterer()
        res = self.client().get(
            '/api/v1/meals/x',
            headers=caterer_header
        )

        self.assertEqual(res.status_code, 400)
        self.assertIn(b'Id must be an integer', res.data)

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

    def test_meal_cannot_be_updated_without_unique_name(self):
        caterer_header, id = self.loginCaterer()
        res = self.client().post('/api/v1/meals',
                                 data=self.meal, headers=caterer_header)
        self.assertEqual(res.status_code, 201)
        res = self.client().post(
            '/api/v1/meals',
            data=json.dumps({
                'name': 'Sembe',
                'img_path': '#',
                'cost': 300.0
            }),
            headers=caterer_header
        )
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
        self.assertEqual(res.status_code, 400)
        self.assertIn(b'Meal name must be unique', res.data)

    def test_cannot_update_meal_with_no_details(self):
        caterer_header, id = self.loginCaterer()
        res = self.client().post('/api/v1/meals',
                                 data=self.meal, headers=caterer_header)
        self.assertEqual(res.status_code, 201)
        res = self.client().put(
            '/api/v1/meals/1',
            data=json.dumps({}),
            headers=caterer_header
        )
        self.assertEqual(res.status_code, 400)

    def test_cannot_update_meal_with_empty_name(self):
        caterer_header, id = self.loginCaterer()
        res = self.client().post('/api/v1/meals',
                                 data=self.meal, headers=caterer_header)
        self.assertEqual(res.status_code, 201)
        res = self.client().put(
            '/api/v1/meals/1',
            data=json.dumps({
                'name': '',
                'img_path': '#',
                'cost': 300.0
            }),
            headers=caterer_header
        )
        self.assertEqual(res.status_code, 400)

    def test_cannot_update_meal_with_non_numeric_cost(self):
        caterer_header, id = self.loginCaterer()
        res = self.client().post('/api/v1/meals',
                                 data=self.meal, headers=caterer_header)
        self.assertEqual(res.status_code, 201)
        res = self.client().put(
            '/api/v1/meals/1',
            data=json.dumps({
                'name': 'sembe',
                'img_path': '#',
                'cost': 'hi'
            }),
            headers=caterer_header
        )
        self.assertEqual(res.status_code, 400)

    def test_meal_deletion(self):
        caterer_header, id = self.loginCaterer()
        res = self.client().post('/api/v1/meals',
                                 data=self.meal, headers=caterer_header)
        self.assertEqual(res.status_code, 201)
        res = self.client().delete('/api/v1/meals/1',
                                   headers=caterer_header)
        self.assertEqual(res.status_code, 200)
        res = self.client().get('/api/v1/meals/1', headers=caterer_header)
        self.assertEqual(res.status_code, 404)

    def test_cannot_delete_nonexistent_meal(self):
        caterer_header, id = self.loginCaterer()
        res = self.client().post('/api/v1/meals',
                                 data=self.meal, headers=caterer_header)
        self.assertEqual(res.status_code, 201)
        res = self.client().delete('/api/v1/meals/100',
                                   headers=caterer_header)
        self.assertEqual(res.status_code, 404)
        self.assertIn(b'Not found', res.data)


if __name__ == '__main__':
    unittest.main()
