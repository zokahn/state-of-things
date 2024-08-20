from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
import datetime

Base = declarative_base()

class Project(Base):
    __tablename__ = 'projects'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)

class Task(Base):
    __tablename__ = 'tasks'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)
    status = Column(String)
    priority = Column(String)
    project_id = Column(Integer, ForeignKey('projects.id'))

class Issue(Base):
    __tablename__ = 'issues'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)
    status = Column(String)
    project_id = Column(Integer, ForeignKey('projects.id'))

class DesignRule(Base):
    __tablename__ = 'design_rules'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)
    project_id = Column(Integer, ForeignKey('projects.id'))

class Requirement(Base):
    __tablename__ = 'requirements'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)
    priority = Column(String)
    project_id = Column(Integer, ForeignKey('projects.id'))

class ProjectGoal(Base):
    __tablename__ = 'project_goals'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)
    status = Column(String)
    project_id = Column(Integer, ForeignKey('projects.id'))

class SBOM(Base):
    __tablename__ = 'sbom_entries'
    id = Column(Integer, primary_key=True, index=True)
    component_name = Column(String, index=True)
    version = Column(String)
    license = Column(String)
    project_id = Column(Integer, ForeignKey('projects.id'))

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
