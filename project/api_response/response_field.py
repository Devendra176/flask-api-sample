from flask_restx import fields

#for register user response
registered_user_response = {
    'user_id':fields.Integer(description='This is user user_id.',attribute='user_id'),
    'email': fields.String(description='This is Email.',attribute='email'),
    'username':fields.String(attribute='username'),
    'full_name':fields.String(attribute='full_name'),
    'country':fields.String(attribute='country'),
    'created_at':fields.DateTime(attribute='created_at',dt_format='rfc822'),
    'updated_at':fields.DateTime(attribute='updated_at',dt_format='rfc822'),
    'last_login':fields.DateTime(dt_format='rfc822'),
}

#for login response
logged_in_user_response = {
    'access_token':fields.String(),
    'message':fields.String(),
    'status':fields.Integer(),
}

#for Profile Pic data 
profile_data_response = {
    'default':fields.Boolean(attribute='default'),
    'active_profile_pic':fields.String(attribute='active_profile_pic'),
    'created_at':fields.DateTime(attribute='created_at',dt_format='rfc822'),
    'updated_at':fields.DateTime(attribute='updated_at',dt_format='rfc822'),
}

#for user_image_upload 
user_image_response = {
    'created_at': fields.DateTime(dt_format='rfc822'),
    'imagepath':fields.String()
}