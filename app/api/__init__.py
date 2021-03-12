from flask.blueprints import Blueprint
api = Blueprint('api', __name__)

from . import (
    Dept, Groups, Material, Scheduales, Student,
    Supervisor, Teacher, User, auth, decorators, email
)