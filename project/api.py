from flask import Blueprint

from flask_restx import Api

from project.views.users import user_api as user
from project.views.user_images_upload import user_images
from project.views.extra_api import public_api as public_api
from project.test import api as view_api

# Creating blueprint for Flask API
user_api  = Blueprint('api', __name__)

# user_blueprint = Blueprint('user', __name__)

# user_images_blueprint = Blueprint('user-images', __name__)

# blueprint2=Blueprint('view', __name__)

# define Authorization

authorizations = {
    'apikey': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization',
        'description':"Add 'Bearer' as Prefix "
    }
}

api = Api(user_api,
    title='TEST API',
    version='1.0.0',
    authorizations=authorizations,
    description='API',
    doc='/', 
)

# adding Namespacees with API this one id for user operations
api.add_namespace(user)

#adding Namespacees with API this one id for user image  upload operations
api.add_namespace(user_images)

api.add_namespace(public_api)

#adding Namespacees with API this one id for Extra 
api.add_namespace(view_api)

