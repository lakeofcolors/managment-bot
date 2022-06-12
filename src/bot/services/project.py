from db.models import Project
from db.db import new_session


class ProjectService():

    def create_project(self, name, user_id):
        with new_session() as session:

            new_project = Project(name=name)
            session.add(new_project)
            session.commit()


    def get_projects(self, user_id):
        with new_session() as session:
            projects = session.query(Project).all()
            return projects
