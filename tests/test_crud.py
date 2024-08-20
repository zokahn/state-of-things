import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200, f"Response: {response.content}"
    assert response.json() == {"message": "Welcome to the Project Notes API"}


from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base
from app.main import app, get_db

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
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

def test_create_user():
    response = client.post(
        "/users/",
        json={"email": "test@example.com", "username": "testuser", "password": "testpassword"}
    )
    assert response.status_code == 200, f"Response: {response.content}"
    data = response.json()
    assert data["email"] == "test@example.com"
    assert "id" in data

def test_create_project():
    # First, create a user
    user_response = client.post(
        "/users/",
        json={"email": "project_test@example.com", "username": "projectuser", "password": "testpassword"}
    )
    assert user_response.status_code == 200
    user_data = user_response.json()
    
    # Login to get the access token
    login_response = client.post(
        "/token",
        data={"username": "project_test@example.com", "password": "testpassword"}
    )
    assert login_response.status_code == 200
    token_data = login_response.json()
    access_token = token_data["access_token"]
    
    # Create a project
    project_response = client.post(
        "/projects/",
        json={"title": "Test Project", "description": "This is a test project"},
        headers={"Authorization": f"Bearer {access_token}"}
    )
    assert project_response.status_code == 200
    project_data = project_response.json()
    assert project_data["title"] == "Test Project"
    assert project_data["description"] == "This is a test project"
    assert "id" in project_data