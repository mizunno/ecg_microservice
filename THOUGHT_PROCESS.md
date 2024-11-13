# ECG Microservice thought process

This document describes the thought process behind the design of the ECG microservice along with information about how the current architecture was designed to be scalable and maintainable.

## Current Architecture Strengths

### Hexagonal Architecture
- The current architecture is based on hexagonal architecture.
- Clear separation between business logic and infrastructure.
- Domain logic is independent of external concerns (e.g. database technology).
- Makes the system more maintainable and adaptable to change. For example, it would be easy to switch to a different database technology.
- To add another insight, the code would only need to change in the service layer, without the need to change the API layer. Moreover, the insights computation could be moved to another service.

### Service Layer Pattern
- `ECGService` and `AuthService` classes encapsulate business logic, making the code more maintainable and testable (as we can leverage dependency injection to mock the services).
- Services act as orchestrators between the API layer and data access layer.
- Reference: 
    - `app/services/ecg_service.py`
    - `app/services/auth_service.py`

### Repository Pattern
- Abstracts database operations through ABC classes `ECGRepository` and `UserRepository`. I decided to use ABC classes instead of duck typing because I think it would be better for a production environment.
- Makes it trivial to switch between different database implementations (SQLite, PostgreSQL, etc.). The current implementation uses SQLite to keep the challenge simple, but in a production environment I would use PostgreSQL.
- Enables easy mocking for tests. As we can see in the tests, we can easily inject a mock or an in-memory implementation of the repository.
- Reference:
    - `app/adapters/database/repository.py`
    - `tests/test_ecg_service.py`
    - `tests/test_auth_service.py`

### Background Tasks
- Current implementation uses FastAPI background tasks to compute insights. The zero crossing insight is a fast computation and it would not be a problem to run it synchronously. I decided to use background tasks because it would be easier to add more computationally expensive insights in the future.
- Easily replaceable with Celery by implementing a new `CeleryBackgroundTask` class and implementing the `AbstractBackgroundTask` class. FastAPI background tasks are run in the same event loop so they are lighter than Celery tasks.
- Reference:
    - `app/adapters/tasks/tasks.py`

### Authentication
- Basic authentication implemented with clear separation of concerns. 
- Easily extensible to OAuth2 or JWT by modifying only the auth service layer.
- Reference:
    - `app/services/auth_service.py`

## Potential Improvements

The following are potential improvements to the current architecture that would make it more robust and scalable. I did not implement them because I wanted to keep the challenge simple. For a production environment, most of these would be necessary.

### Database
- Current string-based signal storage could be optimized using binary formats or specialized time-series databases.
- Consider using PostgreSQL `ARRAY` or `JSONB` type for signal data.
- Zero crossing insight is stored in the `ecgs` table. This may not be the best approach if the future insights are more complex. 
- Reference:
    - `app/adapters/database/models.py`

### Caching
- Implement caching layer for frequently accessed ECGs.
- Redis could be integrated using the repository pattern with a local or remote cache.

### Config Management
- Use a configuration management system like `pydantic-settings` to manage configuration. Instead of hardcoding values in the `app/core/config.py` file, we can use environment variables or a configuration file.
- Reference:
    - `app/core/config.py`

### API Documentation
- Include examples for all endpoints. Although FastAPI automatically generates interactive API documentation, it is always a good idea to include examples.

### Monitoring
- Add logging and metrics collection. This can be done using the `logging` package and implementing a custom logging handler.
- Implement health check endpoints.
- Implement tracing.

### Security
- Add rate limiting for API endpoints. 
- Consider using OAuth2 with refresh tokens or an external authentication service (e.g. Auth0, Cognito, Keycloak, etc.).

### Testing
- Add more tests.
- Add performance tests.
