import redis

from flask_restx import abort

from flask_jwt_extended import JWTManager

from project.models import User



jwt_redis_blocklist = redis.StrictRedis(
    host="localhost", port=6379, db=0, decode_responses=True
)

jwt = JWTManager()

@jwt.user_identity_loader
def user_identity_lookup(user):
    return user.id
@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    return User.objects.get(id=identity) if User.objects(id=identity).first() else abort(404,'User not found in database')

@jwt.token_in_blocklist_loader
def check_if_token_is_revoked(jwt_header, jwt_payload):
    jti = jwt_payload["jti"]
    token_in_redis = jwt_redis_blocklist.get(jti)
    return token_in_redis is not None