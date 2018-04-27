import json
import unittest
from app import create_app 
from app.model import MealType
from app.api import bam



class MealTestCase(unittest.TestCase):
    """ This will test meal resource endpoints"""

    def setUp(self):
        self.app = create_app(config_name='testing')
        self.client = self.app.test_client
        self.meal = json.dumps({
            'name': 'Ugali',
            'img_path': '#',
            'cost': 200.0
        })
        self.headers = {'Content-Type' : 'application/json'} 
        
        user = {
            'username': 'John', 
            'email': 'john@doe.com', 
            'password': 'secretservice'
        }            
        bam.post_user(user)
        self.user = json.dumps(user)
        res = self.client().post('/api/v1/auth/login', 
                                 data=self.user,
                                 headers=self.headers)
        json_result = json.loads(res.get_data(as_text=True))
        self.headers = {'Content-Type' : 'application/json',
                        'Authorization': 'JWT {}'.format(json_result['access_token'])} 

    def test_meal_creation(self):
        res = self.client().post('/api/v1/meals',
                                 data=self.meal, headers=self.headers)

        json_result = json.loads(res.get_data(as_text=True))
        self.assertEqual(res.status_code, 201)
        self.assertEqual(json_result['name'], 'Ugali')
        self.assertEqual(json_result['cost'], 200)

    def test_can_get_all_meals(self):
        res = self.client().post('/api/v1/meals',
                                 data=self.meal, headers=self.headers)
        self.assertEqual(res.status_code, 201)
        res = self.client().get('/api/v1/meals')

        json_result = json.loads(res.get_data(as_text=True))
        self.assertEqual(res.status_code, 200)
        self.assertEqual(json_result['num_results'], 1)
        self.assertIn(b'objects', res.data)

    def test_can_get_meal_by_id(self):
        res = self.client().post('/api/v1/meals',
                                 data=self.meal, headers=self.headers)
        self.assertEqual(res.status_code, 201)
        json_result = json.loads(res.get_data(as_text=True))
        res = self.client().get(
            '/api/v1/meals/{}'.format(json_result['id'])
        )

        json_result = json.loads(res.get_data(as_text=True))
        self.assertEqual(res.status_code, 200)
        self.assertEqual(json_result['name'], 'Ugali')
        self.assertEqual(json_result['cost'], 200)

    def test_meal_can_be_updated(self):
        res = self.client().post('/api/v1/meals',
                                 data=self.meal, headers=self.headers)
        self.assertEqual(res.status_code, 201)
        res = self.client().patch(
            '/api/v1/meals/1',
            data=json.dumps({
                'name': 'Sembe',
                'img_path': '#',
                'cost': 300.0
            }),
            headers=self.headers
        )
        self.assertEqual(res.status_code, 200)
        res = self.client().get('/api/v1/meals/1', headers=self.headers)

        json_result = json.loads(res.get_data(as_text=True))
        self.assertEqual(res.status_code, 200)
        self.assertEqual(json_result['name'], 'Sembe')
        self.assertEqual(json_result['cost'], 300)

    def test_meal_deletion(self):
        res = self.client().post('/api/v1/meals',
                                 data=self.meal, headers=self.headers)
        self.assertEqual(res.status_code, 201)
        res = self.client().delete('/api/v1/meals/1',
                                   headers=self.headers)
        self.assertEqual(res.status_code, 204)

        res = self.client().get('/api/v1/meals/1')
        self.assertEqual(res.status_code, 404)

    def tearDown(self):
        with self.app.app_context():
            bam.clear()



if __name__ == '__main__':
    unittest.main()
