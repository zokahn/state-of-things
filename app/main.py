import logging\nfrom fastapi import FastAPI, Depends, HTTPException, Query\nfrom sqlalchemy.orm import Session\nfrom sqlalchemy.exc import IntegrityError\nfrom . import models, schemas\nfrom .database import SessionLocal, engine\nfrom typing import List\n\n# Configure logging\nlogging.basicConfig(\n    level=logging.INFO,\n    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',\n    filename='/root/project_notes_api/app.log'\n)\n\nlogger = logging.getLogger(__name__)\n\nmodels.Base.metadata.create_all(bind=engine)\n\napp = FastAPI()\n\ndef get_db():\n    db = SessionLocal()\n    try:\n        yield db\n    finally:\n        db.close()\n\n@app.post('/projects/', response_model=schemas.Project)\ndef create_project(project: schemas.ProjectCreate, db: Session = Depends(get_db)):\n    logger.info(f'Attempting to create project: {project.name}')\n    try:\n        db_project = models.Project(**project.dict())\n        db.add(db_project)\n        db.commit()\n        db.refresh(db_project)\n        logger.info(f'Project created successfully: {db_project.id}')\n        return db_project\n    except IntegrityError:\n        logger.error(f'IntegrityError: Project with name {project.name} already exists')\n        db.rollback()\n        raise HTTPException(status_code=400, detail=\"Project with this name already exists\")\n    except Exception as e:\n        logger.error(f'Unexpected error in create_project: {str(e)}')\n        db.rollback()\n        raise HTTPException(status_code=500, detail=f\"An unexpected error occurred\")\n\n
@app.put("/projects/{project_id}", response_model=schemas.Project)
def update_project(project_id: int, project: schemas.ProjectUpdate, db: Session = Depends(get_db)):
    logger.info("Attempting to update project: " + str(project_id))
    try:
        db_project = db.query(models.Project).filter(models.Project.id == project_id).first()
        if db_project is None:
            logger.warning("Project with id " + str(project_id) + " not found")
            raise HTTPException(status_code=404, detail="Project not found")
        for key, value in project.dict(exclude_unset=True).items():
            setattr(db_project, key, value)
        db.commit()
        db.refresh(db_project)
        logger.info("Successfully updated project: " + str(db_project.id))
        return db_project
    except IntegrityError:
        logger.error("IntegrityError: Project update failed")
        db.rollback()
        raise HTTPException(status_code=400, detail="Update failed due to integrity constraint")
    except Exception as e:
        logger.error("Unexpected error in update_project: " + str(e))
        db.rollback()
        raise HTTPException(status_code=500, detail="An unexpected error occurred")

@app.delete("/projects/{project_id}", response_model=schemas.ProjectDelete)
def delete_project(project_id: int, db: Session = Depends(get_db)):
    logger.info("Attempting to delete project: " + str(project_id))
    db_project = db.query(models.Project).filter(models.Project.id == project_id).first()
    if db_project is None:
        logger.warning("Project with id " + str(project_id) + " not found")
        raise HTTPException(status_code=404, detail="Project not found")
    try:
        db.delete(db_project)
        db.commit()
        logger.info("Successfully deleted project: " + str(project_id))
        return {"message": "Project " + str(project_id) + " has been deleted"}
    except Exception as e:
        logger.error("Unexpected error in delete_project: " + str(e))
        db.rollback()
        raise HTTPException(status_code=500, detail="An unexpected error occurred")

@app.get('/projects/', response_model=List[schemas.Project])
def read_projects(skip: int = Query(0, ge=0), limit: int = Query(100, ge=1, le=1000), db: Session = Depends(get_db)):
    logger.info(f'Fetching projects with skip={skip} and limit={limit}')
    try:
        projects = db.query(models.Project).offset(skip).limit(limit).all()
        logger.info(f'Successfully fetched {len(projects)} projects')
        return projects
    except Exception as e:
        logger.error(f'Error in read_projects: {str(e)}')
        raise HTTPException(status_code=500, detail="An error occurred while fetching projects")

@app.get('/projects/{project_id}', response_model=schemas.Project)
def read_project(project_id: int, db: Session = Depends(get_db)):
    logger.info(f'Fetching project with id: {project_id}')
    db_project = db.query(models.Project).filter(models.Project.id == project_id).first()
    if db_project is None:
        logger.warning(f'Project with id {project_id} not found')
        raise HTTPException(status_code=404, detail="Project not found")
    logger.info(f'Successfully fetched project: {db_project.id}')
    return db_project
