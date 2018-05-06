import json
import unittest
from app import create_app, db
from tests.base import BaseTest
from app.models import MenuType, MenuItem, Menu, Meal


class OrderTestCase(BaseTest):
    """ This will test order resource endpoints """

    def setUp(self):
        self.app = create_app(config_name='testing')
        self.client = self.app.test_client
        self.headers = {'Content-Type' : 'application/json'} 

        with self.app.app_context():
            db.create_all()

    def test_order_creation(self):
        caterer_header, _ = self.loginCaterer()
        customer_header, id = self.loginCustomer()
        res = self.client().post(
            '/api/v1/orders',
            data=json.dumps({
                'menu_item_id': self.createMenuItem(),
            }),
            headers=customer_header
        )
        json_result = json.loads(res.get_data(as_text=True))

        self.assertEqual(res.status_code, 201)
        self.assertEqual(json_result['user_id'], id)

    def test_can_get_all_orders(self):
        caterer_header, _ = self.loginCaterer()
        customer_header, id = self.loginCustomer()
        res = self.client().post(
            '/api/v1/orders',
            data=json.dumps({
                'menu_item_id': self.createMenuItem(),
            }),
            headers=caterer_header
        )
        self.assertEqual(res.status_code, 201)
        res = self.client().get('/api/v1/orders', headers=caterer_header)
        json_result = json.loads(res.get_data(as_text=True))
        self.assertEqual(res.status_code, 200)
        self.assertEqual(json_result['num_results'], 1)
        self.assertIn(b'objects', res.data)

    def test_can_get_order_by_id(self):
        caterer_header, _ = self.loginCaterer()
        customer_header, id = self.loginCustomer()
        res = self.client().post(
            '/api/v1/orders',
            data=json.dumps({
                'menu_item_id': self.createMenuItem(),
            }),
            headers=customer_header
        )
        json_result = json.loads(res.get_data(as_text=True))
        self.assertEqual(res.status_code, 201)
        res = self.client().get(
            '/api/v1/orders/{}'.format(json_result['id']),
            headers=caterer_header
        )

        json_result = json.loads(res.get_data(as_text=True))
        self.assertEqual(res.status_code, 200)
        self.assertEqual(json_result['user_id'], id)

    def test_order_can_be_updated(self):
        caterer_header, _ = self.loginCaterer()
        customer_header, id = self.loginCustomer()
        res = self.client().post(
            '/api/v1/orders',
            data=json.dumps({
                'menu_item_id': self.createMenuItem(),
                'user_id': id
            }),
            headers=customer_header
        )
        self.assertEqual(res.status_code, 201)
        res = self.client().put(
            '/api/v1/orders/1',
            data=json.dumps({
                'menu_item_id': self.createMenuItem(id=2),
                'user_id': id
            }),
            headers=customer_header
        )
        self.assertEqual(res.status_code, 200)

        customer_header, _ = self.loginCustomer()
        res = self.client().get('/api/v1/orders/1', headers=customer_header)
        json_result = json.loads(res.get_data(as_text=True))

        self.assertEqual(res.status_code, 200)
        self.assertEqual(json_result['menu_item_id'], 2)

    def test_order_deletion(self):
        caterer_header, _ = self.loginCaterer()
        customer_header, id = self.loginCustomer()
        res = self.client().post(
            '/api/v1/orders',
            data=json.dumps({
                'menu_item_id': self.createMenuItem(),
                'user_id': id
            }),
            headers=caterer_header
        )
        self.assertEqual(res.status_code, 201)
        res = self.client().delete('/api/v1/orders/1',
                                   headers=customer_header)
        self.assertEqual(res.status_code, 200)
        customer_header, _ = self.loginCustomer()
        res = self.client().get('/api/v1/orders/1', headers=customer_header)
        self.assertEqual(res.status_code, 404)

    def createMenuItem(self, id = 1):
        with self.app.app_context():
            menu_item = MenuItem.query.get(id)
            if not menu_item:
                menu = Menu.query.get(1)
                if not menu:
                    menu = Menu(category=MenuType.BREAKFAST)
                    menu.save()
                meal_name = 'ugali'
                meal = Meal.query.filter_by(name=meal_name).first()
                if not meal:
                    meal = Meal(name=meal_name, img_path='#', cost=200)
                    meal.save()
                menu_item = MenuItem(menu_id=menu.id, meal_id=meal.id)
                menu_item.save()
            return menu_item.id


if __name__ == '__main__':
    unittest.main()
