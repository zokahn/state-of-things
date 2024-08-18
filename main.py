
from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from typing import List
from datetime import datetime
from pydantic import BaseModel
import logging

# Import your database models and session here
# from database import SessionLocal, engine
# from models import Base, Project, Task, Issue, DesignRule, Requirement, ProjectGoal, SBOM

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Health check endpoint
@app.get("/health")
def health_check():
    return {"status": "healthy"}

# Helper function for pagination
def paginate(query, skip: int = 0, limit: int = 100):
    return query.offset(skip).limit(limit).all()


from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from pydantic import BaseModel

# Import your database models and session here
# from database import SessionLocal, engine
# from models import Base, Project, Task, Issue, DesignRule, Requirement, ProjectGoal, SBOM

# Schema definitions
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
    project_id: int

class TaskCreate(TaskBase):
    pass

class Task(TaskBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class IssueBase(BaseModel):
    title: str
    description: str
    status: str
    project_id: int

class IssueCreate(IssueBase):
    pass

class Issue(IssueBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class DesignRuleBase(BaseModel):
    title: str
    description: str
    project_id: int

class DesignRuleCreate(DesignRuleBase):
    pass

class DesignRule(DesignRuleBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class RequirementBase(BaseModel):
    title: str
    description: str
    priority: str
    project_id: int

class RequirementCreate(RequirementBase):
    pass

class Requirement(RequirementBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class ProjectGoalBase(BaseModel):
    title: str
    description: str
    status: str
    project_id: int

class ProjectGoalCreate(ProjectGoalBase):
    pass

class ProjectGoal(ProjectGoalBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class SBOMBase(BaseModel):
    component_name: str
    version: str
    license: str
    project_id: int

class SBOMCreate(SBOMBase):
    pass

class SBOM(SBOMBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

# Initialize FastAPI app
app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# CRUD operations for Project
@app.post("/projects/", response_model=Project)
def create_project(project: ProjectCreate, db: Session = Depends(get_db)):
    try:
        db_project = Project(**project.dict())
        db.add(db_project)
        db.commit()
        db.refresh(db_project)
        logger.info(f"Created project: {db_project.id}")
        return db_project
    except SQLAlchemyError as e:
        logger.error(f"Error creating project: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail="Could not create project")

@app.get("/projects/", response_model=List[Project])
def read_projects(skip: int = Query(0, ge=0), limit: int = Query(100, ge=1, le=100), db: Session = Depends(get_db)):
    projects = paginate(db.query(Project), skip, limit)
    return projects

@app.get("/projects/{project_id}", response_model=Project)
def read_project(project_id: int, db: Session = Depends(get_db)):
    db_project = db.query(Project).filter(Project.id == project_id).first()
    if db_project is None:
        logger.warning(f"Project not found: {project_id}")
        raise HTTPException(status_code=404, detail="Project not found")
    return db_project

@app.put("/projects/{project_id}", response_model=Project)
def update_project(project_id: int, project: ProjectCreate, db: Session = Depends(get_db)):
    try:
        db_project = db.query(Project).filter(Project.id == project_id).first()
        if db_project is None:
            logger.warning(f"Project not found for update: {project_id}")
            raise HTTPException(status_code=404, detail="Project not found")
        for key, value in project.dict().items():
            setattr(db_project, key, value)
        db_project.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(db_project)
        logger.info(f"Updated project: {project_id}")
        return db_project
    except SQLAlchemyError as e:
        logger.error(f"Error updating project: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail="Could not update project")

@app.delete("/projects/{project_id}", response_model=Project)
def delete_project(project_id: int, db: Session = Depends(get_db)):
    try:
        db_project = db.query(Project).filter(Project.id == project_id).first()
        if db_project is None:
            logger.warning(f"Project not found for deletion: {project_id}")
            raise HTTPException(status_code=404, detail="Project not found")
        db.delete(db_project)
        db.commit()
        logger.info(f"Deleted project: {project_id}")
        return db_project
    except SQLAlchemyError as e:
        logger.error(f"Error deleting project: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail="Could not delete project")


# CRUD operations for Task
@app.post("/tasks/", response_model=Task)
def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    try:
        db_task = Task(**task.dict())
        db.add(db_task)
        db.commit()
        db.refresh(db_task)
        logger.info(f"Created task: {db_task.id}")
        return db_task
    except SQLAlchemyError as e:
        logger.error(f"Error creating task: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail="Could not create task")

@app.get("/tasks/", response_model=List[Task])
def read_tasks(skip: int = Query(0, ge=0), limit: int = Query(100, ge=1, le=100), db: Session = Depends(get_db)):
    tasks = paginate(db.query(Task), skip, limit)
    return tasks

@app.get("/tasks/{task_id}", response_model=Task)
def read_task(task_id: int, db: Session = Depends(get_db)):
    db_task = db.query(Task).filter(Task.id == task_id).first()
    if db_task is None:
        logger.warning(f"Task not found: {task_id}")
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task

@app.put("/tasks/{task_id}", response_model=Task)
def update_task(task_id: int, task: TaskCreate, db: Session = Depends(get_db)):
    try:
        db_task = db.query(Task).filter(Task.id == task_id).first()
        if db_task is None:
            logger.warning(f"Task not found for update: {task_id}")
            raise HTTPException(status_code=404, detail="Task not found")
        for key, value in task.dict().items():
            setattr(db_task, key, value)
        db_task.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(db_task)
        logger.info(f"Updated task: {task_id}")
        return db_task
    except SQLAlchemyError as e:
        logger.error(f"Error updating task: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail="Could not update task")

@app.delete("/tasks/{task_id}", response_model=Task)
def delete_task(task_id: int, db: Session = Depends(get_db)):
    try:
        db_task = db.query(Task).filter(Task.id == task_id).first()
        if db_task is None:
            logger.warning(f"Task not found for deletion: {task_id}")
            raise HTTPException(status_code=404, detail="Task not found")
        db.delete(db_task)
        db.commit()
        logger.info(f"Deleted task: {task_id}")
        return db_task
    except SQLAlchemyError as e:
        logger.error(f"Error deleting task: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail="Could not delete task")


# CRUD operations for Issue
@app.post("/issues/", response_model=Issue)
def create_issue(issue: IssueCreate, db: Session = Depends(get_db)):
    try:
        db_issue = Issue(**issue.dict())
        db.add(db_issue)
        db.commit()
        db.refresh(db_issue)
        logger.info(f"Created issue: {db_issue.id}")
        return db_issue
    except SQLAlchemyError as e:
        logger.error(f"Error creating issue: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail="Could not create issue")

@app.get("/issues/", response_model=List[Issue])
def read_issues(skip: int = Query(0, ge=0), limit: int = Query(100, ge=1, le=100), db: Session = Depends(get_db)):
    issues = paginate(db.query(Issue), skip, limit)
    return issues

@app.get("/issues/{issue_id}", response_model=Issue)
def read_issue(issue_id: int, db: Session = Depends(get_db)):
    db_issue = db.query(Issue).filter(Issue.id == issue_id).first()
    if db_issue is None:
        logger.warning(f"Issue not found: {issue_id}")
        raise HTTPException(status_code=404, detail="Issue not found")
    return db_issue

# CRUD operations for DesignRule
@app.post("/design_rules/", response_model=DesignRule)
def create_design_rule(design_rule: DesignRuleCreate, db: Session = Depends(get_db)):
    db_design_rule = DesignRule(**design_rule.dict())
    db.add(db_design_rule)
    db.commit()
    db.refresh(db_design_rule)
    return db_design_rule

@app.get("/design_rules/", response_model=List[DesignRule])
def read_design_rules(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    design_rules = db.query(DesignRule).offset(skip).limit(limit).all()
    return design_rules

@app.get("/design_rules/{design_rule_id}", response_model=DesignRule)
def read_design_rule(design_rule_id: int, db: Session = Depends(get_db)):
    db_design_rule = db.query(DesignRule).filter(DesignRule.id == design_rule_id).first()
    if db_design_rule is None:
        raise HTTPException(status_code=404, detail="Design rule not found")
    return db_design_rule

@app.put("/design_rules/{design_rule_id}", response_model=DesignRule)
def update_design_rule(design_rule_id: int, design_rule: DesignRuleCreate, db: Session = Depends(get_db)):
    db_design_rule = db.query(DesignRule).filter(DesignRule.id == design_rule_id).first()
    if db_design_rule is None:
        raise HTTPException(status_code=404, detail="Design rule not found")
    for key, value in design_rule.dict().items():
        setattr(db_design_rule, key, value)
    db_design_rule.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_design_rule)
    return db_design_rule

@app.delete("/design_rules/{design_rule_id}", response_model=DesignRule)
def delete_design_rule(design_rule_id: int, db: Session = Depends(get_db)):
    db_design_rule = db.query(DesignRule).filter(DesignRule.id == design_rule_id).first()
    if db_design_rule is None:
        raise HTTPException(status_code=404, detail="Design rule not found")
    db.delete(db_design_rule)
    db.commit()
    return db_design_rule

# CRUD operations for Requirement
@app.post("/requirements/", response_model=Requirement)
def create_requirement(requirement: RequirementCreate, db: Session = Depends(get_db)):
    db_requirement = Requirement(**requirement.dict())
    db.add(db_requirement)
    db.commit()
    db.refresh(db_requirement)
    return db_requirement

@app.get("/requirements/", response_model=List[Requirement])
def read_requirements(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    requirements = db.query(Requirement).offset(skip).limit(limit).all()
    return requirements

@app.get("/requirements/{requirement_id}", response_model=Requirement)
def read_requirement(requirement_id: int, db: Session = Depends(get_db)):
    db_requirement = db.query(Requirement).filter(Requirement.id == requirement_id).first()
    if db_requirement is None:
        raise HTTPException(status_code=404, detail="Requirement not found")
    return db_requirement

@app.put("/requirements/{requirement_id}", response_model=Requirement)
def update_requirement(requirement_id: int, requirement: RequirementCreate, db: Session = Depends(get_db)):
    db_requirement = db.query(Requirement).filter(Requirement.id == requirement_id).first()
    if db_requirement is None:
        raise HTTPException(status_code=404, detail="Requirement not found")
    for key, value in requirement.dict().items():
        setattr(db_requirement, key, value)
    db_requirement.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_requirement)
    return db_requirement

@app.delete("/requirements/{requirement_id}", response_model=Requirement)
def delete_requirement(requirement_id: int, db: Session = Depends(get_db)):
    db_requirement = db.query(Requirement).filter(Requirement.id == requirement_id).first()
    if db_requirement is None:
        raise HTTPException(status_code=404, detail="Requirement not found")
    db.delete(db_requirement)
    db.commit()
    return db_requirement

# CRUD operations for ProjectGoal
@app.post("/project_goals/", response_model=ProjectGoal)
def create_project_goal(project_goal: ProjectGoalCreate, db: Session = Depends(get_db)):
    db_project_goal = ProjectGoal(**project_goal.dict())
    db.add(db_project_goal)
    db.commit()
    db.refresh(db_project_goal)
    return db_project_goal

@app.get("/project_goals/", response_model=List[ProjectGoal])
def read_project_goals(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    project_goals = db.query(ProjectGoal).offset(skip).limit(limit).all()
    return project_goals

@app.get("/project_goals/{project_goal_id}", response_model=ProjectGoal)
def read_project_goal(project_goal_id: int, db: Session = Depends(get_db)):
    db_project_goal = db.query(ProjectGoal).filter(ProjectGoal.id == project_goal_id).first()
    if db_project_goal is None:
        raise HTTPException(status_code=404, detail="Project goal not found")
    return db_project_goal

@app.put("/project_goals/{project_goal_id}", response_model=ProjectGoal)
def update_project_goal(project_goal_id: int, project_goal: ProjectGoalCreate, db: Session = Depends(get_db)):
    db_project_goal = db.query(ProjectGoal).filter(ProjectGoal.id == project_goal_id).first()
    if db_project_goal is None:
        raise HTTPException(status_code=404, detail="Project goal not found")
    for key, value in project_goal.dict().items():
        setattr(db_project_goal, key, value)
    db_project_goal.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_project_goal)
    return db_project_goal

@app.delete("/project_goals/{project_goal_id}", response_model=ProjectGoal)
def delete_project_goal(project_goal_id: int, db: Session = Depends(get_db)):
    db_project_goal = db.query(ProjectGoal).filter(ProjectGoal.id == project_goal_id).first()
    if db_project_goal is None:
        raise HTTPException(status_code=404, detail="Project goal not found")
    db.delete(db_project_goal)
    db.commit()
    return db_project_goal

# CRUD operations for SBOM
@app.post("/sboms/", response_model=SBOM)
def create_sbom(sbom: SBOMCreate, db: Session = Depends(get_db)):
    db_sbom = SBOM(**sbom.dict())
    db.add(db_sbom)
    db.commit()
    db.refresh(db_sbom)
    return db_sbom

@app.get("/sboms/", response_model=List[SBOM])
def read_sboms(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    sboms = db.query(SBOM).offset(skip).limit(limit).all()
    return sboms

@app.get("/sboms/{sbom_id}", response_model=SBOM)
def read_sbom(sbom_id: int, db: Session = Depends(get_db)):
    db_sbom = db.query(SBOM).filter(SBOM.id == sbom_id).first()
    if db_sbom is None:
        raise HTTPException(status_code=404, detail="SBOM not found")
    return db_sbom

@app.put("/sboms/{sbom_id}", response_model=SBOM)
def update_sbom(sbom_id: int, sbom: SBOMCreate, db: Session = Depends(get_db)):
    db_sbom = db.query(SBOM).filter(SBOM.id == sbom_id).first()
    if db_sbom is None:
        raise HTTPException(status_code=404, detail="SBOM not found")
    for key, value in sbom.dict().items():
        setattr(db_sbom, key, value)
    db_sbom.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_sbom)
    return db_sbom

@app.delete("/sboms/{sbom_id}", response_model=SBOM)
def delete_sbom(sbom_id: int, db: Session = Depends(get_db)):
    db_sbom = db.query(SBOM).filter(SBOM.id == sbom_id).first()
    if db_sbom is None:
        raise HTTPException(status_code=404, detail="SBOM not found")
    db.delete(db_sbom)
    db.commit()
    return db_sbom

# CRUD operations for DesignRule
@app.post("/design_rules/", response_model=DesignRule)
def create_design_rule(design_rule: DesignRuleCreate, db: Session = Depends(get_db)):
    try:
        db_design_rule = DesignRule(**design_rule.dict())
        db.add(db_design_rule)
        db.commit()
        db.refresh(db_design_rule)
        logger.info(f"Created design rule: {db_design_rule.id}")
        return db_design_rule
    except SQLAlchemyError as e:
        logger.error(f"Error creating design rule: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail="Could not create design rule")

@app.get("/design_rules/", response_model=List[DesignRule])
def read_design_rules(skip: int = Query(0, ge=0), limit: int = Query(100, ge=1, le=100), db: Session = Depends(get_db)):
    design_rules = paginate(db.query(DesignRule), skip, limit)
    return design_rules

@app.get("/design_rules/{design_rule_id}", response_model=DesignRule)
def read_design_rule(design_rule_id: int, db: Session = Depends(get_db)):
    db_design_rule = db.query(DesignRule).filter(DesignRule.id == design_rule_id).first()
    if db_design_rule is None:
        logger.warning(f"Design rule not found: {design_rule_id}")
        raise HTTPException(status_code=404, detail="Design rule not found")
    return db_design_rule

@app.put("/design_rules/{design_rule_id}", response_model=DesignRule)
def update_design_rule(design_rule_id: int, design_rule: DesignRuleCreate, db: Session = Depends(get_db)):
    try:
        db_design_rule = db.query(DesignRule).filter(DesignRule.id == design_rule_id).first()
        if db_design_rule is None:
            logger.warning(f"Design rule not found for update: {design_rule_id}")
            raise HTTPException(status_code=404, detail="Design rule not found")
        for key, value in design_rule.dict().items():
            setattr(db_design_rule, key, value)
        db_design_rule.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(db_design_rule)
        logger.info(f"Updated design rule: {design_rule_id}")
        return db_design_rule
    except SQLAlchemyError as e:
        logger.error(f"Error updating design rule: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail="Could not update design rule")

@app.delete("/design_rules/{design_rule_id}", response_model=DesignRule)
def delete_design_rule(design_rule_id: int, db: Session = Depends(get_db)):
    try:
        db_design_rule = db.query(DesignRule).filter(DesignRule.id == design_rule_id).first()
        if db_design_rule is None:
            logger.warning(f"Design rule not found for deletion: {design_rule_id} \
# @@==>> SSHInteractiveSession End-of-Command  <<==@@
raise HTTPException(status_code=404, detail="Design rule not found")
        db.delete(db_design_rule)
        db.commit()
        logger.info(f"Deleted design rule: {design_rule_id}")
        return db_design_rule
    except SQLAlchemyError as e:
        logger.error(f"Error deleting design rule: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail="Could not delete design rule")

# CRUD operations for Project
@app.post("/projects/", response_model=Project)
def create_project(project: ProjectCreate, db: Session = Depends(get_db)):
    try:
        db_project = Project(**project.dict())
        db.add(db_project)
        db.commit()
        db.refresh(db_project)
        logger.info(f"Created project: {db_project.id}")
        return db_project
    except SQLAlchemyError as e:
        logger.error(f"Error creating project: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail="Could not create project")

@app.get("/projects/", response_model=List[Project])
def read_projects(skip: int = Query(0, ge=0), limit: int = Query(100, ge=1, le=100), db: Session = Depends(get_db)):
    projects = paginate(db.query(Project), skip, limit)
    return projects

@app.get("/projects/{project_id}", response_model=Project)
def read_project(project_id: int, db: Session = Depends(get_db)):
    db_project = db.query(Project).filter(Project.id == project_id).first()
    if db_project is None:
        logger.warning(f"Project not found: {project_id}")
        raise HTTPException(status_code=404, detail="Project not found")
    return db_project

@app.put("/projects/{project_id}", response_model=Project)
def update_project(project_id: int, project: ProjectCreate, db: Session = Depends(get_db)):
    try:
        db_project = db.query(Project).filter(Project.id == project_id).first()
        if db_project is None:
            logger.warning(f"Project not found for update: {project_id}")
            raise HTTPException(status_code=404, detail="Project not found")
        for key, value in project.dict().items():
            setattr(db_project, key, value)
        db_project.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(db_project)
        logger.info(f"Updated project: {project_id}")
        return db_project
    except SQLAlchemyError as e:
        logger.error(f"Error updating project: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail="Could not update project")

@app.delete("/projects/{project_id}", response_model=Project)
def delete_project(project_id: int, db: Session = Depends(get_db)):
    try:
        db_project = db.query(Project).filter(Project.id == project_id).first()
        if db_project is None:
            logger.warning(f"Project not found for deletion: {project_id}")
            raise HTTPException(status_code=404, detail="Project not found")
        db.delete(db_project)
        db.commit()
        logger.info(f"Deleted project: {project_id}")
        return db_project
    except SQLAlchemyError as e:
        logger.error(f"Error deleting project: {str(e)} \
# @@==>> SSHInteractiveSession End-of-Command  <<==@@
