
from project import db
from datetime import datetime

class User(db.Document):
    id = db.SequenceField(primary_key=True)
    email = db.EmailField(unique=True)
    username = db.StringField(max_length=50,required=True)
    first_name =  db.StringField(max_length=10,required=True)
    last_name = db.StringField(max_length=10,required=True)
    country = db.StringField(max_length=10,required=True)
    password = db.StringField(required=True)
    created_at = db.DateTimeField(default=datetime.now)
    updated_at = db.DateTimeField(default=datetime.now)
    last_login = db.DateTimeField(default=datetime.now)

    def to_json(self):
        return {"user_id":int(self.id),
                "email": self.email,
                "username":self.username,
                "full_name":self.first_name+' '+self.last_name,
                "country":self.country,
                "created_at": self.created_at,
                "updated_at":self.updated_at,
                "last_login":self.last_login,
                }

class ProfileImages(db.Document):
    user = db.ReferenceField(User,primary_key=True,reverse_delete_rule=db.CASCADE)
    created_at = db.DateTimeField(default=datetime.now)
    updated_at = db.DateTimeField(default=datetime.now)
    default = db.BooleanField(default=True)
    defaultpic = db.StringField(default='static/profileImages/default/icon.jpg')
    profilepic = db.StringField(null=True)
    def to_json(self):
        return {"user_id":self.user.id,
                "created_at":self.created_at,
                "updated_at":self.updated_at,
                "default":self.default,
                "defaultpic":self.defaultpic,
                "profilepic":self.profilepic,
        }


class ImageUpload(db.Document):
    user = db.ReferenceField(User,reverse_delete_rule=db.CASCADE)
    created_at = db.DateTimeField(default=datetime.now)
    imagepath = db.StringField()

    def to_json(self):
        return {
                "user_id": int(self.user.id),
                "created_at": self.created_at,
                "imagepath":self.imagepath,
                }