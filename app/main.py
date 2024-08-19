from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from . import crud, models, schemas
from .database import SessionLocal, engine
import logging

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

# Project endpoints (existing code)
@app.post("/projects/", response_model=schemas.Project)
def create_project(project: schemas.ProjectCreate, db: Session = Depends(get_db)):
    try:
        return crud.create_project(db=db, project=project)
    except Exception as e:
        logger.error(f"Error creating project: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/projects/", response_model=list[schemas.Project])
def read_projects(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    try:
        projects = crud.get_projects(db, skip=skip, limit=limit)
        return projects
    except Exception as e:
        logger.error(f"Error reading projects: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/projects/{project_id}", response_model=schemas.Project)
def read_project(project_id: int, db: Session = Depends(get_db)):
    try:
        db_project = crud.get_project(db, project_id=project_id)
        if db_project is None:
            raise HTTPException(status_code=404, detail="Project not found")
        return db_project
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error reading project: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.put("/projects/{project_id}", response_model=schemas.Project)
def update_project(project_id: int, project: schemas.ProjectUpdate, db: Session = Depends(get_db)):
    try:
        db_project = crud.update_project(db, project_id, project)
        if db_project is None:
            raise HTTPException(status_code=404, detail="Project not found")
        return db_project
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating project: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.delete("/projects/{project_id}", response_model=schemas.Project)
def delete_project(project_id: int, db: Session = Depends(get_db)):
    try:
        db_project = crud.delete_project(db, project_id)
        if db_project is None:
            raise HTTPException(status_code=404, detail="Project not found")
        return db_project
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting project: {str(e)} \
# @@==>> SSHInteractiveSession End-of-Command  <<==@@
cat << 'EOF' > /root/project_notes_api/app/main.py
from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from . import crud, models, schemas
from .database import SessionLocal, engine
import logging

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

# Project endpoints (existing code)
@app.post("/projects/", response_model=schemas.Project)
def create_project(project: schemas.ProjectCreate, db: Session = Depends(get_db)):
    try:
        return crud.create_project(db=db, project=project)
    except Exception as e:
        logger.error(f"Error creating project: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/projects/", response_model=list[schemas.Project])
def read_projects(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    try:
        projects = crud.get_projects(db, skip=skip, limit=limit)
        return projects
    except Exception as e:
        logger.error(f"Error reading projects: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/projects/{project_id}", response_model=schemas.Project)
def read_project(project_id: int, db: Session = Depends(get_db)):
    try:
        db_project = crud.get_project(db, project_id=project_id)
        if db_project is None:
            raise HTTPException(status_code=404, detail="Project not found")
        return db_project
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error reading project: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.put("/projects/{project_id}", response_model=schemas.Project)
def update_project(project_id: int, project: schemas.ProjectUpdate, db: Session = Depends(get_db)):
    try:
        db_project = crud.update_project(db, project_id, project)
        if db_project is None:
            raise HTTPException(status_code=404, detail="Project not found")
        return db_project
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating project: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.delete("/projects/{project_id}", response_model=schemas.Project)
def delete_project(project_id: int, db: Session = Depends(get_db)):
    try:
        db_project = crud.delete_project(db, project_id)
        if db_project is None:
            raise HTTPException(status_code=404, detail="Project not found")
        return db_project
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting project: {str(e)} \
# @@==>> SSHInteractiveSession End-of-Command  <<==@@
cat << 'EOF' > /root/project_notes_api/app/main.py
from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from . import crud, models, schemas
from .database import SessionLocal, engine
import logging

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

# Project endpoints
@app.post("/projects/", response_model=schemas.Project)
def create_project(project: schemas.ProjectCreate, db: Session = Depends(get_db)):
    try:
        return crud.create_project(db=db, project=project)
    except Exception as e:
        logger.error(f"Error creating project: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/projects/", response_model=list[schemas.Project])
def read_projects(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    try:
        projects = crud.get_projects(db, skip=skip, limit=limit)
        return projects
    except Exception as e:
        logger.error(f"Error reading projects: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/projects/{project_id}", response_model=schemas.Project)
def read_project(project_id: int, db: Session = Depends(get_db)):
    try:
        db_project = crud.get_project(db, project_id=project_id)
        if db_project is None:
            raise HTTPException(status_code=404, detail="Project not found")
        return db_project
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error reading project: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.put("/projects/{project_id}", response_model=schemas.Project)
def update_project(project_id: int, project: schemas.ProjectUpdate, db: Session = Depends(get_db)):
    try:
        db_project = crud.update_project(db, project_id, project)
        if db_project is None:
            raise HTTPException(status_code=404, detail="Project not found")
        return db_project
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating project: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.delete("/projects/{project_id}", response_model=schemas.Project)
def delete_project(project_id: int, db: Session = Depends(get_db)):
    try:
        db_project = crud.delete_project(db, project_id)
        if db_project is None:
            raise HTTPException(status_code=404, detail="Project not found")
        return db_project
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting project: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

# Task endpoints
@app.post("/tasks/", response_model=schemas.Task)
def create_task(task: schemas.TaskCreate, db: Session = Depends(get_db)):
    try:
        return crud.create_task(db=db, task=task)
    except Exception as e:
        logger.error(f"Error creating task: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/tasks/", response_model=list[schemas.Task])
def read_tasks(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    try:
        tasks = crud.get_tasks(db, skip=skip, limit=limit)
        return tasks
    except Exception as e:
        logger.error(f"Error reading tasks: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/tasks/{task_id}", response_model=schemas.Task)
def read_task(task_id: int, db: Session = Depends(get_db)):
    try:
        db_task = crud.get_task(db, task_id=task_id)
        if db_task is None:
            raise HTTPException(status_code=404, detail="Task not found")
        return db_task
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error reading task: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.put("/tasks/{task_id}", response_model=schemas.Task)
def update_task(task_id: int, task: schemas.TaskUpdate, db: Session = Depends(get_db)):
    try:
        db_task = crud.update_task(db, task_id, task)
        if db_task is None:
            raise HTTPException(status_code=404, detail="Task not found")
        return db_task
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating task: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.delete("/tasks/{task_id}", response_model=schemas.Task)
def delete_task(task_id: int, db: Session = Depends(get_db)):
    try:
        db_task = crud.delete_task(db, task_id)
        if db_task is None:
            raise HTTPException(status_code=404, detail="Task not found")
        return db_task
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting task: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")
