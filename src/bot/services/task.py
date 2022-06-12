from db.models import Task, Dashboard
from db.db import new_session


class TaskService:
    def create_task(self, name, dashboard):
        with new_session as session:
            new_task = Task(name=name, dashboard_id=dashboard)
            session.add(new_task)
            session.commit()
