"""Middlewares for menu items"""


from app.validators import Valid
from app.models import MenuItem
from .common_middlewares import post_delete, check_exists
from .auth_middlewares import caterer_auth, default_auth

pre_menu_item={
    'POST': [caterer_auth, Valid.post_menu_item],
    'GET_SINGLE': [default_auth, check_exists(MenuItem)],
    'GET_MANY': [default_auth],
    'PUT_SINGLE': [caterer_auth, check_exists(MenuItem),
                   Valid.put_menu_item],
    'DELETE_SINGLE': [caterer_auth],
    'DELETE_MANY': [caterer_auth],
}

post_menu_item={
    'DELETE_SINGLE': [post_delete],
    'DELETE_MANY': [post_delete]
}
