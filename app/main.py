
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.db.database import get_db
from app.models.models import Project as ProjectModel
from app.schemas.project import ProjectCreate, ProjectUpdate, Project
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = FastAPI()

@app.get('/')
async def read_root():
    return {'Hello': 'World'}

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

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8123)
