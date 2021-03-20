# from flask_jwt_extended import current_user
from flask_jwt_extended import get_jwt_claims, get_current_user
from random import randint
from flask import request, current_app
from . import api
from .LogoutList import LogoutList
from .email import send_verfy_mail
from ..models import Users
from .. import jwt

@jwt.user_claims_loader
def user_rank(identity):
    if identity:
        user = Users.query.filter_by(id=identity).first()
        rank = user.get_rank(identity)
        if not rank:
            return {"msg": "login required"}
        return {"id" : identity, "rank": rank}

@jwt.token_in_blacklist_loader
def check_token(decrypted_token):
    return decrypted_token['jti'] in LogoutList
