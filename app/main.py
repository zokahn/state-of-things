import logging
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from .models.models import Project as ProjectModel
from .schemas.project import Project, ProjectCreate
from .db.database import SessionLocal, engine, Base

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/api/v1/projects/", response_model=Project)
def create_project(project: ProjectCreate, db: Session = Depends(get_db)):
    logger.info(f"Attempting to create project: {project}")
    db_project = ProjectModel(**project.dict())
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    logger.info(f"Project created: {db_project}")
    return db_project

@app.get("/api/v1/projects/", response_model=list[Project])
def read_projects(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    logger.info(f"Attempting to read projects. skip: {skip}, limit: {limit}")
    projects = db.query(ProjectModel).offset(skip).limit(limit).all()
    logger.info(f"Projects retrieved: {projects}")
    return projects

@app.get("/")
def read_root():
    logger.info("Root endpoint accessed")
    return {"Hello": "World"}
