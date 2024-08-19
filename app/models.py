
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Project(Base):
    __tablename__ = 'projects'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    tasks = relationship("Task", back_populates="project")
    issues = relationship("Issue", back_populates="project")
    design_rules = relationship("DesignRule", back_populates="project")
    requirements = relationship("Requirement", back_populates="project")
    goals = relationship("ProjectGoal", back_populates="project")
    sbom = relationship("SBOM", back_populates="project", uselist=False)

class Task(Base):
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)
    status = Column(String)
    project_id = Column(Integer, ForeignKey('projects.id'))
    project = relationship("Project", back_populates="tasks")

class Issue(Base):
    __tablename__ = 'issues'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)
    status = Column(String)
    project_id = Column(Integer, ForeignKey('projects.id'))
    project = relationship("Project", back_populates="issues")

class DesignRule(Base):
    __tablename__ = 'design_rules'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)
    project_id = Column(Integer, ForeignKey('projects.id'))
    project = relationship("Project", back_populates="design_rules")

class Requirement(Base):
    __tablename__ = 'requirements'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)
    status = Column(String)
    project_id = Column(Integer, ForeignKey('projects.id'))
    project = relationship("Project", back_populates="requirements")

class ProjectGoal(Base):
    __tablename__ = 'project_goals'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)
    due_date = Column(DateTime)
    project_id = Column(Integer, ForeignKey('projects.id'))
    project = relationship("Project", back_populates="goals")

class SBOM(Base):
    __tablename__ = 'sboms'

    id = Column(Integer, primary_key=True, index=True)
    content = Column(String)
    project_id = Column(Integer, ForeignKey('projects.id'))
    project = relationship("Project", back_populates="sbom")

class Task(Base):
    __tablename__ = "tasks"
