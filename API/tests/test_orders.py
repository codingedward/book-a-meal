import json
import unittest
from datetime import datetime, timedelta
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
        customer_header, user_id = self.loginCustomer()
        res = self.client().post(
            '/api/v1/orders',
            data=json.dumps({
                'menu_item_id': self.createMenuItem(),
            }),
            headers=customer_header
        )
        json_result = json.loads(res.get_data(as_text=True))

        self.assertEqual(res.status_code, 201)
        self.assertEqual(json_result['user_id'], user_id)

    def test_cannot_create_order_without_menu_item_id(self):
        caterer_header, _ = self.loginCaterer()
        _, user_id = self.loginCustomer()
        res = self.client().post(
            '/api/v1/orders',
            data=json.dumps({}),
            headers=customer_header
        )
        self.assertEqual(res.status_code, 400)

    def test_cannot_create_order_with_non_existing_menu_item_id(self):
        caterer_header, _ = self.loginCaterer()
        customer_header, user_id = self.loginCustomer()
        res = self.client().post(
            '/api/v1/orders',
            data=json.dumps({'menu_item_id': 40}),
            headers=customer_header
        )
        self.assertEqual(res.status_code, 400)


    def test_can_get_all_orders(self):
        caterer_header, _ = self.loginCaterer()
        customer_header, user_id = self.loginCustomer()
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
        customer_header, user_id = self.loginCustomer()
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
            headers=customer_header
        )

        json_result = json.loads(res.get_data(as_text=True))
        self.assertEqual(res.status_code, 200)
        self.assertEqual(json_result['user_id'], user_id)

    def test_cannot_get_other_users_order(self):
        caterer_header, _ = self.loginCaterer()
        customer_header, user_id = self.loginCustomer()
        res = self.client().post(
            '/api/v1/orders',
            data=json.dumps({
                'menu_item_id': self.createMenuItem(),
            }),
            headers=customer_header
        )
        json_result = json.loads(res.get_data(as_text=True))
        self.assertEqual(res.status_code, 201)

        customer_header, user_id = self.loginCustomer('hacker@mail.com')
        res = self.client().get(
            '/api/v1/orders/{}'.format(json_result['id']),
            headers=customer_header
        )

        self.assertEqual(res.status_code, 401)
        self.assertIn(b'Unauthorized access', res.data)

    def test_cannot_create_order_with_expired_menu(self):
        caterer_header, _ = self.loginCaterer()
        customer_header, user_id = self.loginCustomer()
        res = self.client().post(
            '/api/v1/orders',
            data=json.dumps({
                'menu_item_id': self.createMenuItem(yesterdays=True),
                'user_id': user_id
            }),
            headers=customer_header
        )
        self.assertEqual(res.status_code, 400)
        self.assertIn(b'This menu is expired', res.data)

    def test_order_can_be_updated(self):
        caterer_header, _ = self.loginCaterer()
        customer_header, user_id = self.loginCustomer()
        res = self.client().post(
            '/api/v1/orders',
            data=json.dumps({
                'menu_item_id': self.createMenuItem(),
                'user_id': user_id
            }),
            headers=customer_header
        )
        self.assertEqual(res.status_code, 201)
        res = self.client().put(
            '/api/v1/orders/1',
            data=json.dumps({
                'menu_item_id': self.createMenuItem(menu_item_id=2),
                'user_id': user_id
            }),
            headers=customer_header
        )
        self.assertEqual(res.status_code, 200)

        customer_header, _ = self.loginCustomer()
        res = self.client().get('/api/v1/orders/1', headers=customer_header)
        json_result = json.loads(res.get_data(as_text=True))

        self.assertEqual(res.status_code, 200)
        self.assertEqual(json_result['menu_item_id'], 2)

    def test_cannot_update_order_with_wrong_menu_id(self):
        caterer_header, _ = self.loginCaterer()
        customer_header, user_id = self.loginCustomer()
        res = self.client().post(
            '/api/v1/orders',
            data=json.dumps({
                'menu_item_id': self.createMenuItem(),
                'user_id': user_id
            }),
            headers=customer_header
        )
        self.assertEqual(res.status_code, 201)
        res = self.client().put(
            '/api/v1/orders/1',
            data=json.dumps({
                'menu_item_id': 100,
                'user_id': user_id
            }),
            headers=customer_header
        )
        self.assertEqual(res.status_code, 400)
        self.assertIn(b'No menu item found for that', res.data)

    def test_cannot_update_order_with_expired_menu(self):
        caterer_header, _ = self.loginCaterer()
        customer_header, user_id = self.loginCustomer()
        res = self.client().post(
            '/api/v1/orders',
            data=json.dumps({
                'menu_item_id': self.createMenuItem(),
                'user_id': user_id
            }),
            headers=customer_header
        )
        self.assertEqual(res.status_code, 201)
        res = self.client().put(
            '/api/v1/orders/1',
            data=json.dumps({
                'menu_item_id': self.createMenuItem(yesterdays=True),
                'user_id': user_id
            }),
            headers=customer_header
        )
        self.assertEqual(res.status_code, 400)
        self.assertIn(b'This menu is expired', res.data)

    def test_cannot_edit_another_users_order(self):
        caterer_header, _ = self.loginCaterer()
        customer_header, user_id = self.loginCustomer()
        res = self.client().post(
            '/api/v1/orders',
            data=json.dumps({
                'menu_item_id': self.createMenuItem(),
                'user_id': user_id
            }),
            headers=customer_header
        )
        customer_header, user_id = self.loginCustomer(email='hacker@mail.com')
        self.assertEqual(res.status_code, 201)
        res = self.client().put(
            '/api/v1/orders/1',
            data=json.dumps({
                'menu_item_id': self.createMenuItem(menu_item_id=2),
                'user_id': user_id
            }),
            headers=customer_header
        )
        self.assertEqual(res.status_code, 401)
        self.assertIn(b'This user cannot edit this order', res.data)

    def test_order_deletion(self):
        caterer_header, _ = self.loginCaterer()
        customer_header, user_id = self.loginCustomer()
        res = self.client().post(
            '/api/v1/orders',
            data=json.dumps({
                'menu_item_id': self.createMenuItem(),
                'user_id': user_id
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

    def createMenuItem(self, menu_item_id=1, yesterdays=False):
        with self.app.app_context():
            menu_item = MenuItem.query.get(menu_item_id)
            if not menu_item or yesterdays:
                menu = Menu.query.get(1)
                if not menu or yesterdays:
                    menu = Menu(category=MenuType.BREAKFAST)
                    if yesterdays:
                        menu.day = datetime.utcnow().date() - timedelta(1)
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
