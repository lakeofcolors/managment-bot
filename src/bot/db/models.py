from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class Dashboard(Base):
    __tablename__ = "dashboard"
    id = Column(Integer, primary_key=True)
    name = Column(String(30))
    project_id = Column(Integer, ForeignKey("project.id"))
    tasks = relationship("Task")


class Project(Base):
    __tablename__ = "project"
    id = Column(Integer, primary_key=True)
    name = Column(String(30))
    dashboards = relationship("Dashboard")
    owner_id = Column(Integer)
    chat_id = Column(Integer, ForeignKey("chat.id"))


class Task(Base):
    __tablename__ = "task"
    id = Column(Integer, primary_key=True)
    name = Column(String(30))
    dashboard_id = Column(Integer, ForeignKey("dashboard.id"))
    status = Column(String(30))

class Chat(Base):
    __tablename__ = "chat"
    id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer)
    name = Column(String(30))
    manager_id = Column(Integer)
    members = relationship("Member")
    projects = relationship("Project")

class Member(Base):
    __tablename__ = "member"
    id = Column(Integer, primary_key=True)
    name = Column(String(30))
    telegram_id = Column(Integer)
    chat_id = Column(Integer, ForeignKey("chat.id"))
