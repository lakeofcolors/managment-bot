from .models import Dashboard, Task
from .extensions import ma


class DashboardSerializer(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Dashboard
        include_fk = True


class TaskSerializer(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Task
        include_fk = True
