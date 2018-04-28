import os
from datetime import timedelta


class Config(object):
    DEBUG = False
    CSRF_ENABLED = True    # prevent cross site request forgery
    SECRET = os.getenv('SECRET')
    JWT_AUTH_URL_RULE = '/api/v1/auth/login'
    JWT_AUTH_USERNAME_KEY = 'email'
    JWT_EXPIRATION_DELTA = timedelta(seconds=3600)
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')


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
