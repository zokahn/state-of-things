# Project Notes Management API

This project implements an API for managing project notes, including features for creating and listing projects, changelogs, requirements, and recurring problems.

## Features

- Create, list, and update projects
- Add and list changelogs for projects
- Add and list requirements for projects
- Add and list recurring problems for projects
- Get project categories with counts of changelogs, requirements, and recurring problems

## Project Structure

- `/root/project_notes_api/`: Main API implementation
- `/root/project_notes_api/tests/`: Test files for the API
- `/root/scripts/project_notes_client.py`: Companion script to interact with the API

## Setup and Installation

1. Clone the repository
2. Install dependencies:
   ```
   pip install fastapi sqlalchemy httpx requests
   ```
3. Run the API:
   ```
   uvicorn main:app --reload
   ```

## Testing

Run tests using pytest:

```
python -m pytest tests/
```

## TODO

- Debug and fix failing tests
- Implement error handling and input validation
- Set up continuous integration
- Create comprehensive documentation
- Add more features (e.g., search functionality, data export)



## Next Steps
1. Complete API Endpoint Testing
2. Perform Log Analysis
3. Resolve ASGI App Loading Error
4. Check Database Connection
5. Update API Documentation
6. Implement Remaining CRUD Operations
7. Begin Authentication Implementation
8. Implement Error Handling and Data Validation
9. Conduct Code Review and Refactoring
10. Plan for Front-end Development

## Companion Script

A companion script has been added to interact with the Project Management API. It provides two modes: read and write.

### Usage:
```
python /root/companion_script.py [mode] --url [API_URL] --token [API_TOKEN] --project [PROJECT_ID]
```

Where:
- [mode] is either 'read' or 'write'
- [API_URL] is the base URL of the Project Management API
- [API_TOKEN] is the authentication token for the API
- [PROJECT_ID] is the identifier of the project to interact with

Example usage:
```
python /root/companion_script.py read --url http://api.example.com --token abc123 --project proj001
python /root/companion_script.py write --url http://api.example.com --token abc123 --project proj001
```


## Companion Script

A companion script has been added to interact with the Project Management API. It provides two modes: read and write.

### Usage:
```
python companion_script.py [mode] --url [API_URL] --token [API_TOKEN] --project [PROJECT_ID]
```

Where:
- [mode] is either 'read' or 'write'
- [API_URL] is the base URL of the Project Management API
- [API_TOKEN] is the authentication token for the API
- [PROJECT_ID] is the identifier of the project to interact with

Example usage:
```
python companion_script.py read --url http://api.example.com --token abc123 --project proj001
python companion_script.py write --url http://api.example.com --token abc123 --project proj001
```

