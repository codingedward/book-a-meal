from app.models import Notification
from app.middlewares.notification_middlewares import (
    pre_notification, post_notification
)


def create_api(manager, url_prefix=''):
    manager.create_api(
        Notification,
        methods=['GET', 'POST', 'DELETE', 'PUT'],
        url_prefix=url_prefix,
        preprocessors=pre_notification,
        postprocessors=post_notification
    )

