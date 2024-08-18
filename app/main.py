
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.db.database import get_db
from app.models.models import (
    Task as TaskModel,
    Issue as IssueModel,
    DesignRule as DesignRuleModel,
    Requirement as RequirementModel,
    ProjectGoal as ProjectGoalModel,
    SBOM as SBOMModel,
    Project as ProjectModel
)
from app.schemas.models import (
    TaskCreate, TaskUpdate, Task,
    IssueCreate, IssueUpdate, Issue,
    DesignRuleCreate, DesignRuleUpdate, DesignRule,
    RequirementCreate, RequirementUpdate, Requirement,
    ProjectGoalCreate, ProjectGoalUpdate, ProjectGoal,
    SBOMCreate, SBOMUpdate, SBOM,
    ProjectCreate, ProjectUpdate, Project
)
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = FastAPI()

@app.get('/')
async def read_root():
    return {'Hello': 'World'}

@app.post('/api/v1/tasks/', response_model=Task)
async def create_task(task: TaskCreate, db: AsyncSession = Depends(get_db)):
    try:
        db_task = TaskModel(**task.dict())
        db.add(db_task)
        await db.commit()
        await db.refresh(db_task)
        return db_task
    except Exception as e:
        logger.error(f'Error creating task: {str(e)}')
        raise HTTPException(status_code=500, detail=str(e))

