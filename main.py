from typing import List
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel

from models import Project, Task, Issue, DesignRule, Requirement, ProjectGoal, SBOM
from database import get_db

app = FastAPI()

# Schema definitions
class ProjectBase(BaseModel):
    name: str
    description: str

    class Config:
        orm_mode = True

class TaskBase(BaseModel):
    title: str
    description: str
    status: str
    project_id: int

    class Config:
        orm_mode = True

class IssueBase(BaseModel):
    title: str
    description: str
    status: str
    project_id: int

    class Config:
        orm_mode = True

class DesignRuleBase(BaseModel):
    title: str
    description: str
    project_id: int

    class Config:
        orm_mode = True

class RequirementBase(BaseModel):
    title: str
    description: str
    priority: str
    project_id: int

    class Config:
        orm_mode = True

class ProjectGoalBase(BaseModel):
    title: str
    description: str
    status: str
    project_id: int

    class Config:
        orm_mode = True

class SBOMBase(BaseModel):
    component_name: str
    version: str
    license: str
    project_id: int

    class Config:
        orm_mode = True

@app.get('/')
def read_root():
    return {'Hello': 'World'}

# CRUD operations for Project
@app.post('/projects/', response_model=ProjectBase)
def create_project(project: ProjectBase, db: Session = Depends(get_db)):
    db_project = Project(**project.dict())
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project

@app.get('/projects/', response_model=List[ProjectBase])
def read_projects(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    projects = db.query(Project).offset(skip).limit(limit).all()
    return projects

@app.get('/projects/{project_id}', response_model=ProjectBase)
def read_project(project_id: int, db: Session = Depends(get_db)):
    db_project = db.query(Project).filter(Project.id == project_id).first()
    if db_project is None:
        raise HTTPException(status_code=404, detail='Project not found')
    return db_project

@app.put('/projects/{project_id}', response_model=ProjectBase)
def update_project(project_id: int, project: ProjectBase, db: Session = Depends(get_db)):
    db_project = db.query(Project).filter(Project.id == project_id).first()
    if db_project is None:
        raise HTTPException(status_code=404, detail='Project not found')
    for key, value in project.dict().items():
        setattr(db_project, key, value)
    db.commit()
    db.refresh(db_project)
    return db_project

@app.delete('/projects/{project_id} # @@==>> SSHInteractiveSession End-of-Command  <<==@@
cat > main.py << EOL
from typing import List
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel

from models import Project, Task, Issue, DesignRule, Requirement, ProjectGoal, SBOM
from database import get_db

app = FastAPI()

# Schema definitions
class ProjectBase(BaseModel):
    name: str
    description: str

    class Config:
        orm_mode = True

class TaskBase(BaseModel):
    title: str
    description: str
    status: str
    project_id: int

    class Config:
        orm_mode = True

class IssueBase(BaseModel):
    title: str
    description: str
    status: str
    project_id: int

    class Config:
        orm_mode = True

class DesignRuleBase(BaseModel):
    title: str
    description: str
    project_id: int

    class Config:
        orm_mode = True

class RequirementBase(BaseModel):
    title: str
    description: str
    priority: str
    project_id: int

    class Config:
        orm_mode = True

class ProjectGoalBase(BaseModel):
    title: str
    description: str
    status: str
    project_id: int

    class Config:
        orm_mode = True

class SBOMBase(BaseModel):
    component_name: str
    version: str
    license: str
    project_id: int

    class Config:
        orm_mode = True

@app.get('/')
def read_root():
    return {'Hello': 'World'}
