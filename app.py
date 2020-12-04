from flask import jsonify
from configurations import app, api, jwt
from resources.User import Login
from resources.Student import AddStudent
from resources.Dept import AddDept
from resources.Supervisor import AddSuperVisor
from models.AdminModel import Admin

# db.create_all()
# @app.route('/', methods=['GET'])
# def index():
#     admin = Admin('admin', '12345', 'admin@admin', '1234', 'Adminstrator', '20201209')
#     admin.save_data()
#     return {"msg": "admin created."}

api.add_resource(Login, '/login')
api.add_resource(AddStudent, '/add-student')
api.add_resource(AddDept, '/add-dept')
api.add_resource(AddSuperVisor, '/add-supervisor')
if __name__ == "__main__":
    app.run(debug=True)