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

