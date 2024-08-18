import requests
import json

BASE_URL = 'http://localhost:8000'  # Adjust if your server is running on a different port

def test_project_crud():
    # Create a project
    create_response = requests.post(f'{BASE_URL}/projects/', json={
        'name': 'Test Project',
        'description': 'This is a test project'
    })
    assert create_response.status_code == 200
    project_id = create_response.json()['id']
    print(f'Created project with id: {project_id}')

    # Read the project
    read_response = requests.get(f'{BASE_URL}/projects/{project_id}')
    assert read_response.status_code == 200
    assert read_response.json()['name'] == 'Test Project'
    print('Read project successfully')

    # Update the project
    update_response = requests.put(f'{BASE_URL}/projects/{project_id}', json={
        'name': 'Updated Test Project',
        'description': 'This is an updated test project'
    })
    assert update_response.status_code == 200
    assert update_response.json()['name'] == 'Updated Test Project'
    print('Updated project successfully')

    # Delete the project
    delete_response = requests.delete(f'{BASE_URL}/projects/{project_id}')
    assert delete_response.status_code == 200
    print('Deleted project successfully')

def test_task_crud():
    # Create a task
    create_response = requests.post(f'{BASE_URL}/tasks/', json={
        'title': 'Test Task',
        'description': 'This is a test task',
        'status': 'In Progress',
        'priority': 'High',
        'project_id': 1  # Assuming a project with id 1 exists
    })
    assert create_response.status_code == 200
    task_id = create_response.json()['id']
    print(f'Created task with id: {task_id}')

    # Read the task
    read_response = requests.get(f'{BASE_URL}/tasks/{task_id}')
    assert read_response.status_code == 200
    assert read_response.json()['title'] == 'Test Task'
    print('Read task successfully')

    # Update the task
    update_response = requests.put(f'{BASE_URL}/tasks/{task_id}', json={
        'title': 'Updated Test Task',
        'description': 'This is an updated test task',
        'status': 'Completed',
        'priority': 'Medium',
        'project_id': 1
    })
    assert update_response.status_code == 200
    assert update_response.json()['title'] == 'Updated Test Task'
    print('Updated task successfully')

    # Delete the task
    delete_response = requests.delete(f'{BASE_URL}/tasks/{task_id}')
    assert delete_response.status_code == 200
    print('Deleted task successfully')

if __name__ == '__main__':
    print('Testing Project CRUD operations:')
    test_project_crud()
    print('
Testing Task CRUD operations:')
    test_task_crud()

print('All tests completed successfully')
EOL # @@==>> SSHInteractiveSession End-of-Command  <<==@@
uvicorn main:app --host 0.0.0.0 --port 8000 & # @@==>> SSHInteractiveSession End-of-Command  <<==@@
curl http://localhost:8000 # @@==>> SSHInteractiveSession End-of-Command  <<==@@
ps aux | grep uvicorn # @@==>> SSHInteractiveSession End-of-Command  <<==@@
cat > /root/status.txt << EOL
Current Status:

1. Progress:
   - Installed 'requests' library for API testing
   - Created test_api.py with CRUD test functions for Project and Task entities
   - Attempted to start the FastAPI server using uvicorn (status unknown)

2. Issues:
   - Unable to confirm if the FastAPI server is running
   - Curl request to localhost:8000 did not return any response

3. Next Steps:
   - Verify if the FastAPI server is running correctly
   - Check server logs for any startup errors
   - Ensure the server is accessible on localhost:8000
   - Run the test_api.py script to test API endpoints
   - Debug any issues that arise during testing

4. To-Do:
   - Implement test functions for other entities (Issue, DesignRule, Requirement, ProjectGoal, SBOM)
   - Add error handling and more detailed assertions to test functions
   - Consider adding integration tests for entity relationships

5. Long-term Goals:
   - Implement authentication and authorization
   - Add advanced queries (filtering, sorting)
   - Develop a comprehensive test suite
   - Set up continuous integration for automated testing

Next session should focus on verifying the server status, running the tests, and addressing any issues that come up during testing.
