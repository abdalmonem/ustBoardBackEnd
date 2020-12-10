import os
from flask import jsonify
from configurations import app, api, jwt
from resources.User import Login
from resources.Student import AddStudent
from resources.Teacher import Teacher
from resources.Supervisor import SuperVisor
from models.AdminModel import Admin
from resources.Dept import AddDept
from resources.Material import Material
from resources.Groups import ClassGroup, LabGroup
from resources.Scheduales import LabScheduales, ClassScheduales


# db.create_all()
@app.route('/', methods=['GET'])
def index():
    # admin = Admin('admin2', '6666', 'admin2@admin', '6666', 'Hekmat', '20201209')
    # admin.save_data()
    return {"msg": "Hello World."}

api.add_resource(Login, '/login')
api.add_resource(AddStudent, '/add-student')
api.add_resource(Teacher, '/add-teacher')
api.add_resource(AddDept, '/add-dept')
api.add_resource(SuperVisor, '/add-supervisor')
api.add_resource(Material, '/add-material')
api.add_resource(ClassGroup, '/add-class-group')
api.add_resource(LabGroup, '/add-lab-group')
api.add_resource(ClassScheduales, '/add-class-scheduale')
api.add_resource(LabScheduales, '/add-lab-scheduale')

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
