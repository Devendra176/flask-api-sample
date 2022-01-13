from flask_restx import abort
from project import ALLOWED_EXTENSIONS, EMAIL_REGEX
from .models import User


def allowed_file(filename):
    """
    This method is used to check images extensions.
    ALLOWED_EXTENSIONS are jpg, png, jpeg.
    """
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def validate_email(email):
    """
    This method is used to check valid email pattern,
    and this is email validator.
    """
    user = User.objects(email=email).first()
    if user:
        abort(409,'Email - %s already exists.'%email)
    email = email.replace(" ","")
    if not email:
        abort(400, 'Email field cannot be empty.')
    if not EMAIL_REGEX.match(email):
        abort(400, 'email- %s is invalid '% email)
        
    return True 

def validate_password(password,confirm_password):
    """
    this is password validation method.
    """
    # password= password.replace(" ","")
    # confirm_password = confirm_password.replace(" ","")
    if not password and not confirm_password:
        abort(400, 'password and confirm_password field cannot be empty.')
    if not password:
        abort(400, 'password field cannot be empty.')
    if not confirm_password:
        abort(400, 'password field cannot be empty.')
    if password != confirm_password:
        abort(400, 'password does not match with confirm password field')
    return True

def validate_username(username):
    if len(username)>50:
        abort(400,'Username cannot be more than 50 characters.')
    return True

def validate_fname_lname(first_name,last_name):
    if len(first_name)>10 or len(last_name)>10:
        abort(400,'first name or last name cannot be more than 10 characters.')
    for i in first_name:
        if i.isdigit():
            abort(400,'Invalid first name: Integer found')
    for i in last_name:
        if i.isdigit():
            abort(400,'Invalid last name: Integer found')
    return True

def validate_country(country):
    if len(country)>10:
        abort(400,'country name cannot be more than 10 characters.')
    for j in country:
        if j.isdigit():
            abort(400,'Invalid country name: Integer found')
    return True