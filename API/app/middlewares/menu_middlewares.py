"""Middlewares for menu resource"""


from app.validators import Valid
from app.models import Menu
from .common_middlewares import (
    todays, post_delete, check_exists
)
from .auth_middlewares import caterer_auth, default_auth


def post_get_many(result=None, search_params=None, **kwargs):
    if result:
        result['menu'] = result['objects']
        del result['objects']

pre_menu={
    'POST': [caterer_auth, Valid.post_menu],
    'GET_SINGLE': [default_auth, check_exists(Menu)],
    'GET_MANY': [default_auth, todays, post_get_many],
    'PUT_SINGLE': [caterer_auth, check_exists(Menu), Valid.put_menu],
    'DELETE_SINGLE': [caterer_auth],
    'DELETE_MANY': [caterer_auth],
}

post_menu={
    'DELETE_SINGLE': [post_delete],
    'DELETE_MANY': [post_delete]
}
