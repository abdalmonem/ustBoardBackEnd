from functools import wraps
from flask_jwt_extended import verify_jwt_in_request, get_jwt_claims
from .. import jwt
from ..models import Users

def admin_required(fn):
    @wraps(fn)
    def decorated(*args, **kwargs):
        verify_jwt_in_request()
        claims = get_jwt_claims()
        print(claims)
        user = Users.find_by_id(claims['id'])
        if not user.is_admin(claims['rank']):
            return {"message": "unautherized access"}, 403
        return fn(*args, **kwargs)
    return decorated

def supervisor_required(fn):
    @wraps(fn)
    def decorated(*args, **kwargs):
        verify_jwt_in_request()
        claims = get_jwt_claims()
        user = Users.find_by_id(claims['id'])
        if not user.is_supervisor(claims['rank']) and not user.is_admin(claims['rank']):
            return {"message": "unautherized access"}, 403
        return fn(*args, **kwargs)
    return decorated

def confirmed(fn):
    @wraps(fn)
    def decorated(*args, **kwargs):
        verify_jwt_in_request()
        claims = get_jwt_claims()
        user = Users.find_by_id(claims['id'])
        if user.confirmed == False:
            return {"msg": "unautherzied, please confirm your account."}, 403
        return fn(*args, **kwargs)
    return decorated
