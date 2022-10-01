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
        app.config.from_object("project.config.ProductionConfig")
    else:
        app.config.from_object("project.config.DevelopmentConfig")
    with app.app_context():


        db = MongoEngine()
        db.init_app(app)

        from project.api import user_api
        app.register_blueprint(user_api)

        from project.jwt_operations import jwt
        jwt.init_app(app)
    
        return app
