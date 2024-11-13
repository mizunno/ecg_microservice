# ECG Microservice

This repository contains my solution for the backend challenge. The ECG microservice is a FastAPI-based microservice for processing and storing ECG data with user authentication. Is not a production ready application, but a proof of concept. Nonetheless, the code could be deployed in a production environment with some adjustments.

For detailed architectural decisions and future improvements, see [THOUGHT_PROCESS.md](THOUGHT_PROCESS.md).

## Features

- ECG signal processing and storage
- User authentication and authorization. For testing purposes, a default admin user is created with username `admin` and password `adminpass`.
- Asynchronous computation of ECG insights
- Role-based access control (User/Admin)
- RESTful API endpoints
- Hexagonal architecture and clean code

## Architecture

The project follows a hexagonal architecture pattern with clear separation of concerns:

- **Services**: Business logic encapsulation 
- **Adapters**: Infrastructure and external interfaces (API, Database)
- **Repository Pattern**: Database abstraction layer
- **Background Tasks**: Asynchronous processing of ECG insights

Refer to [THOUGHT_PROCESS.md](THOUGHT_PROCESS.md) for more information about the architecture.

## Prerequisites

- Make
- Python 3.10.9
- uv (Python package installer)
- SQLite

## Installation

1. Clone the repository
2. Install the dependencies:
```bash
make install
```

The `make install` command will:
1. Create a Python virtual environment called `venv`.
2. Install all required dependencies using `uv` package manager.

Note: Make sure you have `uv` installed before running this command.

### Running the application

The following command will run the application on [http://localhost:8000](http://localhost:8000) in development mode.

```bash
make run
```

### Running the tests

The following command will run the tests and will generate a coverage report.

```bash
make test
```

### Formatting the code

The following command will format the code using `black`.

```bash
make format
```

### Cleaning the project (uninstall)

The following command will remove the virtual environment and the generated files (e.g., coverage reports). It will not remove the database.

```bash
make clean
```

### Running with Docker

You can run the application with Docker by running the following commands:

1. Build the Docker image:

```bash
make docker-build
```

2. Run the Docker container:

```bash
make docker-run
```

The `make docker-run` command will run the Docker container and expose the application on [http://localhost:8000](http://localhost:8000). In this case, the FastAPI will be running in production mode. 

## API Documentation

The API documentation is available at [http://localhost:8000/docs](http://localhost:8000/docs).

### ECG endpoints
- `POST /ecg/` - Upload ECG data
- `GET /ecg/{ecg_id}` - Retrieve ECG data
- `GET /ecg/{ecg_id}/insights` - Get ECG insights

### User Management endpoints
- `POST /users/` - Create new user (Admin only). The default admin user is created with username `admin` and password `adminpass`.
