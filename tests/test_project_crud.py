import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


import os
import sys
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import Base
from app.main import app, get_db
from app import crud, schemas

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


def create_test_user(db):
    user = schemas.UserCreate(email='test@example.com', username='testuser', password='testpassword')
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        return db_user
    db_user = crud.create_user(db=db, user=user)
    db.commit()
    return db_user

@pytest.fixture(scope="function")
def test_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    print("Database tables dropped and recreated.")
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)

def get_token(client):
    response = client.post('/token', data={'username': 'test@example.com', 'password': 'testpassword'})
    if response.status_code != 200:
        raise Exception(f'Failed to get token: {response.status_code} {response.text}')
    return response.json()['access_token']


def test_create_project(test_db):
    print('Starting test_create_project')
    create_test_user(test_db)
    token = get_token(client)
    print(f'Token received: {token}')
    headers = {'Authorization': f'Bearer {token}'}
    project_data = {'name': 'Test Project', 'description': 'This is a test project'}
    response = client.post('/projects/', json=project_data, headers=headers)
    print(f'Create project response status: {response.status_code}')
    print(f'Create project response content: {response.content}')
    assert response.status_code == 200, f'Failed to create project: {response.content}'
    created_project = response.json()
    assert 'id' in created_project, f'Created project does not have an id: {created_project}'
    assert created_project['name'] == project_data['name'], f'Project name mismatch: {created_project["name"]} != {project_data["name"]}'
    assert created_project['description'] == project_data['description'], f'Project description mismatch: {created_project["description"]} != {project_data["description"]}'
    print('test_create_project completed successfully')


def test_read_project(test_db):
    create_test_user(test_db)
    token = get_token(client)
    headers = {"Authorization": f"Bearer {token}"}
    project_data = {"name": "Test Project", "description": "This is a test project"}
    create_response = client.post("/projects/", json=project_data, headers=headers)
    created_project = create_response.json()

    response = client.get(f"/projects/{created_project['id']}", headers=headers)
    assert response.status_code == 200
    project = response.json()
    assert project["id"] == created_project["id"]
    assert project["name"] == project_data["name"]
    assert project["description"] == project_data["description"]


def test_update_project(test_db):
    create_test_user(test_db)
    token = get_token(client)
    headers = {"Authorization": f"Bearer {token}"}
    project_data = {"name": "Test Project", "description": "This is a test project"}
    create_response = client.post("/projects/", json=project_data, headers=headers)
    created_project = create_response.json()

    updated_data = {"name": "Updated Project", "description": "This is an updated project"}
    response = client.put(f"/projects/{created_project['id']}", json=updated_data, headers=headers)
    assert response.status_code == 200
    updated_project = response.json()
    assert updated_project["id"] == created_project["id"]
    assert updated_project["name"] == updated_data["name"]
    assert updated_project["description"] == updated_data["description"]


def test_delete_project(test_db):
    create_test_user(test_db)
    token = get_token(client)
    headers = {"Authorization": f"Bearer {token}"}
    project_data = {"name": "Test Project", "description": "This is a test project"}
    create_response = client.post("/projects/", json=project_data, headers=headers)
    created_project = create_response.json()

    response = client.delete(f"/projects/{created_project['id']}", headers=headers)
    assert response.status_code == 200
    assert response.json()["message"] == "Project deleted successfully"

    # Verify the project is deleted
    get_response = client.get(f"/projects/{created_project['id']}", headers=headers)
    assert get_response.status_code == 404