@app.get('/api/v1/tasks/', response_model=list[Task])
async def read_tasks(db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(select(TaskModel))
        tasks = result.scalars().all()
        return tasks
    except Exception as e:
        logger.error(f'Error listing tasks: {str(e)}')
        raise HTTPException(status_code=500, detail=str(e))

@app.get('/api/v1/tasks/{task_id}', response_model=Task)
async def read_task(task_id: int, db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(select(TaskModel).filter(TaskModel.id == task_id))
        task = result.scalar_one_or_none()
        if task is None:
            raise HTTPException(status_code=404, detail='Task not found')
        return task
    except Exception as e:
        logger.error(f'Error reading task: {str(e)}')
        raise HTTPException(status_code=500, detail=str(e))

@app.put('/api/v1/tasks/{task_id}', response_model=Task)
async def update_task(task_id: int, task: TaskUpdate, db: AsyncSession = Depends(get_db)):
    try:
        async with db.begin():
            db_task = await db.get(TaskModel, task_id)
            if db_task is None:
                raise HTTPException(status_code=404, detail='Task not found')
            update_data = task.dict(exclude_unset=True)
            for key, value in update_data.items():
                setattr(db_task, key, value)
            await db.commit()
            await db.refresh(db_task)
        return db_task
    except Exception as e:
        logger.error(f'Error updating task: {str(e)}')
        raise HTTPException(status_code=500, detail=str(e))

# Issue routes
@app.post('/api/v1/issues/', response_model=Issue)
async def create_issue(issue: IssueCreate, db: AsyncSession = Depends(get_db)):
    try:
        db_issue = IssueModel(**issue.dict())
        db.add(db_issue)
        await db.commit()
        await db.refresh(db_issue)
        return db_issue
    except Exception as e:
        logger.error(f'Error creating issue: {str(e)}')
        raise HTTPException(status_code=500, detail=str(e))

@app.get('/api/v1/issues/', response_model=list[Issue])
async def read_issues(db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(select(IssueModel))
        issues = result.scalars().all()
        return issues
    except Exception as e:
        logger.error(f'Error listing issues: {str(e)}')
        raise HTTPException(status_code=500, detail=str(e))

@app.get('/api/v1/issues/{issue_id}', response_model=Issue)
async def read_issue(issue_id: int, db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(select(IssueModel).filter(IssueModel.id == issue_id))
        issue = result.scalar_one_or_none()
        if issue is None:
            raise HTTPException(status_code=404, detail='Issue not found')
        return issue
    except Exception as e:
        logger.error(f'Error reading issue: {str(e)}')
        raise HTTPException(status_code=500, detail=str(e))

@app.put('/api/v1/issues/{issue_id}', response_model=Issue)
async def update_issue(issue_id: int, issue: IssueUpdate, db: AsyncSession = Depends(get_db)):
    try:
        async with db.begin():
            db_issue = await db.get(IssueModel, issue_id)
            if db_issue is None:
                raise HTTPException(status_code=404, detail='Issue not found')
            update_data = issue.dict(exclude_unset=True)
            for key, value in update_data.items():
                setattr(db_issue, key, value)
            await db.commit()
            await db.refresh(db_issue)
        return db_issue
    except Exception as e:
        logger.error(f'Error updating issue: {str(e)}')
        raise HTTPException(status_code=500, detail=str(e))

# DesignRule routes
@app.post('/api/v1/design_rules/', response_model=DesignRule)
async def create_design_rule(design_rule: DesignRuleCreate, db: AsyncSession = Depends(get_db)):
    try:
        db_design_rule = DesignRuleModel(**design_rule.dict())
        db.add(db_design_rule)
        await db.commit()
        await db.refresh(db_design_rule)
        return db_design_rule
    except Exception as e:
        logger.error(f'Error creating design rule: {str(e)}')
        raise HTTPException(status_code=500, detail=str(e))

@app.get('/api/v1/design_rules/', response_model=list[DesignRule])
async def read_design_rules(db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(select(DesignRuleModel))
        design_rules = result.scalars().all()
        return design_rules
    except Exception as e:
        logger.error(f'Error listing design rules: {str(e)}')
        raise HTTPException(status_code=500, detail=str(e))

@app.get('/api/v1/design_rules/{design_rule_id}', response_model=DesignRule)
async def read_design_rule(design_rule_id: int, db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(select(DesignRuleModel).filter(DesignRuleModel.id == design_rule_id))
        design_rule = result.scalar_one_or_none()
        if design_rule is None:
            raise HTTPException(status_code=404, detail='Design rule not found')
        return design_rule
    except Exception as e:
        logger.error(f'Error reading design rule: {str(e)}')
        raise HTTPException(status_code=500, detail=str(e))

@app.put('/api/v1/design_rules/{design_rule_id}', response_model=DesignRule)
async def update_design_rule(design_rule_id: int, design_rule: DesignRuleUpdate, db: AsyncSession = Depends(get_db)):
    try:
        async with db.begin():
            db_design_rule = await db.get(DesignRuleModel, design_rule_id)
            if db_design_rule is None:
                raise HTTPException(status_code=404, detail='Design rule not found')
            update_data = design_rule.dict(exclude_unset=True)
            for key, value in update_data.items():
                setattr(db_design_rule, key, value)
            await db.commit()
            await db.refresh(db_design_rule)
        return db_design_rule
    except Exception as e:
        logger.error(f'Error updating design rule: {str(e)}')
        raise HTTPException(status_code=500, detail=str(e))

# Requirement routes
@app.post('/api/v1/requirements/', response_model=Requirement)
async def create_requirement(requirement: RequirementCreate, db: AsyncSession = Depends(get_db)):
    try:
        db_requirement = RequirementModel(**requirement.dict())
        db.add(db_requirement)
        await db.commit()
        await db.refresh(db_requirement)
        return db_requirement
    except Exception as e:
        logger.error(f'Error creating requirement: {str(e)}')
        raise HTTPException(status_code=500, detail=str(e))

@app.get('/api/v1/requirements/', response_model=list[Requirement])
async def read_requirements(db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(select(RequirementModel))
        requirements = result.scalars().all()
        return requirements
    except Exception as e:
        logger.error(f'Error listing requirements: {str(e)}')
        raise HTTPException(status_code=500, detail=str(e))

@app.get('/api/v1/requirements/{requirement_id}', response_model=Requirement)
async def read_requirement(requirement_id: int, db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(select(RequirementModel).filter(RequirementModel.id == requirement_id))
        requirement = result.scalar_one_or_none()
        if requirement is None:
            raise HTTPException(status_code=404, detail='Requirement not found')
        return requirement
    except Exception as e:
        logger.error(f'Error reading requirement: {str(e)}')
        raise HTTPException(status_code=500, detail=str(e))

@app.put('/api/v1/requirements/{requirement_id}', response_model=Requirement)
async def update_requirement(requirement_id: int, requirement: RequirementUpdate, db: AsyncSession = Depends(get_db)):
    try:
        async with db.begin():
            db_requirement = await db.get(RequirementModel, requirement_id)
            if db_requirement is None:
                raise HTTPException(status_code=404, detail='Requirement not found')
            update_data = requirement.dict(exclude_unset=True)
            for key, value in update_data.items():
                setattr(db_requirement, key, value)
            await db.commit()
            await db.refresh(db_requirement)
        return db_requirement
    except Exception as e:
        logger.error(f'Error updating requirement: {str(e)}')
        raise HTTPException(status_code=500, detail=str(e))

# ProjectGoal routes
@app.post('/api/v1/project_goals/', response_model=ProjectGoal)
async def create_project_goal(project_goal: ProjectGoalCreate, db: AsyncSession = Depends(get_db)):
    try:
        db_project_goal = ProjectGoalModel(**project_goal.dict())
        db.add(db_project_goal)
        await db.commit()
        await db.refresh(db_project_goal)
        return db_project_goal
    except Exception as e:
        logger.error(f'Error creating project goal: {str(e)}')
        raise HTTPException(status_code=500, detail=str(e))

@app.get('/api/v1/project_goals/', response_model=list[ProjectGoal])
async def read_project_goals(db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(select(ProjectGoalModel))
        project_goals = result.scalars().all()
        return project_goals
    except Exception as e:
        logger.error(f'Error listing project goals: {str(e)}')
        raise HTTPException(status_code=500, detail=str(e))

@app.get('/api/v1/project_goals/{project_goal_id}', response_model=ProjectGoal)
async def read_project_goal(project_goal_id: int, db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(select(ProjectGoalModel).filter(ProjectGoalModel.id == project_goal_id))
        project_goal = result.scalar_one_or_none()
        if project_goal is None:
            raise HTTPException(status_code=404, detail='Project goal not found')
        return project_goal
    except Exception as e:
        logger.error(f'Error reading project goal: {str(e)}')
        raise HTTPException(status_code=500, detail=str(e))

@app.put('/api/v1/project_goals/{project_goal_id}', response_model=ProjectGoal)
async def update_project_goal(project_goal_id: int, project_goal: ProjectGoalUpdate, db: AsyncSession = Depends(get_db)):
    try:
        async with db.begin():
            db_project_goal = await db.get(ProjectGoalModel, project_goal_id)
            if db_project_goal is None:
                raise HTTPException(status_code=404, detail='Project goal not found')
            update_data = project_goal.dict(exclude_unset=True)
            for key, value in update_data.items():
                setattr(db_project_goal, key, value)
            await db.commit()
            await db.refresh(db_project_goal)
        return db_project_goal
    except Exception as e:
        logger.error(f'Error updating project goal: {str(e)}')
        raise HTTPException(status_code=500, detail=str(e))

# SBOM routes
@app.post('/api/v1/sbom/', response_model=SBOM)
async def create_sbom_entry(sbom: SBOMCreate, db: AsyncSession = Depends(get_db)):
    try:
        db_sbom = SBOMModel(**sbom.dict())
        db.add(db_sbom)
        await db.commit()
        await db.refresh(db_sbom)
        return db_sbom
    except Exception as e:
        logger.error(f'Error creating SBOM entry: {str(e)}')
        raise HTTPException(status_code=500, detail=str(e))

@app.get('/api/v1/sbom/', response_model=list[SBOM])
async def read_sbom_entries(db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(select(SBOMModel))
        sbom_entries = result.scalars().all()
        return sbom_entries
    except Exception as e:
        logger.error(f'Error listing SBOM entries: {str(e)}')
        raise HTTPException(status_code=500, detail=str(e))

@app.get('/api/v1/sbom/{sbom_id}', response_model=SBOM)
async def read_sbom_entry(sbom_id: int, db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(select(SBOMModel).filter(SBOMModel.id == sbom_id))
        sbom_entry = result.scalar_one_or_none()
        if sbom_entry is None:
            raise HTTPException(status_code=404, detail='SBOM entry not found')
        return sbom_entry
    except Exception as e:
        logger.error(f'Error reading SBOM entry: {str(e)}')
        raise HTTPException(status_code=500, detail=str(e))

@app.put('/api/v1/sbom/{sbom_id}', response_model=SBOM)
async def update_sbom_entry(sbom_id: int, sbom: SBOMUpdate, db: AsyncSession = Depends(get_db)):
    try:
        async with db.begin():
            db_sbom = await db.get(SBOMModel, sbom_id)
            if db_sbom is None:
                raise HTTPException(status_code=404, detail='SBOM entry not found')
            update_data = sbom.dict(exclude_unset=True)
            for key, value in update_data.items():
                setattr(db_sbom, key, value)
            await db.commit()
            await db.refresh(db_sbom)
        return db_sbom
    except Exception as e:
        logger.error(f'Error updating SBOM entry: {str(e)}')
        raise HTTPException(status_code=500, detail=str(e))

# Project routes
@app.post('/api/v1/projects/', response_model=Project)
async def create_project(project: ProjectCreate, db: AsyncSession = Depends(get_db)):
    try:
        db_project = ProjectModel(**project.dict())
        db.add(db_project)
        await db.commit()
        await db.refresh(db_project)
        return db_project
    except Exception as e:
        logger.error(f'Error creating project: {str(e)}')
        raise HTTPException(status_code=500, detail=str(e))

@app.get('/api/v1/projects/', response_model=list[Project])
async def read_projects(db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(select(ProjectModel))
        projects = result.scalars().all()
        return projects
    except Exception as e:
        logger.error(f'Error listing projects: {str(e)}')
        raise HTTPException(status_code=500, detail=str(e))

@app.get('/api/v1/projects/{project_id}', response_model=Project)
async def read_project(project_id: int, db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(select(ProjectModel).filter(ProjectModel.id == project_id))
        project = result.scalar_one_or_none()
        if project is None:
            raise HTTPException(status_code=404, detail='Project not found')
        return project
    except Exception as e:
        logger.error(f'Error reading project: {str(e)}')
        raise HTTPException(status_code=500, detail=str(e))

@app.put('/api/v1/projects/{project_id}', response_model=Project)
async def update_project(project_id: int, project: ProjectUpdate, db: AsyncSession = Depends(get_db)):
    try:
        async with db.begin():
            db_project = await db.get(ProjectModel, project_id)
            if db_project is None:
                raise HTTPException(status_code=404, detail='Project not found')
            update_data = project.dict(exclude_unset=True)
            for key, value in update_data.items():
                setattr(db_project, key, value)
            await db.commit()
            await db.refresh(db_project)
        return db_project
    except Exception as e:
        logger.error(f'Error updating project: {str(e)}')
        raise HTTPException(status_code=500, detail=str(e))

# Additional route to get all related entities for a project
@app.get('/api/v1/projects/{project_id}/full', response_model=ProjectFull)
async def read_project_full(project_id: int, db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(
            select(ProjectModel)
            .options(
                selectinload(ProjectModel.tasks),
                selectinload(ProjectModel.issues),
                selectinload(ProjectModel.design_rules),
                selectinload(ProjectModel.requirements),
                selectinload(ProjectModel.project_goals),
                selectinload(ProjectModel.sbom_entries)
            )
            .filter(ProjectModel.id == project_id)
        )
        project = result.scalar_one_or_none()
        if project is None:
            raise HTTPException(status_code=404, detail='Project not found')
        return project
    except Exception as e:
        logger.error(f'Error reading full project details: {str(e)}')
        raise HTTPException(status_code=500, detail=str(e))

# Add this at the end of the file to create tables
@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

print("API setup complete. Run the server with 'uvicorn main:app --reload'")
