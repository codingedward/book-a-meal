import os
import json
import unittest
from app import create_app, db
from app.models import User, UserType, Meal, MealType, Menu

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
                'Authorization': 'JWT {}'.format(json_result['access_token'])
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
                'Authorization': 'JWT {}'.format(json_result['access_token'])
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
        self.user = {'name': 'John', 'email': 'john@doe.com',
                     'password': 'secret'}

        with self.app.app_context():
            db.create_all()

    def test_user_can_signup(self):
        res = self.client().post('/api/v1/auth/signup', data=self.user)
        self.assertEqual(res.status_code, 201)

    def test_user_can_login(self):
        res = self.client().post('/api/v1/auth/login', data=self.user)
        self.assertEqual(res.status_code, 201)
        self.assertIn('token', res.data)

    def test_user_can_logout(self):
        res = self.client().post('/api/v1/auth/logout')
        self.assertEqual(res.status_code, 201)

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()


class MealTestCase(BaseTest):
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
        res = self.client().get('/api/v1/meals')

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
            '/api/v1/meals/{}'.format(json_result['id'])
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
        res = self.client().patch(
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

        res = self.client().get('/api/v1/meals/1')
        self.assertEqual(res.status_code, 404)


class MenuTestCase(BaseTest):
    """ This will test menu resource endpoints"""

    def setUp(self):
        self.app = create_app(config_name='testing')
        self.client = self.app.test_client
        self.headers = {'Content-Type' : 'application/json'} 

        with self.app.app_context():
            db.create_all()

    def test_menu_creation(self):
        caterer_header, _ = self.loginCaterer()
        res = self.client().post(
            '/api/v1/menus',
            data=json.dumps({
                'meal_id': self.createMeal(),
                'category': MealType.BREAKFAST
            }),
            headers=caterer_header
        )
        json_result = json.loads(res.get_data(as_text=True))

        self.assertEqual(res.status_code, 201)
        self.assertEqual(json_result['category'], MealType.BREAKFAST)

    def test_can_get_all_menus(self):
        caterer_header, _ = self.loginCaterer()
        res = self.client().post(
            '/api/v1/menus',
            data=json.dumps({
                'meal_id': self.createMeal(),
                'category': MealType.BREAKFAST
            }),
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
            data=json.dumps({
                'meal_id': self.createMeal(),
                'category': MealType.BREAKFAST
            }),
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
        self.assertEqual(json_result['category'], MealType.BREAKFAST)

    def test_menu_can_be_updated(self):
        caterer_header, _ = self.loginCaterer()
        res = self.client().post(
            '/api/v1/menus',
            data=json.dumps({
                'meal_id': self.createMeal(),
                'category': MealType.BREAKFAST
            }),
            headers=caterer_header
        )
        self.assertEqual(res.status_code, 201)

        res = self.client().patch(
            '/api/v1/menus/1',
            data=json.dumps({
                'meal_id': self.createMeal(),
                'category': MealType.SUPPER
            }),
            headers=caterer_header
        )
        self.assertEqual(res.status_code, 200)

        customer_header, _ = self.loginCustomer()
        res = self.client().get('/api/v1/menus/1', headers=customer_header)
        json_result = json.loads(res.get_data(as_text=True))

        self.assertEqual(res.status_code, 200)
        self.assertEqual(json_result['category'], MealType.SUPPER)

    def test_menu_deletion(self):
        caterer_header, _ = self.loginCaterer()
        res = self.client().post(
            '/api/v1/menus',
            data=json.dumps({
                'meal_id': self.createMeal(),
                'category': MealType.BREAKFAST
            }),
            headers=caterer_header
        )
        self.assertEqual(res.status_code, 201)

        res = self.client().delete('/api/v1/menus/1',
                                   headers=caterer_header)
        self.assertEqual(res.status_code, 204)

        customer_header, _ = self.loginCustomer()
        res = self.client().get('/api/v1/menus/1', headers=customer_header)
        self.assertEqual(res.status_code, 404)

    def createMeal(self):
        with self.app.app_context():
            meal_name = 'Ugali'
            meal = Meal.query.filter_by(name=meal_name).first()
            if not meal:
                meal = Meal(name='Ugali', img_path='#', cost=200)
                meal.save()
            return meal.id


class NotificationTestCase(unittest.TestCase):
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
        res = self.client().patch(
            '/api/v1/notifications/1',
            data=json.dumps(self.notification), 
            headers=caterer_header
        )
        self.assertEqual(res.status_code, 200)

        res = self.client().get('/api/v1/notifications/1', headers=customer_header)
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

        res = self.client().get('/api/v1/notifications/1')
        self.assertEqual(res.status_code, 404)

    def loginCustomer(self):
        with self.app.app_context():
            user_email = "customer@mail.com"
            user = User.query.filter_by(email=user_email).first()
            if not user:
                user = User(username="John", email="customer@mail.com",
                            password="secret")
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
                'Authorization': 'JWT {}'.format(json_result['access_token'])
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
                'Authorization': 'JWT {}'.format(json_result['access_token'])
            }, user.id

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()



class OrderTestCase(BaseTest):
    """ This will test order resource endpoints"""

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
                'menu_id': self.createMenu(),
                'user_id': id
            }),
            headers=caterer_header
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
                'menu_id': self.createMenu(),
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
                'menu_id': self.createMenu(),
                'user_id': id
            }),
            headers=caterer_header
        )
        self.assertEqual(res.status_code, 201)

        json_result = json.loads(res.get_data(as_text=True))
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
                'menu_id': self.createMenu(),
                'user_id': id
            }),
            headers=caterer_header
        )
        self.assertEqual(res.status_code, 201)

        res = self.client().patch(
            '/api/v1/orders/1',
            data=json.dumps({
                'menu_id': self.createMenu(),
                'user_id': id
            }),
            headers=caterer_header
        )
        self.assertEqual(res.status_code, 200)

        customer_header, _ = self.loginCustomer()
        res = self.client().get('/api/v1/orders/1', headers=customer_header)
        json_result = json.loads(res.get_data(as_text=True))

        self.assertEqual(res.status_code, 200)
        self.assertEqual(json_result['user_id'], id)

    def test_order_deletion(self):
        caterer_header, _ = self.loginCaterer()
        customer_header, id = self.loginCustomer()
        res = self.client().post(
            '/api/v1/orders',
            data=json.dumps({
                'menu_id': self.createMenu(),
                'user_id': id
            }),
            headers=caterer_header
        )
        self.assertEqual(res.status_code, 201)

        res = self.client().delete('/api/v1/orders/1',
                                   headers=caterer_header)
        self.assertEqual(res.status_code, 204)

        customer_header, _ = self.loginCustomer()
        res = self.client().get('/api/v1/orders/1', headers=customer_header)
        self.assertEqual(res.status_code, 404)

    def createMenu(self):
        with self.app.app_context():
            meal_name = 'Ugali'
            meal = Meal.query.filter_by(name=meal_name).first()
            if not meal:
                meal = Meal(name='Ugali', img_path='#', cost=200)
                meal.save()

            menu = Menu.query.filter_by(meal_id=meal.id).first()
            if not menu:
                menu = Menu(meal_id=meal.id, category=MealType.BREAKFAST)

            return menu.id


if __name__ == '__main__':
    unittest.main()
