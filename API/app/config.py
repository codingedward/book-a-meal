import os


class Config(object):
    DEBUG = False
    CSRF_ENABLED = True # prevent cross site request forgery
    SECRET = os.getenv('SECRET')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class ProductionConfig(Config):
    DEBUG = False
    TESTING = False

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
