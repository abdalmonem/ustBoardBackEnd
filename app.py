from configurations import app, api, jwt
from resources.User import Login
from resources.Student import AddStudent
from resources.Dept import AddDept

# db.create_all()

api.add_resource(Login, '/login')
api.add_resource(AddStudent, '/add-student')
api.add_resource(AddDept, '/add-dept')
if __name__ == "__main__":
    app.run(debug=True)