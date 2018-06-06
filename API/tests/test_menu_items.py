"""Test the menu item resource endpoints"""


import json
from app import create_app, db
from app.models import Meal, MenuType, Menu
from tests.base import BaseTest

class MenuItemTestCase(BaseTest):
    """ This will test menu item resource endpoints"""

    def setUp(self):
        """Create an application"""
        self.app = create_app(config_name='testing')
        self.client = self.app.test_client
        self.headers = {'Content-Type' : 'application/json'}

        with self.app.app_context():
            db.create_all()
            self.menu_item = json.dumps({
                'meal_id': self.createMeal(),
                'menu_id': self.createMenu(),
                'quantity': 4,
            })

    def test_menu_item_creation(self):
        """Test can create a menu item"""
        caterer_header, _ = self.loginCaterer()
        res = self.client().post(
            '/api/v1/menu_items',
            data=self.menu_item,
            headers=caterer_header
        )
        json_result = json.loads(res.get_data(as_text=True))
        self.assertEqual(res.status_code, 201)
        self.assertEqual(json_result['menu_id'], 1)

    def test_cannot_create_same_menu_item(self):
        """Test cannot create same menu item"""
        caterer_header, _ = self.loginCaterer()
        res = self.client().post(
            '/api/v1/menu_items',
            data=self.menu_item,
            headers=caterer_header
        )
        json_result = json.loads(res.get_data(as_text=True))
        self.assertEqual(res.status_code, 201)
        self.assertEqual(json_result['menu_id'], 1)
        res = self.client().post(
            '/api/v1/menu_items',
            data=self.menu_item,
            headers=caterer_header
        )
        self.assertEqual(res.status_code, 400)
        self.assertIn(b'This menu item already exists', res.data)

    def test_cannot_create_menu_item_without_meal_id(self):
        """Test cannot create a menu item without a meal id"""
        caterer_header, _ = self.loginCaterer()
        res = self.client().post(
            '/api/v1/menu_items',
            data=json.dumps({
                'menu_id': self.createMenu(),
            }),
            headers=caterer_header
        )
        self.assertEqual(res.status_code, 400)

    def test_cannot_create_menu_item_without_menu_id(self):
        """Test cannot create a menu item without a menu id"""
        caterer_header, _ = self.loginCaterer()
        res = self.client().post(
            '/api/v1/menu_items',
            data=json.dumps({
                'meal_id': self.createMeal(),
            }),
            headers=caterer_header
        )
        self.assertEqual(res.status_code, 400)

    def test_cannot_create_menu_item_with_wrong_meal_id(self):
        """Test cannot create a menu item with a wrong meal id"""
        caterer_header, _ = self.loginCaterer()
        res = self.client().post(
            '/api/v1/menu_items',
            data=json.dumps({
                'meal_id': 40,
                'quantity': 4,
                'menu_id': self.createMenu(),
            }),
            headers=caterer_header
        )
        self.assertEqual(res.status_code, 400)

    def test_cannot_create_menu_item_without_quantity(self):
        """Test cannot create menu item without quantity"""
        caterer_header, _ = self.loginCaterer()
        res = self.client().post(
            '/api/v1/menu_items',
            data=json.dumps({
                'meal_id': self.createMeal(),
                'menu_id': self.createMenu(),
            }),
            headers=caterer_header
        )
        self.assertEqual(res.status_code, 400)
        self.assertIn(b'Quantity is required', res.data)

    def test_cannot_create_menu_item_without_quantity(self):
        """Test cannot create menu item without quantity"""
        caterer_header, _ = self.loginCaterer()
        res = self.client().post(
            '/api/v1/menu_items',
            data=json.dumps({
                'quantity': 'x',
                'meal_id': self.createMeal(),
                'menu_id': self.createMenu(),
            }),
            headers=caterer_header
        )
        self.assertEqual(res.status_code, 400)
        self.assertIn(b'Quantity is required and must', res.data)

    def test_cannot_create_menu_item_with_wrong_menu_id(self):
        """Test cannot create a menu item with wrong menu id"""
        caterer_header, _ = self.loginCaterer()
        res = self.client().post(
            '/api/v1/menu_items',
            data=json.dumps({
                'menu_id': 50,
                'quantity': 4,
                'meal_id': self.createMeal(),
            }),
            headers=caterer_header
        )
        self.assertEqual(res.status_code, 400)

    def test_cannot_create_menu_item_with_negative_quantity(self):
        """Test cannot create a menu item with negative quantity"""
        caterer_header, _ = self.loginCaterer()
        res = self.client().post(
            '/api/v1/menu_items',
            data=json.dumps({
                'quantity': -1,
                'menu_id': self.createMenu(),
                'meal_id': self.createMeal(),
            }),
            headers=caterer_header
        )
        self.assertEqual(res.status_code, 400)

    def test_cannot_create_existing_menu_item(self):
        """Test cannot create an existing menu item"""
        caterer_header, _ = self.loginCaterer()
        res = self.client().post(
            '/api/v1/menu_items',
            data=self.menu_item,
            headers=caterer_header
        )
        self.assertEqual(res.status_code, 201)

        res = self.client().post(
            '/api/v1/menu_items',
            data=self.menu_item,
            headers=caterer_header
        )
        self.assertEqual(res.status_code, 400)

    def test_can_get_all_menu_items(self):
        """Test can get all menu items"""
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
        """Test can get a menu item by id"""
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
        """Test menu item can be updated"""
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
                'meal_id': self.createMeal(meal_id=2),
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

    def test_cannot_update_menu_item_with_negative_quantity(self):
        """Test cannot update a menu item with negative quantity"""
        caterer_header, _ = self.loginCaterer()
        res = self.client().post(
            '/api/v1/menu_items',
            data=json.dumps({
                'meal_id': self.createMeal(meal_id=3),
                'menu_id': self.createMenu(),
                'quantity': 10
            }),
            headers=caterer_header
        )
        self.assertEqual(res.status_code, 201)
        res = self.client().put(
            '/api/v1/menu_items/1',
            data=json.dumps({
                'quantity': -1,
            }),
            headers=caterer_header
        )
        self.assertEqual(res.status_code, 400)
        self.assertIn(b'Quantity must be positive', res.data)


    def test_cannot_update_menu_item_without_being_unique(self):
        """Test cannot update a menu item without being unique"""
        caterer_header, _ = self.loginCaterer()
        res = self.client().post(
            '/api/v1/menu_items',
            data=self.menu_item,
            headers=caterer_header
        )
        menu_id = self.createMenu()
        meal_id = self.createMeal(meal_id=2)
        self.assertEqual(res.status_code, 201)
        res = self.client().post(
            '/api/v1/menu_items',
            data=json.dumps({
                'meal_id': meal_id,
                'menu_id': menu_id,
                'quantity': 4,
            }),
            headers=caterer_header
        )
        self.assertEqual(res.status_code, 201)
        res = self.client().put(
            '/api/v1/menu_items/1',
            data=json.dumps({
                'meal_id': meal_id,
                'menu_id': menu_id
            }),
            headers=caterer_header
        )
        self.assertEqual(res.status_code, 400)
        self.assertIn(b'This menu item already exists', res.data)

    def test_cannot_update_menu_item_with_non_existing_menu_id(self):
        """Test cannot update a menu item with non-existing menu id"""
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
                'meal_id': self.createMeal(meal_id=2),
                'menu_id': 48
            }),
            headers=caterer_header
        )
        self.assertEqual(res.status_code, 400)

    def test_cannot_update_menu_item_with_non_existing_meal_id(self):
        """Test cannot update a menu item with non-existing meal id"""
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
                'meal_id': 50,
                'menu_id': self.createMenu(),
            }),
            headers=caterer_header
        )
        self.assertEqual(res.status_code, 400)

    def test_menu_item_deletion(self):
        """Test menu item deletion"""
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

    def createMenu(self, menu_id=1):
        """Create a temporary menu for creating a menu item"""
        with self.app.app_context():
            menu = Menu.query.get(menu_id)
            if not menu:
                menu = Menu(category=MenuType.BREAKFAST)
                menu.save()
            return menu.id

    def createMeal(self, meal_id=1):
        """Create a temporary meal for creating a menu item"""
        with self.app.app_context():
            meal = Meal.query.get(meal_id)
            if not meal:
                meal = Meal(name='meal_{}'.format(meal_id), img_path='#', cost=200)
                meal.save()
            return meal.id


if __name__ == '__main__':
    unittest.main()
