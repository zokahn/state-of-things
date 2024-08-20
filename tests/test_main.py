
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database import Base, get_db
from app import crud, models, schemas
import pytest

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

@pytest.fixture(scope="module")
def test_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

def test_create_user(test_db):
    response = client.post(
        "/users/",
        json={"email": "test@example.com", "password": "testpassword"}
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["email"] == "test@example.com"
    assert "id" in data

def test_create_user_duplicate_email(test_db):
    response = client.post(
        "/users/",
        json={"email": "test@example.com", "password": "testpassword"}
    )
    assert response.status_code == 400, response.text
    assert response.json()["detail"] == "Email already registered"

def test_read_users(test_db):
    response = client.get("/users/")
    assert response.status_code == 200, response.text
    data = response.json()
    assert len(data) > 0

def test_create_project(test_db):
    # First, create a user
    user_response = client.post(
        "/users/",
        json={"email": "project_test@example.com", "password": "testpassword"}
    )
    user_data = user_response.json()
    
    # Now create a project for this user
    response = client.post(
        "/projects/",
        json={"name": "Test Project", "description": "This is a test project"},
        headers={"X-User-ID": str(user_data["id"])}
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["name"] == "Test Project"
    assert data["description"] == "This is a test project"
    assert "id" in data

def test_read_projects(test_db):
    response = client.get("/projects/")
    assert response.status_code == 200, response.text
    data = response.json()
    assert len(data) > 0

# Add more tests as needed for update and delete operations
