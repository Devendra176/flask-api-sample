from flask_restx import fields
#for User Registration

registration_resource = {
    'email': fields.String(required=True,example='example@domain.com'),
    'username':fields.String(required=True,description='Enter less than 50 characters.'),
    'first_name':fields.String(required=True,description='Enter less than 10 characters.'),
    'last_name':fields.String(required=True,description='Enter less than 10 characters.'),
    'country':fields.String(required=True,description='Enter less than 10 characters.'),
    'password':fields.String(required=True,example='string'),
    'confirm_password':fields.String(required=True,example='string'),
}

update_userdeatils_resource = {
    'username':fields.String(required=True,description='Enter less than 50 characters.'),
    'first_name':fields.String(required=True,description='Enter less than 10 characters.'),
    'last_name':fields.String(required=True,description='Enter less than 10 characters.'),
    'country':fields.String(required=True,description='Enter less than 10 characters.'),
}

