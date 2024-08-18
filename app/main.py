
# This module contains the main FastAPI application and route definitions.

from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from . import models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post('/projects/', response_model=schemas.Project)
def create_project(project: schemas.ProjectCreate, db: Session = Depends(get_db)):
    try:
        db_project = models.Project(**project.dict())
        db.add(db_project)
        db.commit()
        db.refresh(db_project)
        return db_project
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Project with this name already exists")
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


@app.get('/projects/', response_model=list[schemas.Project])
def read_projects(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    try:
        projects = db.query(models.Project).offset(skip).limit(limit).all()
        return projects
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

@app.get('/projects/{project_id}', response_model=schemas.Project)
def read_project(project_id: int, db: Session = Depends(get_db)):
    db_project = db.query(models.Project).filter(models.Project.id == project_id).first()
    if db_project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    return db_project

@app.put('/projects/{project_id}', response_model=schemas.Project)
def update_project(project_id: int, project: schemas.ProjectUpdate, db: Session = Depends(get_db)):
    try:
        db_project = db.query(models.Project).filter(models.Project.id == project_id).first()
        if db_project is None:
            raise HTTPException(status_code=404, detail="Project not found")
        for key, value in project.dict(exclude_unset=True).items():
            setattr(db_project, key, value)
        db.commit()
        db.refresh(db_project)
        return db_project
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Project with this name already exists")
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

@app.delete('/projects/{project_id}', response_model=schemas.Project)
def delete_project(project_id: int, db: Session = Depends(get_db)):
    try:
        db_project = db.query(models.Project).filter(models.Project.id == project_id).first()
        if db_project is None:
            raise HTTPException(status_code=404, detail="Project not found")
        db.delete(db_project)
        db.commit()
        return db_project
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

