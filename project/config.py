from datetime import timedelta
class Config(object):
    DEBUG = False
    TESTING = False
    SECRET_KEY = "B\xb2?.\xdf\x9f\xa7m\xf8\x8a%,\xf7\xc4\xfa\x91"
    JWT_SECRET_KEY="B\xb2?.\xdf\x9f\xa7m\xf8\x8a%,\xf7\xc4\xfa\x91"
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=15)
    UPLOAD_FOLDER = 'static/aws_pic'
    PROFILE_UPLOAD_FOLDER= 'static/profileImages'
    S3_BUCKET = "B\xb2?.\xdf\x9f\xa7m\xf8\x8a%,\xf7\xc4\xfa\x91"
    S3_KEY = "B\xb2?.\xdf\x9f\xa7m\xf8\x8a%,\xf7\xc4\xfa\x91"
    S3_SECRET = "B\xb2?.\xdf\x9f\xa7m\xf8\x8a%,\xf7\xc4\xfa\x91"
    MONGODB_SETTINGS = {
                        'db': 'production-db',
                        'host': 'admin',
                        'port': 'example'
                        }

class ProductionConfig(Config):
    pass

class DevelopmentConfig(Config):
    DEBUG = True
    SECRET_KEY = ""
    JWT_SECRET_KEY='3b41a593fb54ddd30e3da26b8fce441c'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=60)
    S3_BUCKET = ""
    S3_KEY = ""
    S3_SECRET = ""
    MONGODB_SETTINGS = {
                        'db': 'db_name',
                        'host': 'localhost',
                        'port': 27017
                        }

class TestingConfig(Config):
    
    TESTING = True
