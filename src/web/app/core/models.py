from app.core.extensions import db


class Dashboard(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'))
    tasks = db.relationship('Task', backref='dashboard')

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    dashboards = db.relationship('Dashboard', backref='project')
    owner_id = db.Column(db.Integer)
    chat_id = db.Column(db.Integer, db.ForeignKey("chat.id"))

class Task(db.Model):
    # TODO creator_id
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    dashboard_id = db.Column(db.Integer, db.ForeignKey('dashboard.id'))
    status = db.Column(db.String, nullable=False)


class Chat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    telegram_id = db.Column(db.Integer)
    name = db.Column(db.String(30))
    manager_id = db.Column(db.Integer)
    members = db.relationship("Member", backref='chat')
    projects = db.relationship("Project", backref='chat')

class Member(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    telegram_id = db.Column(db.Integer)
    chat_id = db.Column(db.Integer, db.ForeignKey('chat.id'))
