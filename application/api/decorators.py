from functools import wraps
from flask_jwt_extended import verify_jwt_in_request, get_jwt_claims
from .. import jwt
from ..models import Users

def admin_required(fn):
    @wraps(fn)
    def decorated(*args, **kwargs):
        verify_jwt_in_request()
        claims = get_jwt_claims()
        user = Users.query.filter_by(id=claims['id']).first()
        if not user.is_admin(claims['rank']):
            return {"msg": "unautherized access"}, 403
        return fn(*args, **kwargs)
    return decorated

def supervisor_required(fn):
    @wraps(fn)
    def decorated(*args, **kwargs):
        verify_jwt_in_request()
        claims = get_jwt_claims()
        user = Users.query.filter_by(id=claims['id']).first()
        if not user.is_supervisor(claims['rank']) or not user.is_admin(claims['rank']):
            return {"msg": "unautherized access"}, 403
        return fn(*args, **kwargs)
    return decorated

def confirmed(fn):
    @wraps(fn)
    def decorated(*args, **kwargs):
        verify_jwt_in_request()
        claims = get_jwt_claims()
        if claims['confirmation']:
            return {"msg": "unautherzied, please confirm your account."}, 403
        return fn(*args, **kwargs)
    return decorated
