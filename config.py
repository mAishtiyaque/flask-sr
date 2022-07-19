import os
basedir = os.path.abspath(os.path.dirname(__file__))
port = int(os.environ.get('PORT', 33507))

class Config(object):
    DEBUG = False
    TESTING = False
    PORT =port
    SECRET_KEY = 'very_very-very_very Secret-Key'
    #SQLALCHEMY_DATABASE_URI="postgresql://caanrfieefnvmu:684b136d7f4108ae5a0d44014b97e270c22be042b22f56c70e7967079bf7e346@ec2-54-152-28-9.compute-1.amazonaws.com:5432/d9abrq28rmoilb"
    SQLALCHEMY_DATABASE_URI = "postgresql://postgres:zamzam@localhost/Ahmad"

class ProductionConfig(Config):
    DEBUG = False

class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True

class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    PORT =5000

class TestingConfig(Config):
    TESTING = True

