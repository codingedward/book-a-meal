"""Contains the application's database models"""


from app import db
from passlib.hash import bcrypt


class UserType:
    """Users roles"""
    CATERER = 1
    CUSTOMER = 2


class MenuType:
    """Menu categories"""
    BREAKFAST = 1
    LUNCH = 2
    SUPPER = 3

class BaseModel:
    """This will handle saving and deletion of models"""

    def save(self):
        """Save current model"""
        db.session.add(self)
        db.session.commit()

    def delete(self):
        """Delete current model"""
        db.session.delete(self)
        db.session.commit()


class Blacklist(db.Model, BaseModel):
    """Holds JWT tokens revoked through user signing out"""

    __tablename__ = 'blacklist'

    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(500))
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    def __init__(self, token):
        """Initialiaze the blacklist record"""
        self.token = token


class User(db.Model, BaseModel):
    """This will have application's users details"""

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255))
    email = db.Column(db.String(1024), unique=True)
    password_hash = db.Column(db.String(300))
    role = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(
        db.DateTime,
        default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp()
    )

    def __init__(self, username, email, password, role = UserType.CUSTOMER):
        """Initialize the user"""
        self.email = email
        self.role = role
        self.username = username
        self.password_hash = bcrypt.encrypt(password)

    def validate_password(self, password):
        """Checks the password is correct against the password hash"""
        return bcrypt.verify(password, self.password_hash)

    def is_caterer(self):
        """Checks if current user is a caterer"""
        return self.role == UserType.CATERER


class Menu(db.Model, BaseModel):
    """Holds the menus"""

    __tablename__ = 'menus'

    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.Integer)
    day = db.Column(db.Date, default=db.func.current_timestamp())
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(
        db.DateTime,
        default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp()
    )

    def __init__(self, category):
        """Initialize the menu"""
        self.category = category


class MenuItem(db.Model, BaseModel):
    """Holds the menu item of the application"""

    __tablename__ = 'menu_items'

    id = db.Column(db.Integer, primary_key=True)
    menu_id = db.Column(db.Integer, db.ForeignKey('menus.id'))
    meal_id = db.Column(db.Integer, db.ForeignKey('meals.id'))
    quantity = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(
        db.DateTime,
        default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp()
    )

    # relationship with the menu
    menu = db.relationship(
        'Menu',
        backref=db.backref('menu_items', lazy='dynamic')
    )

    # relationship with the meal
    meal = db.relationship(
        'Meal',
        backref=db.backref('menu_items', lazy='dynamic')
    )

    def __init__(self, menu_id, meal_id, quantity=1):
        """Initialize a meal item"""
        self.menu_id = menu_id
        self.meal_id = meal_id
        self.quantity = quantity


class Meal(db.Model, BaseModel):
    """Holds a meal in the application"""

    __tablename__ = 'meals'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True)
    cost = db.Column(db.Float(2))
    img_path = db.Column(db.String(2048))
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(
        db.DateTime,
        default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp()
    )

    def __init__(self, name, cost, img_path):
        """Initialize a meal"""
        self.name = name
        self.cost = cost
        self.img_path = img_path


class Order(db.Model, BaseModel):
    """Holds an order of the application"""

    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer, default=1)
    menu_item_id = db.Column(
        db.Integer,
        db.ForeignKey('menu_items.id', ondelete='CASCADE')
    )
    user_id = db.Column(db.Integer,
                        db.ForeignKey('users.id', ondelete='CASCADE'))
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(
        db.DateTime,
        default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp()
    )

    # relationship with the menu items
    menu_item = db.relationship(
        'MenuItem',
        backref=db.backref("orders", lazy="dynamic")
    )

    def __init__(self, menu_item_id, user_id, quantity):
        """Initialize the order"""
        self.user_id = user_id
        self.quantity = quantity
        self.menu_item_id = menu_item_id


class Notification(db.Model, BaseModel):
    """Notification model"""

    __tablename__ = 'notifications'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    message = db.Column(db.String(1024))
    user_id = db.Column(db.Integer,
                        db.ForeignKey('users.id', ondelete='CASCADE'))
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(
        db.DateTime,
        default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp()
    )

    # relationship with a user
    user = db.relationship(
        'User',
        backref=db.backref("notifications", lazy="dynamic")
    )

    def __init__(self, title, message, user_id):
        """Initialize the notification"""
        self.title = title
        self.message = message
        self.user_id = user_id
