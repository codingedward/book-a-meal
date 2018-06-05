"""Menu resource controller"""


from app.models import Menu
from app.middlewares.menu_middlewares import pre_menu, post_menu


def create_api(manager, url_prefix=''):
    """Creates the menus api endpoints"""
    manager.create_api(
        Menu,
        methods=['GET', 'POST', 'DELETE', 'PUT'],
        url_prefix=url_prefix,
        collection_name='menu',
        preprocessors=pre_menu,
        postprocessors=post_menu
    )
