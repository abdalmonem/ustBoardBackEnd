from flask import Flask
from main_classes.User import User
from models.StudentModel import StudentModel


class Student(User):
    def __init__(self):
        User.__init__(self)

    def set_department_id(self, id: int):
        super().department_id = id


