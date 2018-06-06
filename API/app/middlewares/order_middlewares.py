"""Order resource middlewares"""


from app.validators import Valid
from app.models import Order, MenuItem
from .common_middlewares import (
    single_for_user, many_for_user, post_delete, check_exists
)
from .auth_middlewares import caterer_auth, default_auth


def update_quantity(result=None, **kwargs):
    """When an order is made, we need to decrement the number
    of available menu items"""
    if result:
        menu_item = MenuItem.query.get(result['menu_item_id'])
        menu_item.quantity -= result['quantity']
        menu_item.save()

pre_order={
    'POST': [default_auth, Valid.post_order],
    'GET_SINGLE': [default_auth, check_exists(Order), single_for_user(Order)],
    'GET_MANY': [default_auth, many_for_user],
    'PUT_SINGLE': [default_auth, check_exists(Order), Valid.put_order],
    'DELETE_SINGLE': [default_auth],
    'DELETE_MANY': [caterer_auth],
}

post_order={
    'POST': [update_quantity],
    'PUT_SINGLE': [update_quantity],
    'DELETE_SINGLE': [post_delete],
    'DELETE_MANY': [post_delete]
}
