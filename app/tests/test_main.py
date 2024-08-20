from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_project():
    response = client.post(
        '/projects/',
        json={'name': 'Test Project', 'description': 'This is a test project'}
    )
    assert response.status_code == 200
    assert response.json()['name'] == 'Test Project'
    assert response.json()['description'] == 'This is a test project'

def test_read_projects():
    response = client.get('/projects/')
    assert response.status_code == 200
    assert isinstance(response.json(), list)