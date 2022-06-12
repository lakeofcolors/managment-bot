from db.models import Dashboard, Project
from db.db import new_session


class DashboardService:
    def create_dashboard(self, name, project):
        with new_session() as session:
            new_dashboard = Dashboard(name=name, project_id=project)
            session.add(new_dashboard)
            session.commit()
