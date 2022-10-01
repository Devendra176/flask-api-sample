import os

from flask import Blueprint, current_app

from flask_restx import Api, Resource,Namespace, fields, abort

from flask_jwt_extended import current_user,jwt_required

# from flask_login import login_user, logout_user, login_required, current_user

from project.models import ImageUpload, User
from project.methods import s3Operations, rename_file
from project.custom_validation import allowed_file
from project.parsearguments import ParserArgument
from project.api_response.response_field import user_image_response

# Namespace define for User Image operations
user_images = Namespace(name='User images', path='/user/images',description='User Images operations.')

# For Marshaling 
mod = user_images.model( 'ImageUpload',{
    'user_id':fields.Integer(description='This is user ID'),
    'created_at':fields.DateTime(description='Date Time of uploaded image'),
    'imagepath':fields.String(description="This is file Path")
})

@user_images.doc(description='This will Upload images in database and aws s3 bucket',security='apikey')
@user_images.response(404,'No user Found')
@user_images.response(400,'File required')
@user_images.response(422,'Choose allowed extention file')
@user_images.route('/<int:user_id>/uploadImage')
class ImageUploadView(Resource):
    @jwt_required()
    @user_images.marshal_with(mod,code=201,mask=False)
    @user_images.expect(ParserArgument().for_upload_file(),validate=True)
    def post(self,user_id):
        """
        This method will Upload images by logged-in User in database and s3 bucket.
        """

        if current_user.id != user_id:
            return abort(404,message='No user Found',error=404)

        user = User.objects(pk=user_id).first()
        file_upload = ParserArgument().for_upload_file()
        args = file_upload.parse_args()
        file_name = args['file'].filename
        if not user:
            return abort(404,message='No user Found',error=404)
        if not args['file']:
            return abort(400,message='File required',error=400)
        if file_name == '':
            return abort(400,message='File required',error=400)

        if not allowed_file(file_name):
            abort(422, message='Choose allowed extention file',error=422)

        user_dir = os.path.join(current_app.config['UPLOAD_FOLDER'],str(user_id))
        if not os.path.exists(user_dir):
            os.makedirs(user_dir)
        new_name = rename_file(file_name)
        file_path_for_aws = os.path.join(user_dir, new_name)
        args['file'].save(os.path.join(user_dir, new_name))
        data = ImageUpload(user=user_id,imagepath=file_path_for_aws)
        data.save()
        s3_op = s3Operations()
        s3_op.send_file_s3(file_path_for_aws,os.path.join(str(user_id),new_name))
        return data.to_json(),201
        


# For marshaling Nested response
user_fields = user_images.model('data',user_image_response)
response = user_images.model('GetImageData',{
    'user_id':fields.Integer(),
    'imagedata':fields.List(fields.Nested(user_fields))
})

@user_images.response(404,'Not Found')
@user_images.doc(description='This will Get Uploaded images.',security='apikey')
@user_images.route('/<int:user_id>')
class GetUploadedImagesView(Resource):
    @jwt_required()
    @user_images.marshal_with(response,code=200,mask=False)
    def get(self,user_id):
        """
        This method will get all the Images uploaded in s3 by Logged-in User.
        """
        if current_user.id != user_id:
            abort(404,message='No Record Found')
        data = ImageUpload.objects(user=user_id).all()
        if data.count()==0:
            abort(404,message='No Record Found')
        response  = [{'created_at':item.created_at,'imagepath':item.imagepath} for count,item in enumerate(data,1)]
        return {'user_id':user_id,'imagedata':response},200