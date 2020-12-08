from configurations import db

class Notification(db.Model):
    __tabelname__ = 'notifications'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    target = db.Column(db.Integer)

    def __init__(self, title, content, target):
        self.title = title
        self.content = content
        self.target = target

