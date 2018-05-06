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


class ProductionConfig(Config):
    DEBUG = False
    TESTING = False
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=2)


class DevConfig(Config):
    "Config for development"
    DEBUG = True


class TestingConfig(Config):
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.getenv('TEST_DATABASE_URL')


app_config = {
    'dev': DevConfig,
    'testing': TestingConfig,
    'production': ProductionConfig
}
