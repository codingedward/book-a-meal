from app.validators import Valid
from app.models import Order
from .common_middlewares import (
    single_for_user, many_for_user, post_delete, check_exists
)
from .auth_middlewares import caterer_auth, default_auth


pre_order={
    'POST': [default_auth, Valid.post_order],
    'GET_SINGLE': [default_auth, check_exists(Order), single_for_user(Order)],
    'GET_MANY': [default_auth, many_for_user],
    'PUT_SINGLE': [default_auth, check_exists(Order), Valid.put_order],
    'DELETE_SINGLE': [default_auth],
    'DELETE_MANY': [caterer_auth],
}

post_order={
    'DELETE_SINGLE': [post_delete],
    'DELETE_MANY': [post_delete]
}
