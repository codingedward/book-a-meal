from app.validators import Valid
from app.models import Menu
from .common_middlewares import (
    single_for_user, many_for_user, todays, post_delete, check_exists
)
from .auth_middlewares import caterer_auth, default_auth


pre_menu={
    'POST': [caterer_auth, Valid.post_menu],
    'GET_SINGLE': [default_auth, check_exists(Menu)],
    'GET_MANY': [default_auth, todays],
    'PUT_SINGLE': [caterer_auth, check_exists(Menu), Valid.put_menu],
    'DELETE_SINGLE': [caterer_auth],
    'DELETE_MANY': [caterer_auth],
}

post_menu={
    'DELETE_SINGLE': [post_delete],
    'DELETE_MANY': [post_delete]
}
