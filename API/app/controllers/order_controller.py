"""Order resource controller"""


from app.models import Order
from app.middlewares.order_middlewares import pre_order, post_order


def create_api(manager, url_prefix=''):
    """Creates the order API endpoints"""
    manager.create_api(
        Order,
        methods=['GET', 'POST', 'DELETE', 'PUT'],
        url_prefix=url_prefix,
        preprocessors=pre_order,
        postprocessors=post_order
    )
