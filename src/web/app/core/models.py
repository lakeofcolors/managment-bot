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

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    dashboard_id = db.Column(db.Integer, db.ForeignKey('dashboard.id'))
    status = db.Column(db.String, nullable=False)
