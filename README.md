
# Project Notes API

This is a FastAPI-based RESTful API for managing project notes.

## Features

- User authentication
- CRUD operations for projects
- SQLite database
- Unit tests

## Setup

1. Clone the repository
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Run the application:
   ```
   uvicorn app.main:app --reload
   ```

## Running Tests

To run the tests, use the following command:

```
pytest
```

## API Documentation

Once the application is running, you can access the API documentation at:

```
http://localhost:8000/docs
```

## CI/CD

This project uses GitHub Actions for continuous integration. On each push to the main branch, the tests are automatically run.

