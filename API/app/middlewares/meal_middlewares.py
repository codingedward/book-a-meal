from app.validators import Valid
from app.models import Meal
from .common_middlewares import post_delete, check_exists
from .auth_middlewares import caterer_auth, default_auth

pre_meal={
    'POST': [caterer_auth, Valid.post_meal],
    'GET_MANY': [default_auth],
    'GET_SINGLE': [default_auth, check_exists(Meal)],
    'PUT_SINGLE': [caterer_auth, check_exists(Meal), Valid.put_meal],
    'DELETE_SINGLE': [caterer_auth],
    'DELETE_MANY': [caterer_auth],
}

post_meal={
    'DELETE_SINGLE': [post_delete],
    'DELETE_MANY': [post_delete],
}
