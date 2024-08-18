
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from pydantic import BaseModel
from fastapi import FastAPI, Depends, HTTPException
from typing import List

SQLALCHEMY_DATABASE_URL = "sqlite:///./project_notes.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
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
    project_id = Column(Integer, ForeignKey('projects.id'))

class ProjectBase(BaseModel):
    name: str
    description: str

    class Config:
        orm_mode = True


class Issue(Base):
    __tablename__ = 'issues'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)
    project_id = Column(Integer, ForeignKey('projects.id'))

class DesignRule(Base):
    __tablename__ = 'design_rules'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    project_id = Column(Integer, ForeignKey('projects.id'))

class Requirement(Base):
    __tablename__ = 'requirements'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    project_id = Column(Integer, ForeignKey('projects.id'))

class ProjectGoal(Base):
    __tablename__ = 'project_goals'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    project_id = Column(Integer, ForeignKey('projects.id'))

class SBOM(Base):
    __tablename__ = 'sboms'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    content = Column(String)
    project_id = Column(Integer, ForeignKey('projects.id'))

class IssueBase(BaseModel):
    title: str
    description: str
    project_id: int

    class Config:
        orm_mode = True

class DesignRuleBase(BaseModel):
    name: str
    description: str
    project_id: int

    class Config:
        orm_mode = True

class RequirementBase(BaseModel):
    name: str
    description: str
    project_id: int

    class Config:
        orm_mode = True

class ProjectGoalBase(BaseModel):
    name: str
    description: str
    project_id: int

    class Config:
        orm_mode = True

class SBOMBase(BaseModel):
    name: str
    content: str
    project_id: int

    class Config:
        orm_mode = True
class TaskBase(BaseModel):
    title: str
    description: str
    project_id: int

    class Config:
        orm_mode = True

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# CRUD operations for Project
@app.post("/projects/", response_model=ProjectBase)
def create_project(project: ProjectBase, db: Session = Depends(get_db)):
    db_project = Project(**project.dict())
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project

