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

PostgreSQL 18 is installed locally and its Windows service is running. This milestone did not connect to, inspect, create, or modify any database. After an approved local database and Python 3.14 environment are available, configure a dedicated development database using an environment variable such as `DATABASE_URL`; do not put credentials in source control.

## Run checks

```powershell
Set-Location E:\Projects\AidScout\backend
& .\.venv\Scripts\python.exe -m pytest
& .\.venv\Scripts\python.exe -m alembic check
```

`pytest` is database-independent. `alembic check` requires a dedicated configured database and must not be run against an existing database without explicit approval.

## Next manual step

Provision a dedicated local AidScout PostgreSQL database and a least-privilege local role, then set `DATABASE_URL` in an untracked `backend/.env`. Obtain explicit approval before running `alembic upgrade head`; no migration has been applied by this milestone.
