from flask.blueprints import Blueprint

api = Blueprint('api', __name__)

from . import (
    Admin, Dept, Groups, Material, Scheduales, Student,
    Supervisor, Teacher, User, LogoutList, Notifications, 
    auth, decorators, email
)