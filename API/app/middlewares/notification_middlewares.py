"""Middlewares for the notification resource"""


from app.validators import Valid
from app.models import Notification
from .common_middlewares import (
    single_for_user, many_for_user, post_delete, check_exists
)
from .auth_middlewares import caterer_auth, default_auth


pre_notification={
    'POST': [caterer_auth, Valid.post_notification],
    'GET_SINGLE': [default_auth, check_exists(Notification),
                   single_for_user(Notification)],
    'GET_MANY': [default_auth, many_for_user],
    'PUT_SINGLE': [caterer_auth, check_exists(Notification),
                   Valid.put_notification],
    'DELETE_SINGLE': [default_auth],
    'DELETE_MANY': [default_auth],
}

post_notification={
    'DELETE_SINGLE': [post_delete],
    'DELETE_MANY': [post_delete]
}
