import os
from datetime import timedelta


class Config(object):
    DEBUG = False
    SECRET = os.getenv('SECRET')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    PROPAGATE_ERRORS = True
    PROPAGATE_EXCEPTIONS = True
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=48)
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ['access']

    MAIL_USE_TLS = True
    MAIL_DEBUG = False
    MAIL_PORT = os.getenv('MAIL_PORT')
    MAIL_SERVER = os.getenv('MAIL_SERVER')
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')


class ProductionConfig(Config):
    DEBUG = False
    TESTING = False
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=2)


class DevConfig(Config):
    "Config for development"
    DEBUG = True
    #MAIL_SUPPRESS_SEND = True


class TestingConfig(Config):
    DEBUG = True
    TESTING = True
    MAIL_SUPPRESS_SEND = True
    SQLALCHEMY_DATABASE_URI = os.getenv('TEST_DATABASE_URL')


app_config = {
    'dev': DevConfig,
    'testing': TestingConfig,
    'production': ProductionConfig
}
