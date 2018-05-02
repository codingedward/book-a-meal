import enum
from app import db
from datetime import date
from passlib.hash import bcrypt
from sqlalchemy import cast, DATE


class UserType:
    CATERER = 1
    CUSTOMER = 2


class MenuType:
    BREAKFAST = 1
    LUNCH = 2
    SUPPER = 3


class Blacklist(db.Model):

    __tablename__ = 'blacklist'

    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(500))
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    def __init__(self, token):
        self.token = token

    def save(self):
        db.session.add(self)
        db.session.commit()


class User(db.Model):

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
        self.email = email
        self.role = role
        self.username = username
        self.password_hash = bcrypt.encrypt(password)

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all(self):
        return User.query.all()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def validate_password(self, password):
        return bcrypt.verify(password, self.password_hash)

    def is_caterer(self):
        return self.role == UserType.CATERER


class Menu(db.Model):

    __tablename__ = 'menus'

    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(
        db.DateTime,
        default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp()
    )

    def __init__(self, category):
        self.category = category

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all(self):
        return Menu.query.all()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class MenuItem(db.Model):

    __tablename__ = 'menu_items'

    id = db.Column(db.Integer, primary_key=True)
    menu_id = db.Column(db.Integer, db.ForeignKey('menus.id'))
    meal_id = db.Column(db.Integer, db.ForeignKey('meals.id'))
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(
        db.DateTime,
        default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp()
    )

    menu = db.relationship(
        'Menu',
        backref=db.backref('menu_items', lazy='dynamic')
    )

    meal = db.relationship(
        'Meal',
        backref=db.backref('menu_items', lazy='dynamic')
    )

    def __init__(self, menu_id, meal_id):
        self.menu_id = menu_id
        self.meal_id = meal_id

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all(self):
        return MenuItem.query.all()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class Meal(db.Model):

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
        self.name = name
        self.cost = cost
        self.img_path = img_path

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all(self):
        return Meal.query.all()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class Order(db.Model):

    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)
    menu_item_id = db.Column(
        db.Integer,
        db.ForeignKey('menu_items.id',ondelete='CASCADE')
    )
    meal_id = db.Column(
        db.Integer, 
        db.ForeignKey('meals.id', ondelete='CASCADE')
    )
    user_id = db.Column(db.Integer,
                        db.ForeignKey('users.id', ondelete='CASCADE'))
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(
        db.DateTime,
        default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp()
    )

    menu_item = db.relationship(
        'MenuItem',
        backref=db.backref("orders", lazy="dynamic")
    )

    user = db.relationship(
        'User',
        backref=db.backref("orders", lazy="dynamic")
    )

    def __init__(self, menu_item_id, user_id):
        self.user_id = user_id
        self.menu_item_id = menu_item_id

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all(self):
        return Order.query.all()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class Notification(db.Model):

    __tablename__ = 'notifications'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    message = db.Column(db.String(1024))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'))
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(
        db.DateTime,
        default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp()
    )

    user = db.relationship(
        'User',
        backref=db.backref("notifications", lazy="dynamic")
    )

    def __init__(self, title, message, user_id):
        self.title = title
        self.message = message
        self.user_id = user_id

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all(self):
        return Notification.query.all()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
