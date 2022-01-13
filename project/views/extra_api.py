from flask import jsonify
from flask_restx import Resource,Namespace,fields
from flask_restx.marshalling import marshal
from project.methods import s3Operations
from project.models import User, ProfileImages
from api_response.response_field import registered_user_response
public_api = Namespace(name='Public API', path='/public', description='Some Public API')


@public_api.route('/items-in-s3',)
class PublicAPIView(Resource):
    def get(self):
        """
        This is get all the images presnet in s3 bucket.
        """
        s3_op = s3Operations()
        items = s3_op.get_file_from_s3()
        return jsonify(items=items)

user_data = public_api.model('user_data',registered_user_response)

response_all_user = public_api.model('GetAllUsers',{
    'users':fields.List(fields.Nested(user_data))
})


@public_api.route('/get-all-users',)
class PublicGetUserAPIView(Resource):
    @public_api.marshal_with(response_all_user,code=200,mask=False)
    def get(self):
        """
        This will get all the users.
        """
        users = User.objects.all()
        imag = ProfileImages.objects(user__in=users)
        user = [{'user_id':user.id,
                'email':user.email,
                'username':user.username,
                'full_name':user.first_name+' '+user.last_name,
                'country':user.country,
                'created_at':user.created_at,
                'updated_at':user.updated_at,
                'last_login':user.last_login,
                } for user in users]
        data = {'users':user}
        return data,200

