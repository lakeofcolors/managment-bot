from db.models import Dashboard, Project
from db.db import new_session


class DashboardService:
    def create_dashboard(self, name, project):
        with new_session() as session:
            new_dashboard = Dashboard(name=name, project_id=project)
            session.add(new_dashboard)
            session.commit()


    def get_dashboard(self, dashboard_name):
        with new_session() as session:
            dashboard = session.query(Dashboard).filter_by(name=dashboard_name).first()
            return dashboard
