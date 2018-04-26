import enum
from app import db
from passlib.hash import bcrypt


class UserType:
    CATERER = 1
    CUSTOMER = 2


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


class Meal(db.Model):

    __tablename__ = 'meals'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True)
    cost = db.Column(db.Float(2))
    img_path = db.Column(db.String(1024))
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


class MealType:
    BREAKFAST = 1
    LUNCH = 2
    SUPPER = 3


class Menu(db.Model):

    __tablename__ = 'menus'

    id = db.Column(db.Integer, primary_key=True)
    meal_id = db.Column(db.Integer, db.ForeignKey('meals.id', ondelete='CASCADE'))
    category = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(
        db.DateTime,
        default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp()
    )

    meal = db.relationship(
        'Meal',
        backref=db.backref("menus", lazy="dynamic")
    )

    def __init__(self, meal_id, category):
        self.meal_id = meal_id
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


class Order(db.Model):

    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)
    menu_id = db.Column(db.Integer, db.ForeignKey('menus.id', ondelete='CASCADE'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'))
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(
        db.DateTime,
        default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp()
    )

    menu = db.relationship(
        'Menu',
        backref=db.backref("orders", lazy="dynamic")
    )

    user = db.relationship(
        'User',
        backref=db.backref("orders", lazy="dynamic")
    )

    def __init__(self, menu_id, user_id):
        self.menu_id = menu_id
        self.user_id = user_id

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
