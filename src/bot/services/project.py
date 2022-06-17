from db.models import Project
from db.db import new_session


class ProjectService():

    def create_project(self, name, user_id, chat_id):
        with new_session() as session:

            new_project = Project(name=name, owner_id=user_id, chat_id=chat_id)
            session.add(new_project)
            session.commit()


    def get_projects(self, user_id, chat_id):
        with new_session() as session:
            projects = session.query(Project).filter_by(chat_id=chat_id)
            return projects
