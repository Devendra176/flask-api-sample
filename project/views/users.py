import os
from datetime import datetime

from flask import current_app,request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash

# from flask_login import login_user, logout_user, login_required, current_user
from flask_restx import Resource,Namespace,fields, abort
from flask_jwt_extended import create_access_token,current_user,jwt_required,get_jwt

from project.models import User, ProfileImages
from project.jwt_operations import jwt_redis_blocklist

from project.parsearguments import ParserArgument
from api_response.resource_field import registration_resource,update_userdeatils_resource
from project.methods import rename_file
from project.custom_validation import ( validate_email,
                                        validate_password,
                                        validate_username,
                                        validate_fname_lname,
                                        validate_country,
                                        allowed_file,
                                        )
from api_response.response_field import (
    registered_user_response,
    profile_data_response,
    )

# Namespace Defined For user Operation library
user_api = Namespace(name='User', path='/user', description='User Operations.')

resource_fields = user_api.model('Registration',registration_resource)
response_user_profile = user_api.model('ProfilePic',profile_data_response)
response_user = user_api.model('RegisteredUser',registered_user_response)
update_user_deatils = user_api.model('UpdateUserData',update_userdeatils_resource)

@user_api.doc(description='This will Create User.')
@user_api.response(400, 'Validation error')
@user_api.response(409,'Confict')
@user_api.route('/register')
class UserCreateView(Resource):

    @user_api.expect(resource_fields, validate=True)
    @user_api.marshal_with(response_user,code=201,mask=False)
    def post(self):
        """
        This method is used to register the users.
        """
        args = request.json
        email_checked = validate_email(args['email'])
        check_username = validate_username(args['username'])
        check_fname_lname = validate_fname_lname(args['first_name'],args['last_name'])
        check_country = validate_country(args['country'])
        password_checked = validate_password(args['password'],args['confirm_password'])
        if email_checked and password_checked and check_username and check_fname_lname and check_country:
            user = User(
                email=args['email'],
                password= generate_password_hash(args['password'],method='sha256'),
                username=args['username'],
                first_name=args['first_name'],
                last_name=args['last_name'],
                country=args['country'],
                )
            user.save()
            ProfileImages(user=user.id).save()
            return user.to_json(),201



response_login = user_api.model('LoginUserData',{
    'message':fields.String(),
    'status':fields.Integer(),
    'user_data':fields.Nested(response_user),
    'profile_pic_data':fields.Nested(response_user_profile),
    'access_token':fields.String(),
})

@user_api.route('/login')
@user_api.expect(ParserArgument().for_login_argument(),validate=True)
@user_api.doc(description='This will Create Access Token.',security='apikey')
class UserLoginView(Resource):
    @user_api.marshal_with(response_login,mask=False,code=200)
    def post(self):
        """
        This is Login method and it logged in users and create a access Token.
        """
        login_parser = ParserArgument().for_login_argument()
        args = login_parser.parse_args()
        email = args['email']
        password = args['password']
        user = User.objects(email=email).first()
        if not user:
            abort(404,'Email Not Exist.')
        if not check_password_hash(user.password, password):
            abort(401,'password is incorrect')
        access_token = create_access_token(identity=user)
        profileimages = ProfileImages.objects(user=user.id).first()
        user_profile_pic_data = {
            'default':profileimages.default,
            'active_profile_pic':profileimages.profilepic if not profileimages.default else profileimages.defaultpic,
            'created_at':profileimages.created_at,
            'updated_at':profileimages.updated_at,
            }
        return {
            'message':'succesfully login',
            'status':200,
            'user_data':user.to_json(),
            'profile_pic_data':user_profile_pic_data,
            'access_token':access_token,
            },200


@user_api.route('/logout')
@user_api.doc(description='This will Revoke the token.',security='apikey')
class UserLogoutView(Resource):

    @jwt_required()
    def get(self):
        """
        This method is logout method,
        it will Revoke the access Token.
        """
        user_id = current_user.id
        user = User.objects(id=user_id).first()
        jti = get_jwt()["jti"]
        jwt_redis_blocklist.set(jti, "", ex=current_app.config['JWT_ACCESS_TOKEN_EXPIRES'])
        if not user:
            abort(404,'No user found')
        last_login = datetime.now()
        user.update(last_login=last_login)
        return jsonify(message='Successfully logged out.')


response_user_data =  user_api.model('UserData',{
    'user_data':fields.Nested(response_user),
    'profile_pic_data':fields.Nested(response_user_profile),
})
@user_api.doc(security='apikey')
@user_api.route('/<int:user_id>')
class UserProfileView(Resource):

    @jwt_required()
    @user_api.doc(description='This will Get user data.')
    @user_api.marshal_with(response_user_data,mask=False,code=200)
    def get(self,user_id):
        """
        This method will get logged in user data with active profile picture.
        """
        if current_user.id != user_id:
            abort(404,'User Not Found')
        userdata = User.objects(id=user_id).first()
        profile_image_data = ProfileImages.objects(user=user_id).first()
        response = {
            'user_data':userdata.to_json(),
            'profile_pic_data':
                {
                    'default':profile_image_data.default,
                    'active_profile_pic': profile_image_data.defaultpic \
                            if profile_image_data.default else profile_image_data.profilepic,
                    'created_at': profile_image_data.created_at,
                    'updated_at':profile_image_data.updated_at,
                }
            }
        return response,200
    
    @jwt_required()
    @user_api.doc(description='This will Delete User.')
    @user_api.expect(ParserArgument().for_delete_account_arg(),validate=True)
    def delete(self,user_id):
        """
        This will Delete User.
        """
        reqparse = ParserArgument().for_delete_account_arg()
        args = reqparse.parse_args()
        password = args['password']
        if current_user.id != user_id:
            abort(404,'No user found with given user_id')
        if not check_password_hash(current_user.password, password):
            abort(401,'Password does not matched')
        User.objects(id=user_id).delete()
        return jsonify(msg='User deleted successfully')

