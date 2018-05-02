import os
import json
import unittest
from app import create_app, db
from app.models import User, UserType, Meal, MenuType, Menu, MenuItem

class BaseTest(unittest.TestCase):
    """ 
    This will hold the basic methods required by other tests, for 
    example authentication in order to test guarded endpoints
    """
    def loginCustomer(self):
        with self.app.app_context():
            user_email = 'customer@mail.com'
            user = User.query.filter_by(email=user_email).first()
            if not user:
                user = User(username='John', email='customer@mail.com',
                            password='secret')
                user.save()

            # log this user in for the auth token
            res = self.client().post(
                '/api/v1/auth/login',
                data=json.dumps({
                    'email': 'customer@mail.com',
                    'password': 'secret'
                }),
                headers={'Content-Type' : 'application/json'}
            )

            json_result = json.loads(res.get_data(as_text=True))
            return  {
                'Accept': 'application/json',
                'Content-Type' : 'application/json',
                'Authorization': 'Bearer {}'.format(json_result['access_token'])
            }, user.id

    def loginCaterer(self):
        with self.app.app_context():
            # create a temporary caterer
            user = User(username="John", email="caterer@mail.com", 
                        password="secret", role=UserType.CATERER)
            user.save()

            # log this caterer in and obtain headers for the auth token
            res = self.client().post(
                '/api/v1/auth/login',
                data=json.dumps({
                    'email': 'caterer@mail.com',
                    'password': 'secret'
                }),
                headers={'Content-Type' : 'application/json'}
            )

            json_result = json.loads(res.get_data(as_text=True))
            return {
                'Content-Type' : 'application/json',
                'Authorization': 'Bearer {}'.format(json_result['access_token'])
            }, user.id

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()


class AuthenticationTestCase(unittest.TestCase):
    """ This will test authentication endpoints"""

    def setUp(self):
        self.app = create_app(config_name='testing')
        self.client = self.app.test_client
        self.user = json.dumps({
            'username': 'John',
            'email': 'john@doe.com', 
            'password': 'secret'
        })
        self.headers = {'Content-Type' : 'application/json'} 

        with self.app.app_context():
            db.create_all()

    def test_user_can_signup(self):
        res = self.client().post('/api/v1/auth/signup',
                                 data=self.user, headers=self.headers)
        self.assertEqual(res.status_code, 201)

    def test_user_can_login(self):
        res = self.client().post('/api/v1/auth/signup',
                                 data=self.user, headers=self.headers)
        res = self.client().post(
            '/api/v1/auth/login', 
            data=self.user,
            headers=self.headers
        )
        self.assertEqual(res.status_code, 200)
        self.assertIn(b'token', res.data)

    def test_user_can_logout(self):
        res = self.client().post('/api/v1/auth/signup',
                                 data=self.user, headers=self.headers)
        res = self.client().post(
            '/api/v1/auth/login', 
            data=self.user,
            headers=self.headers
        )
        self.assertEqual(res.status_code, 200)
        self.assertIn(b'token', res.data)

        json_result = json.loads(res.get_data(as_text=True))
        res = self.client().delete(
            '/api/v1/auth/logout',
            headers={
                'Accept': 'application/json',
                'Content-Type' : 'application/json',
                'Authorization': 'Bearer {}'.format(json_result['access_token'])
            }
        )
        self.assertEqual(res.status_code, 200)

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()


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
        caterer_header, id = self.loginCaterer()
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


class MenuTestCase(BaseTest):
    """ This will test menu resource endpoints"""

    def setUp(self):
        self.app = create_app(config_name='testing')
        self.client = self.app.test_client
        self.headers = {'Content-Type' : 'application/json'} 
        self.menu = json.dumps({
            'category': MenuType.BREAKFAST
        })

        with self.app.app_context():
            db.create_all()

    def test_menu_creation(self):
        caterer_header, _ = self.loginCaterer()
        res = self.client().post(
            '/api/v1/menus',
            data=self.menu,
            headers=caterer_header
        )
        json_result = json.loads(res.get_data(as_text=True))
        self.assertEqual(res.status_code, 201)
        self.assertEqual(json_result['category'], MenuType.BREAKFAST)

    def test_can_get_all_menus(self):
        caterer_header, _ = self.loginCaterer()
        res = self.client().post(
            '/api/v1/menus',
            data=self.menu,
            headers=caterer_header
        )
        self.assertEqual(res.status_code, 201)

        customer_header, _ = self.loginCustomer()
        res = self.client().get('/api/v1/menus', headers=customer_header)

        json_result = json.loads(res.get_data(as_text=True))
        self.assertEqual(res.status_code, 200)
        self.assertEqual(json_result['num_results'], 1)
        self.assertIn(b'objects', res.data)

    def test_can_get_menu_by_id(self):
        caterer_header, _ = self.loginCaterer()
        res = self.client().post(
            '/api/v1/menus',
            data=self.menu,
            headers=caterer_header
        )
        self.assertEqual(res.status_code, 201)

        customer_header, _ = self.loginCustomer()
        json_result = json.loads(res.get_data(as_text=True))
        res = self.client().get(
            '/api/v1/menus/{}'.format(json_result['id']),
            headers=customer_header
        )

        json_result = json.loads(res.get_data(as_text=True))
        self.assertEqual(res.status_code, 200)
        self.assertEqual(json_result['category'], MenuType.BREAKFAST)

    def test_menu_can_be_updated(self):
        caterer_header, _ = self.loginCaterer()
        res = self.client().post(
            '/api/v1/menus',
            data=self.menu,
            headers=caterer_header
        )
        self.assertEqual(res.status_code, 201)

        res = self.client().put(
            '/api/v1/menus/1',
            data=json.dumps({
                'category': MenuType.SUPPER
            }),
            headers=caterer_header
        )
        self.assertEqual(res.status_code, 200)

        customer_header, _ = self.loginCustomer()
        res = self.client().get('/api/v1/menus/1', headers=customer_header)
        json_result = json.loads(res.get_data(as_text=True))

        self.assertEqual(res.status_code, 200)
        self.assertEqual(json_result['category'], MenuType.SUPPER)

    def test_menu_deletion(self):
        caterer_header, _ = self.loginCaterer()
        res = self.client().post(
            '/api/v1/menus',
            data=self.menu,
            headers=caterer_header
        )
        self.assertEqual(res.status_code, 201)
        res = self.client().delete('/api/v1/menus/1',
                                   headers=caterer_header)
        self.assertEqual(res.status_code, 204)
        customer_header, _ = self.loginCustomer()
        res = self.client().get('/api/v1/menus/1', headers=customer_header)
        self.assertEqual(res.status_code, 404)