@app.get("/projects/", response_model=List[ProjectBase])
def read_projects(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    projects = db.query(Project).offset(skip).limit(limit).all()
    return projects

@app.get("/projects/{project_id}", response_model=ProjectBase)
def read_project(project_id: int, db: Session = Depends(get_db)):
    db_project = db.query(Project).filter(Project.id == project_id).first()
    if db_project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    return db_project

@app.put("/projects/{project_id}", response_model=ProjectBase)
def update_project(project_id: int, project: ProjectBase, db: Session = Depends(get_db)):
    db_project = db.query(Project).filter(Project.id == project_id).first()
    if db_project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    for key, value in project.dict().items():
        setattr(db_project, key, value)
    db.commit()
    db.refresh(db_project)
    return db_project

@app.delete("/projects/{project_id}", response_model=ProjectBase)
def delete_project(project_id: int, db: Session = Depends(get_db)):
    db_project = db.query(Project).filter(Project.id == project_id).first()
    if db_project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    db.delete(db_project)
    db.commit()
    return db_project

# CRUD operations for Task
@app.post("/tasks/", response_model=TaskBase)
def create_task(task: TaskBase, db: Session = Depends(get_db)):
    db_task = Task(**task.dict())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

@app.get("/tasks/", response_model=List[TaskBase])
def read_tasks(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    tasks = db.query(Task).offset(skip).limit(limit).all()
    return tasks

@app.get("/tasks/{task_id}", response_model=TaskBase)
def read_task(task_id: int, db: Session = Depends(get_db)):
    db_task = db.query(Task).filter(Task.id == task_id).first()
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task

@app.put("/tasks/{task_id}", response_model=TaskBase)
def update_task(task_id: int, task: TaskBase, db: Session = Depends(get_db)):
    db_task = db.query(Task).filter(Task.id == task_id).first()
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    for key, value in task.dict().items():
        setattr(db_task, key, value)
    db.commit()
    db.refresh(db_task)
    return db_task

@app.delete("/tasks/{task_id}", response_model=TaskBase)
def delete_task(task_id: int, db: Session = Depends(get_db)):
    db_task = db.query(Task).filter(Task.id == task_id).first()
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(db_task)
    db.commit()
    return db_task


# CRUD operations for Issue
@app.post('/issues/', response_model=IssueBase)
def create_issue(issue: IssueBase, db: Session = Depends(get_db)):
    db_issue = Issue(**issue.dict())
    db.add(db_issue)
    db.commit()
    db.refresh(db_issue)
    return db_issue

@app.get('/issues/', response_model=List[IssueBase])
def read_issues(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    issues = db.query(Issue).offset(skip).limit(limit).all()
    return issues

@app.get('/issues/{issue_id}', response_model=IssueBase)
def read_issue(issue_id: int, db: Session = Depends(get_db)):
    db_issue = db.query(Issue).filter(Issue.id == issue_id).first()
    if db_issue is None:
        raise HTTPException(status_code=404, detail='Issue not found')
    return db_issue

@app.put('/issues/{issue_id}', response_model=IssueBase)
def update_issue(issue_id: int, issue: IssueBase, db: Session = Depends(get_db)):
    db_issue = db.query(Issue).filter(Issue.id == issue_id).first()
    if db_issue is None:
        raise HTTPException(status_code=404, detail='Issue not found')
    for key, value in issue.dict().items():
        setattr(db_issue, key, value)
    db.commit()
    db.refresh(db_issue)
    return db_issue

@app.delete('/issues/{issue_id}', response_model=IssueBase)
def delete_issue(issue_id: int, db: Session = Depends(get_db)):
    db_issue = db.query(Issue).filter(Issue.id == issue_id).first()
    if db_issue is None:
        raise HTTPException(status_code=404, detail='Issue not found')
    db.delete(db_issue)
    db.commit()
    return db_issue
@app.post('/design_rules/', response_model=DesignRuleBase)\ndef create_design_rule(design_rule: DesignRuleBase, db: Session = Depends(get_db)):\n    db_design_rule = DesignRule(**design_rule.dict())\n    db.add(db_design_rule)\n    db.commit()\n    db.refresh(db_design_rule)\n    return db_design_rule\n\nBase.metadata.create_all(bind=engine)
\n@app.get('/design_rules/', response_model=List[DesignRuleBase])\ndef read_design_rules(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):\n    design_rules = db.query(DesignRule).offset(skip).limit(limit).all()\n    return design_rules\n\n

@app.get("/design_rules/{design_rule_id}", response_model=DesignRuleBase)
def read_design_rule(design_rule_id: int, db: Session = Depends(get_db)):
    db_design_rule = db.query(DesignRule).filter(DesignRule.id == design_rule_id).first()
    if db_design_rule is None:
        raise HTTPException(status_code=404, detail="Design Rule not found")
    return db_design_rule

@app.put("/design_rules/{design_rule_id}", response_model=DesignRuleBase)
def update_design_rule(design_rule_id: int, design_rule: DesignRuleBase, db: Session = Depends(get_db)):
    db_design_rule = db.query(DesignRule).filter(DesignRule.id == design_rule_id).first()
    if db_design_rule is None:
        raise HTTPException(status_code=404, detail="Design Rule not found")
    for key, value in design_rule.dict().items():
        setattr(db_design_rule, key, value)
    db.commit()
    db.refresh(db_design_rule)
    return db_design_rule

@app.delete("/design_rules/{design_rule_id}", response_model=DesignRuleBase)
def delete_design_rule(design_rule_id: int, db: Session = Depends(get_db)):
    db_design_rule = db.query(DesignRule).filter(DesignRule.id == design_rule_id).first()
    if db_design_rule is None:
        raise HTTPException(status_code=404, detail="Design Rule not found")
    db.delete(db_design_rule)
    db.commit()
    return db_design_rule

# CRUD operations for Requirement
@app.post("/requirements/", response_model=RequirementBase)
def create_requirement(requirement: RequirementBase, db: Session = Depends(get_db)):
    db_requirement = Requirement(**requirement.dict())
    db.add(db_requirement)
    db.commit()
    db.refresh(db_requirement)
    return db_requirement

@app.get("/requirements/", response_model=List[RequirementBase])
def read_requirements(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    requirements = db.query(Requirement).offset(skip).limit(limit).all()
    return requirements

@app.get("/requirements/{requirement_id}", response_model=RequirementBase)
def read_requirement(requirement_id: int, db: Session = Depends(get_db)):
    db_requirement = db.query(Requirement).filter(Requirement.id == requirement_id).first()
    if db_requirement is None:
        raise HTTPException(status_code=404, detail="Requirement not found")
    return db_requirement

@app.put("/requirements/{requirement_id}", response_model=RequirementBase)
def update_requirement(requirement_id: int, requirement: RequirementBase, db: Session = Depends(get_db)):
    db_requirement = db.query(Requirement).filter(Requirement.id == requirement_id).first()
    if db_requirement is None:
        raise HTTPException(status_code=404, detail="Requirement not found")
    for key, value in requirement.dict().items():
        setattr(db_requirement, key, value)
    db.commit()
    db.refresh(db_requirement)
    return db_requirement

@app.delete("/requirements/{requirement_id}", response_model=RequirementBase)
def delete_requirement(requirement_id: int, db: Session = Depends(get_db)):
    db_requirement = db.query(Requirement).filter(Requirement.id == requirement_id).first()
    if db_requirement is None:
        raise HTTPException(status_code=404, detail="Requirement not found")
    db.delete(db_requirement)
    db.commit()
    return db_requirement


# CRUD operations for ProjectGoal
@app.post("/project_goals/", response_model=ProjectGoalBase)
def create_project_goal(project_goal: ProjectGoalBase, db: Session = Depends(get_db)):
    db_project_goal = ProjectGoal(**project_goal.dict())
    db.add(db_project_goal)
    db.commit()
    db.refresh(db_project_goal)
    return db_project_goal

@app.get("/project_goals/", response_model=List[ProjectGoalBase])
def read_project_goals(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    project_goals = db.query(ProjectGoal).offset(skip).limit(limit).all()
    return project_goals

@app.get("/project_goals/{project_goal_id}", response_model=ProjectGoalBase)
def read_project_goal(project_goal_id: int, db: Session = Depends(get_db)):
    db_project_goal = db.query(ProjectGoal).filter(ProjectGoal.id == project_goal_id).first()
    if db_project_goal is None:
        raise HTTPException(status_code=404, detail="Project Goal not found")
    return db_project_goal

@app.put("/project_goals/{project_goal_id}", response_model=ProjectGoalBase)
def update_project_goal(project_goal_id: int, project_goal: ProjectGoalBase, db: Session = Depends(get_db)):
    db_project_goal = db.query(ProjectGoal).filter(ProjectGoal.id == project_goal_id).first()
    if db_project_goal is None:
        raise HTTPException(status_code=404, detail="Project Goal not found")
    for key, value in project_goal.dict().items():
        setattr(db_project_goal, key, value)
    db.commit()
    db.refresh(db_project_goal)
    return db_project_goal

@app.delete("/project_goals/{project_goal_id}", response_model=ProjectGoalBase)
def delete_project_goal(project_goal_id: int, db: Session = Depends(get_db)):
    db_project_goal = db.query(ProjectGoal).filter(ProjectGoal.id == project_goal_id).first()
    if db_project_goal is None:
        raise HTTPException(status_code=404, detail="Project Goal not found")
    db.delete(db_project_goal)
    db.commit()
    return db_project_goal


# CRUD operations for SBOM
@app.post("/sboms/", response_model=SBOMBase)
def create_sbom(sbom: SBOMBase, db: Session = Depends(get_db)):
    db_sbom = SBOM(**sbom.dict())
    db.add(db_sbom)
    db.commit()
    db.refresh(db_sbom)
    return db_sbom

@app.get("/sboms/", response_model=List[SBOMBase])
def read_sboms(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    sboms = db.query(SBOM).offset(skip).limit(limit).all()
    return sboms

@app.get("/sboms/{sbom_id}", response_model=SBOMBase)
def read_sbom(sbom_id: int, db: Session = Depends(get_db)):
    db_sbom = db.query(SBOM).filter(SBOM.id == sbom_id).first()
    if db_sbom is None:
        raise HTTPException(status_code=404, detail="SBOM not found")
    return db_sbom

@app.put("/sboms/{sbom_id}", response_model=SBOMBase)
def update_sbom(sbom_id: int, sbom: SBOMBase, db: Session = Depends(get_db)):
    db_sbom = db.query(SBOM).filter(SBOM.id == sbom_id).first()
    if db_sbom is None:
        raise HTTPException(status_code=404, detail="SBOM not found")
    for key, value in sbom.dict().items():
        setattr(db_sbom, key, value)
    db.commit()
    db.refresh(db_sbom)
    return db_sbom

@app.delete("/sboms/{sbom_id}", response_model=SBOMBase)
def delete_sbom(sbom_id: int, db: Session = Depends(get_db)):
    db_sbom = db.query(SBOM).filter(SBOM.id == sbom_id).first()
    if db_sbom is None:
        raise HTTPException(status_code=404, detail="SBOM not found")
    db.delete(db_sbom)
    db.commit()
    return db_sbom

# Main execution block
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
