
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from main import app, get_db
from models import Base, Project

SQLALCHEMY_DATABASE_URL = "sqlite://"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the State of Things API"}

def test_create_project():
    response = client.post(
        "/projects/",
        json={"name": "Test Project", "description": "This is a test project"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Project"
    assert data["description"] == "This is a test project"
    assert "id" in data
    assert "created_at" in data
    assert "updated_at" in data

def test_list_projects():
    # Clear the database
    db = TestingSessionLocal()
    db.query(Project).delete()
    db.commit()
    
    # Create a test project
    response = client.post(
        "/projects/",
        json={"name": "Another Test Project", "description": "This is another test project"}
    )
    assert response.status_code == 200

    response = client.get("/projects/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    assert data[0]["name"] == "Another Test Project"
    assert data[0]["description"] == "This is another test project"