class NotificationTestCase(BaseTest):
    """ This will test notification resource endpoints"""

    def setUp(self):
        self.app = create_app(config_name='testing')
        self.client = self.app.test_client
        self.headers = {'Content-Type' : 'application/json'} 
        self.notification = {
            'title': 'Hello there',
            'message': 'I have a message for you',
        }

        with self.app.app_context():
            db.create_all()

    def test_notification_creation(self):
        caterer_header, _ = self.loginCaterer()
        customer_header, id = self.loginCustomer()
        self.notification['user_id'] = id
        res = self.client().post('/api/v1/notifications',
                                 data=json.dumps(self.notification), 
                                 headers=caterer_header)
        json_result = json.loads(res.get_data(as_text=True))

        self.assertEqual(res.status_code, 201)
        self.assertEqual(json_result['title'], 'Hello there')

    def test_can_get_all_notifications(self):
        caterer_header, _ = self.loginCaterer()
        customer_header, id = self.loginCustomer()
        self.notification['user_id'] = id
        res = self.client().post('/api/v1/notifications',
                                 data=json.dumps(self.notification), 
                                 headers=caterer_header)
        self.assertEqual(res.status_code, 201)

        customer_header, _ = self.loginCustomer()
        res = self.client().get('/api/v1/notifications', headers=customer_header)

        json_result = json.loads(res.get_data(as_text=True))
        self.assertEqual(res.status_code, 200)
        self.assertEqual(json_result['num_results'], 1)
        self.assertIn(b'objects', res.data)

    def test_can_get_notification_by_id(self):
        caterer_header, _ = self.loginCaterer()
        customer_header, id = self.loginCustomer()
        self.notification['user_id'] = id
        res = self.client().post('/api/v1/notifications',
                                 data=json.dumps(self.notification), 
                                 headers=caterer_header)
        self.assertEqual(res.status_code, 201)

        json_result = json.loads(res.get_data(as_text=True))
        res = self.client().get(
            '/api/v1/notifications/{}'.format(json_result['id']),
            headers=customer_header
        )

        json_result = json.loads(res.get_data(as_text=True))
        self.assertEqual(res.status_code, 200)
        self.assertEqual(json_result['title'], 'Hello there')

    def test_notification_can_be_updated(self):
        caterer_header, _ = self.loginCaterer()
        customer_header, id = self.loginCustomer()
        self.notification['user_id'] = id
        res = self.client().post('/api/v1/notifications',
                                 data=json.dumps(self.notification), 
                                 headers=caterer_header)
        self.assertEqual(res.status_code, 201)

        self.notification['title'] = 'Hi'
        res = self.client().put(
            '/api/v1/notifications/1',
            data=json.dumps(self.notification), 
            headers=caterer_header
        )
        self.assertEqual(res.status_code, 200)
        res = self.client().get('/api/v1/notifications/1', 
                                headers=customer_header)
        json_result = json.loads(res.get_data(as_text=True))

        self.assertEqual(res.status_code, 200)
        self.assertEqual(json_result['title'], 'Hi')

    def test_notification_deletion(self):
        caterer_header, _ = self.loginCaterer()
        customer_header, id = self.loginCustomer()
        self.notification['user_id'] = id
        res = self.client().post('/api/v1/notifications',
                                 data=json.dumps(self.notification), 
                                 headers=caterer_header)
        self.assertEqual(res.status_code, 201)

        customer_header, _ = self.loginCustomer()
        res = self.client().delete('/api/v1/notifications/1',
                                   headers=customer_header)
        self.assertEqual(res.status_code, 204)

        res = self.client().get('/api/v1/notifications/1',
                                headers=caterer_header)
        self.assertEqual(res.status_code, 404)


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
                'user_id': id
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
                'user_id': id
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
                'user_id': id
            }),
            headers=caterer_header
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
        self.assertEqual(res.status_code, 204)
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
                meal_name = 'Ugali'
                meal = Meal.query.filter_by(name=meal_name).first()
                if not meal:
                    meal = Meal(name=meal_name, img_path='#', cost=200)
                    meal.save()
                menu_item = MenuItem(menu_id=menu.id, meal_id=meal.id)
                menu_item.save()
            return menu_item.id


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
        self.assertEqual(res.status_code, 204)

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
