
from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session, relationship
from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

# Database setup
SQLALCHEMY_DATABASE_URL = "sqlite:///./projects.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# SQLAlchemy models
class Project(Base):
    __tablename__ = "projects"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    tasks = relationship("Task", back_populates="project")
    issues = relationship("Issue", back_populates="project")
    design_rules = relationship("DesignRule", back_populates="project")
    requirements = relationship("Requirement", back_populates="project")
    project_goals = relationship("ProjectGoal", back_populates="project")
    sbom_entries = relationship("SBOM", back_populates="project")

class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)
    status = Column(String)
    priority = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    project_id = Column(Integer, ForeignKey("projects.id"))
    
    project = relationship("Project", back_populates="tasks")

class Issue(Base):
    __tablename__ = "issues"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)
    status = Column(String)
    priority = Column(String)
    is_recurring = Column(Boolean)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    project_id = Column(Integer, ForeignKey("projects.id"))
    
    project = relationship("Project", back_populates="issues")

class DesignRule(Base):
    __tablename__ = "design_rules"
    id = Column(Integer, primary_key=True, index=True)
    rule = Column(String)
    description = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    project_id = Column(Integer, ForeignKey("projects.id"))
    
    project = relationship("Project", back_populates="design_rules")

class Requirement(Base):
    __tablename__ = "requirements"
    id = Column(Integer, primary_key=True, index=True)
    requirement = Column(String)
    description = Column(String)
    priority = Column(String)
    status = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    project_id = Column(Integer, ForeignKey("projects.id"))
    
    project = relationship("Project", back_populates="requirements")

class ProjectGoal(Base):
    __tablename__ = "project_goals"
    id = Column(Integer, primary_key=True, index=True)
    goal = Column(String)
    description = Column(String)
    status = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    project_id = Column(Integer, ForeignKey("projects.id"))
    
    project = relationship("Project", back_populates="project_goals")

class SBOM(Base):
    __tablename__ = "sbom_entries"
    id = Column(Integer, primary_key=True, index=True)
    component = Column(String)
    version = Column(String)
    license = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    project_id = Column(Integer, ForeignKey("projects.id"))
    
    project = relationship("Project", back_populates="sbom_entries")

# Pydantic models for request/response schemas
class ProjectBase(BaseModel):
    name: str
    description: str

class ProjectCreate(ProjectBase):
    pass

class Project(ProjectBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class TaskBase(BaseModel):
    title: str
    description: str
    status: str
    priority: str

class TaskCreate(TaskBase):
    project_id: int

class Task(TaskBase):
    id: int
    created_at: datetime
    updated_at: datetime
    project_id: int

    class Config:
        orm_mode = True

class IssueBase(BaseModel):
    title: str
    description: str
    status: str
    priority: str
    is_recurring: bool

class IssueCreate(IssueBase):
    project_id: int

class Issue(IssueBase):
    id: int
    created_at: datetime
    updated_at: datetime
    project_id: int

    class Config:
        orm_mode = True

class DesignRuleBase(BaseModel):
    rule: str
    description: str

class DesignRuleCreate(DesignRuleBase):
    project_id: int

class DesignRule(DesignRuleBase):
    id: int
    created_at: datetime
    updated_at: datetime
    project_id: int

    class Config:
        orm_mode = True

class RequirementBase(BaseModel):
    requirement: str
    description: str
    priority: str
    status: str

class RequirementCreate(RequirementBase):
    project_id: int

class Requirement(RequirementBase):
    id: int
    created_at: datetime
    updated_at: datetime
    project_id: int

    class Config:
        orm_mode = True

class ProjectGoalBase(BaseModel):
    goal: str
    description: str
    status: str

class ProjectGoalCreate(ProjectGoalBase):
    project_id: int

class ProjectGoal(ProjectGoalBase):
    id: int
    created_at: datetime
    updated_at: datetime
    project_id: int

    class Config:
        orm_mode = True

class SBOMBase(BaseModel):
    component: str
    version: str
    license: str

class SBOMCreate(SBOMBase):
    project_id: int

class SBOM(SBOMBase):
    id: int
    created_at: datetime
    updated_at: datetime
    project_id: int

    class Config:
        orm_mode = True

# Database Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Initialize FastAPI app
app = FastAPI()

# Create tables
Base.metadata.create_all(bind=engine)

@app.post("/projects/", response_model=Project)
def create_project(project: ProjectCreate, db: Session = Depends(get_db)):
    db_project = Project(**project.dict())
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project

@app.get("/projects/", response_model=List[Project])
def read_projects(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    projects = db.query(Project).offset(skip).limit(limit).all()
    return projects

@app.get("/projects/{id}", response_model=Project)
def read_project(id: int, db: Session = Depends(get_db)):
    db_project = db.query(Project).filter(Project.id == id).first()
    if db_project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    return db_project

@app.put("/projects/{id}", response_model=Project)
def update_project(id: int, project: ProjectCreate, db: Session = Depends(get_db)):
    db_project = db.query(Project).filter(Project.id == id).first()
    if db_project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    for key, value in project.dict().items():
        setattr(db_project, key, value)
    db.commit()
    db.refresh(db_project)
    return db_project

@app.delete("/projects/{id}", response_model=Project)
def delete_project(id: int, db: Session = Depends(get_db)):
    db_project = db.query(Project).filter(Project.id == id).first()
    if db_project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    db.delete(db_project)
    db.commit()
    return db_project
