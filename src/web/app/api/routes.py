from flask import send_file, render_template, request, jsonify
from . import bp
from app.core.models import Task, Dashboard
from app.core.extensions import db
from app.core.serializers import TaskSerializer, DashboardSerializer


@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/api/tasks/dashboard/<id>', methods=['GET'])
def tasks_list(id):
    task = Task.query.filter_by(dashboard_id=id).all()
    serializer = TaskSerializer(many=True)
    data = serializer.dump(task)
    return jsonify(data)

@bp.route('/api/tasks/<id>', methods=['GET'])
def get_task(id):
    data = request.json
    task = Task.query.get(id)
    serializer = TaskSerializer()
    data = serializer.dump(task)
    return jsonify(data)

@bp.route('/api/tasks/<id>', methods=['PUT'])
def change_task(id):
    data = request.json
    allowed_statutes = [
        'no_status',
        'todo',
        'in_progress',
        'done'
    ]
    if data['status'] in allowed_statutes:
        task = Task.query.get(id)
        task.status = data['status']
        db.session.commit()
    return 'Change'

@bp.route('/api/tasks/<id>', methods=['DELETE'])
def delete_task(id):
    data = request.json
    Task.query.filter_by(id=id).delete()
    db.session.commit()

    return 'Delete, ty, bro'

@bp.route('/api/tasks/create', methods=['POST'])
def create_task():
    data = request.json
    serializer = TaskSerializer()

    task = Task(
        name = data['name'],
        dashboard_id = data['dashboard_id'],
        status = data['status']
    )
    db.session.add(task)
    db.session.commit()

    return serializer.dump(task)


@bp.route('/api/dashboards', methods=['GET'])
def dashboard_list():
    serializer = DashboardSerializer(many=True)

    dashboards = Dashboard.query.all()
    data = serializer.dump(dashboards)
    return jsonify(data)


@bp.route('/api/dashboard/<id>', methods=['GET'])
def get_dashboard(id):
    dashboard = Dashboard.query.get(id)
    serializer = DashboardSerializer()
    data = serializer.dump(dashboard)
    return jsonify(data)
