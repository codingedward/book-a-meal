"""Meal resource controller"""


from app.models import Meal
from app.middlewares.meal_middlewares import pre_meal, post_meal


def create_api(manager, url_prefix=''):
    """Creates the meals api endpoints"""
    manager.create_api(
        Meal,
        methods=['GET', 'POST', 'DELETE', 'PUT'],
        url_prefix=url_prefix,
        preprocessors=pre_meal,
        postprocessors=post_meal
    )