@user_api.doc(description='This will update user password.',security='apikey')
@user_api.route('/<int:user_id>/password-change')
class UserPasswordChangeView(Resource):

    @jwt_required()
    @user_api.expect(ParserArgument().for_put_argument(),validate=True)
    def put(self,user_id):
        """
        This method is used to update the user password.
        this method requires a existing user password to change password.
        """
        reqparse = ParserArgument().for_put_argument()
        args = reqparse.parse_args()
        password = args['password']
        new_password = args['new_password']
        confirm_new_password=args['confirm_new_password']

        if current_user.id != user_id:
            abort(404,'No user found with given user_id')

        if not check_password_hash(current_user.password, password):
            abort(401,'password is incorrect')

        if validate_password(new_password,confirm_new_password):
            user = User.objects(id=current_user.id).first()
            password = generate_password_hash(args['new_password'],method='sha256')
            user.update(password=password,updated_at=datetime.now())
        return jsonify(msg='password changed successfully')


response_user_profile_data = user_api.model('ProfileImageData', {
    'user_id':fields.Integer(description='This is user user_id.'),
    'created_at':fields.DateTime(),
    'updated_at':fields.DateTime(),
    'default':fields.Boolean(),
    'defaultpic':fields.String(),
    'profilepic':fields.String(),
})

@user_api.doc(description='This will change user profile pic.',security='apikey')
@user_api.route('/<int:user_id>/change-profile-image')
class UserProfileUpdateView(Resource):

    @jwt_required()
    @user_api.expect(ParserArgument().for_profile_pic_arg(),validate=True)
    @user_api.marshal_with(response_user_profile_data,mask=False)
    def put(self,user_id):
        """
        This method will update user profile picture.
        """
        if current_user.id != user_id or not User.objects(id=user_id).first():
            abort(404,'User does not exists')
        reqparse = ParserArgument().for_profile_pic_arg()
        args = reqparse.parse_args()
        file = args['img']
        if not file:
            abort(400,message='File required',error=400)

        if file.filename == "":
            abort(400,message='File required',error=400)

        if not allowed_file(file.filename):
            abort(422, message='Choose allowed extention file',error=422)

        user_dir = os.path.join(current_app.config['PROFILE_UPLOAD_FOLDER'],str(user_id))

        if not os.path.exists(user_dir):
            os.makedirs(user_dir)
        filename = rename_file(file.filename)
        file.save(os.path.join(user_dir,filename))
        image = ProfileImages.objects(user = user_id).first()
        image.update(default=False,
                    profilepic=os.path.join(user_dir,filename),
                    updated_at=datetime.now())
        image = ProfileImages.objects(user = user_id).first()
        return image.to_json()

@user_api.doc(description='This will change user profile pic.',security='apikey')
@user_api.route('/<int:user_id>/make-default-profilepic')
class MakeDefaultProfilePic(Resource):

    @jwt_required()
    @user_api.marshal_with(response_user_profile_data,mask=False)
    def post(self,user_id):
        """
        This method will make default profile picture wich is icon-jpg.
        """
        if current_user.id !=user_id and not ProfileImages.objects(user=user_id).first():
            abort(404,'No user found')
        image = ProfileImages.objects(user=user_id)
        image.update(default=True,updated_at=datetime.now())
        image = ProfileImages.objects(user=user_id).first()
        return image.to_json()

@user_api.route('/<int:user_id>/update-profile-data')
@user_api.doc(description='This will update user profile deatils',security='apikey')
class UpdateProfileData(Resource):
    @jwt_required()
    @user_api.expect(update_user_deatils,validate=True)
    @user_api.marshal_with(update_user_deatils,mask=False)
    def put(self,user_id):
        user = User.objects(id=user_id).first()
        args = request.json
        if current_user.id !=user_id or not user:
            abort(404,'No user found')
        if not args:
            abort(400,'Json Formate allowed')

        check_username = validate_username(args['username'])
        check_fname_lname = validate_fname_lname(args['first_name'],args['last_name'])
        check_country = validate_country(args['country'])

        if check_username and check_fname_lname and check_country:
            user.update(username=args['username'],
                        first_name=args['first_name'],
                        last_name=args['last_name'],
                        country=args['country'],
                        )
            user = User.objects(id=user_id).first()
            return {
                'username':user.username,
                'first_name':user.first_name,
                'last_name':user.last_name,
                'country':user.country,
                }
