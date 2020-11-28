from flask import Flask
from extensions import db
from models.UserModel import UserModel


class LabGroupModel(db.Model):

    __tablename__ = 'labs_group'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100))
    supervisor = db.Column(db.Integer)
    type = db.Column(db.Integer)
    years = db.Column(db.Integer)

    @staticmethod
    def init():
        db.create_all()
        print("labs_group table created")

    @staticmethod
    def drop():
        db.drop_all()
        print("labs_group table droped")