# Medical Records API

A FastAPI-based REST API for managing patient medical records, doctors, and user authentication.

## Features

- Patient medical records management
- Doctor information management
- User authentication with JWT
- CORS support for frontend integration
- PostgreSQL database with SQLAlchemy ORM
- Automatic database migrations with Alembic

## Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd jobtrack
   ```

2. Create a virtual environment:
   ```
   python -m venv .venv
   .venv\Scripts\activate  # On Windows
   ```

3. Install dependencies:
   ```
   pip install fastapi uvicorn sqlalchemy alembic pydantic python-jose[cryptography] passlib[bcrypt] psycopg2-binary
   ```

4. Set up the database:
   - Ensure PostgreSQL is running with a database named `medical_records`
   - Update `DATABASE_URL` in `database.py` if needed
   ```
   alembic upgrade head
   ```

## Running the Application

Start the server with:
```
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`.

## API Documentation

Visit `http://localhost:8000/docs` for interactive Swagger UI documentation.

## Endpoints

- `/records` - Medical records CRUD operations
- `/auth` - User authentication (login/register)
- `/doctors` - Doctor management

## Project Structure

- `main.py` - FastAPI application entry point
- `database.py` - Database configuration
- `models.py` - SQLAlchemy models
- `security.py` - Authentication utilities
- `routers/` - API route handlers
- `schemas/` - Pydantic schemas
- `alembic/` - Database migrations

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests (if any)
5. Submit a pull request

## License

This project is licensed under the MIT License.