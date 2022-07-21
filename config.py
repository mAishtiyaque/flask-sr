import os
basedir = os.path.abspath(os.path.dirname(__file__))
port = int(os.environ.get('PORT', 33507))

class Config(object):
    DEBUG = False
    TESTING = False
    PORT =port
    SECRET_KEY = 'very_very-very_very Secret-Key'
    SQLALCHEMY_DATABASE_URI="postgres://uootornqvinrxu:12c268b0a499dad621a5ded9c9214a1bc9a120b1a7988a0a6a496cf51002f48c@ec2-44-206-197-71.compute-1.amazonaws.com:5432/dfsoqjfus90nu"

class ProductionConfig(Config):
    DEBUG = False

class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True

class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "postgresql://postgres:zamzam@localhost/Ahmad"
    PORT =5000

class TestingConfig(Config):
    TESTING = True

