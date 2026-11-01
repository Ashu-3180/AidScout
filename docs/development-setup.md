# AidScout backend development setup

## Supported local environment

AidScout uses **Python 3.14.10** at `C:\Python3.14\python.exe` in the isolated `backend\.venv` environment. Do not use or alter the machine's Python 3.15 installation.

Python 3.14 is the newest version confirmed by FastAPI's published classifiers at the time of this assessment.

The other planned components are compatible with Python 3.15 according to their published metadata:

- SQLAlchemy 2.x lists Python 3.15 and provides a Windows CPython 3.15 wheel.
- Alembic lists Python 3.15.
- psycopg 3 lists Python 3.15.
- pytest lists Python 3.15.

The reproducible pins are in `backend/requirements.txt`. Install them only into AidScout's existing environment:

```powershell
& 'E:\Projects\AidScout\backend\.venv\Scripts\python.exe' -m pip install -r requirements.txt
& 'E:\Projects\AidScout\backend\.venv\Scripts\python.exe' -m pip check
```

## PostgreSQL

PostgreSQL 18 is installed locally and its Windows service is running. This milestone did not connect to, inspect, create, or modify any database. After an approved local database and Python 3.14 environment are available, configure a dedicated development database using process environment variables; do not put credentials in source control. The application does not load a `.env` file automatically.

`DATABASE_READINESS_TIMEOUT_SECONDS` bounds initial database connection attempts (default 3). `DATABASE_READINESS_STATEMENT_TIMEOUT_MILLISECONDS` bounds the readiness query after connection (default 3000).

`AIDSCOUT_EXPECTED_DATABASE_NAME` defaults to `aidscout_dev`. Online Alembic execution rejects a URL without that configured database name before an engine is constructed. This is a safety guard, not a security boundary: always use a dedicated database and least-privilege AidScout role.

## Run checks

```powershell
Set-Location E:\Projects\AidScout\backend
& .\.venv\Scripts\python.exe -m pytest
& .\.venv\Scripts\python.exe -m alembic upgrade head --sql
```

`pytest` is database-independent. `alembic upgrade head --sql` renders SQL only and does not connect to PostgreSQL. Do not run `alembic upgrade head` until a dedicated database is approved.

## Next manual step

Provision a dedicated local AidScout PostgreSQL database and a least-privilege local role, then set `DATABASE_URL` in the process environment. Obtain explicit approval before running `alembic upgrade head`; no migration has been applied by this milestone.
