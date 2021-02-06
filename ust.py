import os
from flask_migrate import Migrate
from application import create_app, db
from application.models import (
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
def test():
    """ Run test file as command """
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)
