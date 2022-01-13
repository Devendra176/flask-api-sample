import sys
sys.path.insert(0, "/home/cis/Desktop/aws/project")
import re

from flask import Flask
from flask_cors import CORS
from flask_mongoengine import MongoEngine

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
EMAIL_REGEX = re.compile(r'\S+@\S+\.\S+')

db = MongoEngine()

def create_app():
    app = Flask(__name__)
    CORS(app)
    if app.config["ENV"] == "production":
        app.config.from_object("config.ProductionConfig")
    else:
        app.config.from_object("config.DevelopmentConfig")
    with app.app_context():


        db = MongoEngine()
        db.init_app(app)

        from .api import user_api
        app.register_blueprint(user_api)

        from .jwt_operations import jwt
        jwt.init_app(app)
    
        return app