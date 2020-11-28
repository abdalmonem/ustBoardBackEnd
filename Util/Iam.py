from flask import request
from extensions import db

from main_classes.User import User, UserRank


class Iam:
    id = None
    auth_key = None
    rank = None
    __is_login = False

    def __init__(self):
        self.check_login()

    def check_login(self):
        auth_key = request.headers.get('auth_key')
        id = request.headers.get('id')
        if id is not None and auth_key is not None and id.isnumeric():
            _my_data = db.session.query(User.id, User.auth_key, User.rank).filter(User.id == id)
            if _my_data.scalar() is not None:
                _my_data = _my_data.first()
                if int(_my_data[0]) == int(id) and _my_data[1] == auth_key:
                    self.__is_login = True
                    self.id = id
                    self.auth_key = auth_key
                    self.rank = UserRank(_my_data[2])

    def is_login(self) -> bool:
        return self.__is_login

    def get_rank(self) -> UserRank:
        return self.rank

    def get_id(self) -> int:
        return self.id