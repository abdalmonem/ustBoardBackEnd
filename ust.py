import os
# from waitress import serve
from flask_migrate import Migrate, upgrade, Manager
from app import create_app, db
from app.models import (
    Users, Admin, Supervisor, Teachers, Student, DeptModel,
    ClassGroup, LabGroup, Materials, Notifications, SchedualeCells,
    ClassSchedualeCells, LabSchedualeCells, Grades
)

app = create_app(os.environ.get('FLASK_CONFIG') or 'default')
migrate = Migrate(app, db)

@app.shell_context_processor
def make_shell_context():
    return dict(
        db=db, Users=Users, Admin=Admin, Supervisor=Supervisor, Teachers=Teachers,
        Student=Student, DeptModel=DeptModel, ClassGroup=ClassGroup, LabGroup=LabGroup,
        Materials=Materials, Notifications=Notifications, SchedualeCells=SchedualeCells,
        ClassSchedualeCells=ClassSchedualeCells, LabSchedualeCells=LabSchedualeCells, Grades=Grades
    )

@app.cli.command()
def deploy():
    """Migrate database"""
    upgrade()

if __name__ == '__main__':
    app.run(debug=True)

# "ust:create_app('production')"