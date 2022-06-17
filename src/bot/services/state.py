from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton

from db.models import Project, Dashboard
from db.db import new_session
from services.chat import ChatService

class UserStateMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        # print(cls._instances)
        user_id = kwargs.get("user_id")
        # print(user_id, 'user_id')
        if not cls._instances.get(user_id):
            instance = super().__call__(*args, **kwargs)
            cls._instances[user_id] = instance
        return cls._instances[user_id]

class StateMenuService(metaclass=UserStateMeta):
    def __init__(self, user_id):
        self.choices_project = None
        self.choices_chat = None
        self.STATES = {
            'pre_init': self.pre_init,
            'choice_chat': None,
            'init': self.init,
            'projects': self.projects,
            'create_project': None,
            'choice': self.choice,
            'create_dashboard': None,
            'choice_dashboard': None
        }
        self.user = user_id
        self.state = "init"


    def init(self, *args, **kwargs):
        kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        buttons = ('/projects', '/craftproject')
        for i in buttons:
            kb.add(KeyboardButton(i))
        return kb


    def pre_init(self, *args, **kwargs):
        chats = ChatService().get_chats(kwargs.get("member_id"))
        kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        for i in chats:
            kb.add(KeyboardButton(i.name))
        return kb

    def get_keyboard(self, *args, **kwargs):
        state = self.state
        return self.STATES.get(state)(*args, **kwargs)


    def projects(self, *args, **kwargs):
        projects = kwargs.get("projects")
        kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        kb.add(KeyboardButton("/back"))
        for i in projects:
            kb.add(KeyboardButton(i.name))
        return kb


    def change_state(self, state):
        if state in self.STATES:
            self.state = state


    def choice(self, *args, **kwargs):
        project_name = self.choices_project
        with new_session() as session:
            project = session.query(Project).filter_by(name=project_name).first()
            dashboards = session.query(Dashboard).filter_by(project_id=project.id)
        kb = ReplyKeyboardMarkup(resize_keyboard=True)
        kb.add(KeyboardButton("/back"))
        kb.add(KeyboardButton("/craftdashboard"))
        for i in dashboards:
            kb.add(KeyboardButton(i.name))
        return kb
