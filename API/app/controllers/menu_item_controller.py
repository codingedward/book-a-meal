from app.models import MenuItem
from app.middlewares.menu_item_middlewares import (
    pre_menu_item, post_menu_item
)


def create_api(manager, url_prefix=''):
    manager.create_api(
        MenuItem,
        methods=['GET', 'POST', 'DELETE', 'PUT'],
        url_prefix=url_prefix,
        preprocessors=pre_menu_item,
        postprocessors=post_menu_item
    )
