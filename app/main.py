
from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from . import crud, schemas
from .models import Base
from . import models
from .database import SessionLocal, engine
import logging
import traceback

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def log_input_validation(func):
    def wrapper(*args, **kwargs):
        logger.info(f"Input validation for {func.__name__}: {kwargs}")
        return func(*args, **kwargs)
    return wrapper

# Project endpoints
@app.post('/projects/', response_model=schemas.Project)
@log_input_validation
def create_project(project: schemas.ProjectCreate, db: Session = Depends(get_db)):
    try:
        new_project = crud.create_project(db=db, project=project)
        logger.info(f"Project created successfully: {new_project.id}")
        return new_project
    except SQLAlchemyError as e:
        logger.error(f"Database error while creating project: {str(e)}")
        raise HTTPException(status_code=500, detail="Database error occurred")
    except Exception as e:
        logger.error(f"Unexpected error creating project: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get('/projects/', response_model=list[schemas.Project])
@log_input_validation
def read_projects(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    try:
        projects = crud.get_projects(db, skip=skip, limit=limit)
        logger.info(f"Retrieved {len(projects)} projects")
        return projects
    except SQLAlchemyError as e:
        logger.error(f"Database error while reading projects: {str(e)}")
        raise HTTPException(status_code=500, detail="Database error occurred")
    except Exception as e:
        logger.error(f"Unexpected error reading projects: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")
@app.get('/projects/{project_id}', response_model=schemas.Project)
@log_input_validation
def read_project(project_id: int, db: Session = Depends(get_db)):
    try:
        db_project = crud.get_project(db, project_id=project_id)
        if db_project is None:
            logger.warning(f"Project not found: {project_id}")
            raise HTTPException(status_code=404, detail="Project not found")
        logger.info(f"Retrieved project: {project_id}")
        return db_project
    except SQLAlchemyError as e:
        logger.error(f"Database error while reading project {project_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Database error occurred")
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error reading project {project_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.put('/projects/{project_id}', response_model=schemas.Project)
@log_input_validation
def update_project(project_id: int, project: schemas.ProjectUpdate, db: Session = Depends(get_db)):
    try:
        db_project = crud.update_project(db, project_id, project)
        if db_project is None:
            raise HTTPException(status_code=404, detail="Project not found")
        return db_project
    except SQLAlchemyError as e:
        logger.error(f"Database error while updating project {project_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Database error occurred")
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error updating project {project_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@app.on_event("startup")
async def startup_event():
    logger.info("Application startup...")
    try:
        # Add any startup logic here
        logger.info("Startup completed successfully")
    except Exception as e:
        logger.error(f"Error during startup: {str(e)}")
        logger.error(traceback.format_exc())
        raise

@app.delete('/projects/{project_id}', response_model=schemas.Project)
@log_input_validation
def delete_project(project_id: int, db: Session = Depends(get_db)):
    try:
        db_project = crud.delete_project(db, project_id=project_id)
        if db_project is None:
            logger.warning(f"Project not found for deletion: {project_id}")
            raise HTTPException(status_code=404, detail="Project not found")
        logger.info(f"Deleted project: {project_id}")
        return db_project
    except SQLAlchemyError as e:
        logger.error(f"Database error while deleting project {project_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Database error occurred")
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error deleting project {project_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Application shutting down...")
    try:
        # Add any shutdown logic here
        logger.info("Shutdown completed successfully")
    except Exception as e:
        logger.error(f"Error during shutdown: {str(e)}")
        logger.error(traceback.format_exc())
