# AidScout backend architecture

## Scope

This is the Phase 1, Milestone 2 data foundation. It has no authentication, AI, retrieval, paid service, frontend integration, or eligibility decision engine.

## Components

- FastAPI exposes liveness and database-readiness probes.
- Pydantic validates API-bound data structures before persistence.
- SQLAlchemy 2.x models define the normalized PostgreSQL schema.
- Alembic owns schema history; its initial migration is present but has not been applied.
- `services/data_quality.py` evaluates records without claiming they are verified.

## Operational boundaries

`GET /health` never opens a database connection. `GET /ready` performs only `SELECT 1` when `DATABASE_URL` is set and returns a generic 503 otherwise. It never returns a connection string or underlying exception.

The initial read API is intentionally deferred: a database has not been approved or provisioned for this project. Sessions are explicit and short-lived in `app.db.session`; future writes must use an explicit transaction boundary.
