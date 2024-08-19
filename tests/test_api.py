
import requests
import json

BASE_URL = 'http://localhost:8123'

def test_create_project():
    url = f"{BASE_URL}/projects/"
    data = {"name": "Test Project", "description": "This is a test project"}
    response = requests.post(url, json=data)
    assert response.status_code == 200
    project = response.json()
    assert project['name'] == "Test Project"
    return project['id']

def test_get_projects():
    url = f"{BASE_URL}/projects/"
    response = requests.get(url)
    assert response.status_code == 200
    projects = response.json()
    assert isinstance(projects, list)

def test_get_project(project_id):
    url = f"{BASE_URL}/projects/{project_id}"
    response = requests.get(url)
    assert response.status_code == 200
    project = response.json()
    assert project['id'] == project_id

def test_update_project(project_id):
    url = f"{BASE_URL}/projects/{project_id}"
    data = {"name": "Updated Test Project", "description": "This project has been updated"}
    response = requests.put(url, json=data)
    assert response.status_code == 200
    project = response.json()
    assert project['name'] == "Updated Test Project"

def test_delete_project(project_id):
    url = f"{BASE_URL}/projects/{project_id}"
    response = requests.delete(url)
    assert response.status_code == 200
    message = response.json()
    assert "deleted" in message['message']

def run_tests():
    print("Running API tests...")
    project_id = test_create_project()
    print("Create project test passed.")
    test_get_projects()
    print("Get projects test passed.")
    test_get_project(project_id)
    print("Get single project test passed.")
    test_update_project(project_id)
    print("Update project test passed.")
    test_delete_project(project_id)
    print("Delete project test passed.")
    print("All tests passed successfully!")

if __name__ == "__main__":
    run_tests()
