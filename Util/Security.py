import hashlib
import time
from random import randrange

from flask import Flask


class Security:
    @classmethod
    def encrypt_password(cls, password: any = None):
        return hashlib.md5(password.encode('utf8')).hexdigest()