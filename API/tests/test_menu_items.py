import os
import json
import unittest
from app import create_app, db
from app.models import Meal, MenuType, Menu
from tests.base import BaseTest

class MenuItemTestCase(BaseTest):
    """ This will test menu item resource endpoints"""

    def setUp(self):
        self.app = create_app(config_name='testing')
        self.client = self.app.test_client
        self.headers = {'Content-Type' : 'application/json'} 

        with self.app.app_context():
            db.create_all()
            self.menu_item = json.dumps({
                'meal_id': self.createMeal(),
                'menu_id': self.createMenu(),
            })

    def test_menu_item_creation(self):
        caterer_header, _ = self.loginCaterer()
        res = self.client().post(
            '/api/v1/menu_items',
            data=self.menu_item,
            headers=caterer_header
        )
        json_result = json.loads(res.get_data(as_text=True))
        self.assertEqual(res.status_code, 201)
        self.assertEqual(json_result['menu_id'], 1)

    def test_can_get_all_menu_items(self):
        caterer_header, _ = self.loginCaterer()
        res = self.client().post(
            '/api/v1/menu_items',
            data=self.menu_item,
            headers=caterer_header
        )
        self.assertEqual(res.status_code, 201)

        customer_header, _ = self.loginCustomer()
        res = self.client().get('/api/v1/menu_items', headers=customer_header)

        json_result = json.loads(res.get_data(as_text=True))
        self.assertEqual(res.status_code, 200)
        self.assertEqual(json_result['num_results'], 1)
        self.assertIn(b'objects', res.data)

    def test_can_get_menu_item_by_id(self):
        caterer_header, _ = self.loginCaterer()
        res = self.client().post(
            '/api/v1/menu_items',
            data=self.menu_item,
            headers=caterer_header
        )
        self.assertEqual(res.status_code, 201)

        customer_header, _ = self.loginCustomer()
        json_result = json.loads(res.get_data(as_text=True))
        res = self.client().get(
            '/api/v1/menu_items/{}'.format(json_result['id']),
            headers=customer_header
        )

        json_result = json.loads(res.get_data(as_text=True))
        self.assertEqual(res.status_code, 200)
        self.assertEqual(json_result['meal_id'], 1)

    def test_menu_item_can_be_updated(self):
        caterer_header, _ = self.loginCaterer()
        res = self.client().post(
            '/api/v1/menu_items',
            data=self.menu_item,
            headers=caterer_header
        )
        self.assertEqual(res.status_code, 201)

        res = self.client().put(
            '/api/v1/menu_items/1',
            data=json.dumps({
                'meal_id': self.createMeal(id=2),
                'menu_id': self.createMenu(),
            }),
            headers=caterer_header
        )
        self.assertEqual(res.status_code, 200)
        customer_header, _ = self.loginCustomer()
        res = self.client().get('/api/v1/menu_items/1', 
                                headers=customer_header)
        json_result = json.loads(res.get_data(as_text=True))

        self.assertEqual(res.status_code, 200)
        self.assertEqual(json_result['meal_id'], 2)

    def test_menu_item_deletion(self):
        caterer_header, _ = self.loginCaterer()
        res = self.client().post(
            '/api/v1/menu_items',
            data=self.menu_item,
            headers=caterer_header
        )
        self.assertEqual(res.status_code, 201)
        res = self.client().delete('/api/v1/menu_items/1',
                                   headers=caterer_header)
        self.assertEqual(res.status_code, 200)

        customer_header, _ = self.loginCustomer()
        res = self.client().get('/api/v1/menu_items/1', 
                                headers=customer_header)
        self.assertEqual(res.status_code, 404)

    def createMenu(self, id = 1):
        with self.app.app_context():
            menu = Menu.query.get(id)
            if not menu:
                menu = Menu(category=MenuType.BREAKFAST)
                menu.save()
            return menu.id

    def createMeal(self, id = 1):
        with self.app.app_context():
            meal = Meal.query.get(id)
            if not meal:
                meal = Meal(name='meal_{}'.format(id), img_path='#', cost=200)
                meal.save()
            return meal.id


if __name__ == '__main__':
    unittest.main()
