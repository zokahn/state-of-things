
# Project Notes API

This is a FastAPI-based RESTful API for managing project notes.

## Features

- User authentication
- CRUD operations for projects, tasks, issues, design rules, requirements, project goals, and SBOMs
- SQLite database
- Comprehensive error handling and logging
- Unit tests

## Recent Updates (as of 2024-08-19)

1. Error Handling and Logging:
   - Implemented comprehensive error handling for all routes.
   - Added a log_input_validation decorator to log input data for all routes.
   - Implemented try-except blocks to catch and handle different types of errors.
   - Added appropriate logging statements for successful operations, warnings, and errors.

2. Documentation:
   - Updated README with information about the new error handling and logging implementation.

3. Project Status:
   - All routes now have proper error handling and logging.
   - The API is more robust and easier to debug due to improved error handling and logging.

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

## Next Steps

1. Test all implemented routes to ensure they're working correctly with the new error handling.
2. Update and expand test coverage to include error scenarios.
3. Implement relationships between entities (e.g., Tasks belonging to Projects).
4. Create a basic front-end interface to interact with the API.
5. Add authentication and authorization.
6. Implement advanced queries (e.g., filtering, sorting).

## Future Goals

### Mid-term Goals

- Optimize database queries and API performance.
- Implement additional features like task assignment and project status updates.
- Develop a comprehensive test suite.

### Long-term Goals

- Add advanced features like reporting and analytics.
- Deploy the application to a production environment.
- Implement continuous integration and deployment (CI/CD) pipeline.
- Implement advanced security features.
- Develop a mobile application for the API.
- Integrate with popular project management tools.

For more detailed information about the project's features and immediate tasks, please refer to the state-of-things.txt file.
