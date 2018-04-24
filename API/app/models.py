import enum
from app import db
from passlib.hash import bcrypt


class User(db.Model):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255))
    email = db.Column(db.String(1024), unique=True)
    password_hash = db.Column(db.String(300))
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(
        db.DateTime, 
        default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp()
    )
    orders = db.relationship('Order')
    notifications = db.relationship('Notification')

    def __init__(self, username, email, password):
        self.email = email
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
        return bcrypt.verify(password, self.password)


class Meal(db.Model):

    __tablename__ = 'meals'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True)
    cost = db.Column(db.Float(2))
    img_path = db.Column(dp.String(1024))
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(
        db.DateTime, 
        default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp()
    )
    menus = db.relationship('Menu')

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


class MealType(enum.Enum):
    BREAKFAST = 1
    LUNCH = 2
    SUPPER = 3


class Menu(db.Model):

    __tablename__ = 'menus'

    id = db.Column(db.Integer, primary_key=True)
    meal_id = db.Column(db.Integer, db.ForeignKey('meals.id'))
    category = db.Column(db.Enum(MealType))
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(
        db.DateTime, 
        default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp()
    )
    orders = db.relationship('Order')

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
    menu_id = db.Column(db.Integer, db.ForeignKey('menus.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(
        db.DateTime, 
        default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp()
    )

    def __init__(self, menu_id, user_id):
        self.meal_id = meal_id
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
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(
        db.DateTime, 
        default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp()
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

