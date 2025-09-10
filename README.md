# FastAPI CRUD Assignment

## Overview
Small FastAPI application exposing CRUD for an `Item` resource (a simple task/book-like entity).
Includes:
- FastAPI + SQLAlchemy (SQLite)
- Pydantic schemas
- CRUD endpoints (POST, GET list, GET single, PUT, DELETE)
- Pagination support (`limit` and `offset`)
- One custom SQL query (aggregation)
- Transaction handling (create + update wrapped)
- Tests: unit test for business logic and integration test using TestClient
- Dockerfile and requirements.txt

## Run
1. Create virtualenv and install:
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```
2. Create .env file with variables defined in sample.env file
3. Run migration using alembic
4. Run the app:
```bash
uvicorn main:app --reload
```
API available at `http://127.0.0.1:8000`.

3. Run tests:
```bash
PYTHONPATH=. pytest -q
```

## Notes
- Database: SQLite file `./test.db` by default.
- Unique constraint: `title` is UNIQUE.
- Custom SQL: `GET /items/summary/` uses a custom SQL aggregation to return counts.
- Transaction example: `POST /items/?related_update_id=...` will create a new item and update another item inside a single transaction.

