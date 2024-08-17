
from fastapi.testclient import TestClient
from main import app

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
    response = client.get("/projects/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
