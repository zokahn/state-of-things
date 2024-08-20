import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_project():
    response = client.post(
        "/projects/",
        json={"name": "Test Project", "description": "A test project"}
    )
    assert response.status_code == 200
    assert response.json()["name"] == "Test Project"

def test_read_projects():
    response = client.get("/projects/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_create_task():
    response = client.post(
        "/tasks/",
        json={"title": "Test Task", "description": "A test task", "project_id": 1}
    )
    assert response.status_code == 200
    assert response.json()["title"] == "Test Task"

def test_read_tasks():
    response = client.get("/tasks/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_create_issue():
    response = client.post(
        "/issues/",
        json={"title": "Test Issue", "description": "A test issue", "project_id": 1}
    )
    assert response.status_code == 200
    assert response.json()["title"] == "Test Issue"

def test_read_issues():
    response = client.get("/issues/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)