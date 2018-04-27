import os
from datetime import timedelta


class Config(object):
    DEBUG = False
    CSRF_ENABLED = True    # prevent cross site request forgery
    SECRET = os.getenv('SECRET')


class ProductionConfig(Config):
    DEBUG = False
    TESTING = False


class DevConfig(Config):
    "Config for development"
    DEBUG = True


class TestingConfig(Config):
    DEBUG = True
    TESTING = True

app_config = {
    'dev': DevConfig,
    'testing': TestingConfig,
    'production': ProductionConfig
}
