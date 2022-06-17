from flask_admin.contrib.sqla import ModelView
from app.core.extensions import db, admin
from app.core.models import Dashboard, Project, Chat, Member, Task


admin.add_view(ModelView(Dashboard, db.session))
admin.add_view(ModelView(Project, db.session))
admin.add_view(ModelView(Task, db.session))
admin.add_view(ModelView(Chat, db.session))
admin.add_view(ModelView(Member, db.session))
