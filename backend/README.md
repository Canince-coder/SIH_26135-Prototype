# SIH26135 — Skilling-to-Employment Platform (Backend Prototype)

Clean-room FastAPI prototype demonstrating the full flow:
Trainee → Training → Skills → Job Requirements → Skill Gap → Matching → Application → Employment → Analytics.

**Stack:** Python · FastAPI · PostgreSQL · SQLAlchemy 2.x · Pydantic v2 · Alembic · JWT

## Structure

```
backend/
├── app/
│   ├── main.py            # FastAPI app + /health
│   ├── core/config.py     # pydantic-settings config
│   ├── db/{base,session}  # Declarative Base, engine, get_db
│   ├── models/            # SQLAlchemy 2.x models (12 tables)
│   ├── schemas/           # Pydantic v2 (later phases)
│   ├── routers/           # API routers (later phases)
│   └── services/          # matching + analytics (later phases)
├── alembic/               # migrations
├── seed.py                # demo data (later phase)
├── requirements.txt
└── .env.example
```

## Setup

```bash
cd backend
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

pip install -r requirements.txt
cp .env.example .env      # then edit DATABASE_URL / SECRET_KEY
```

Create the database (PostgreSQL):

```sql
CREATE DATABASE sih26135;
```

Generate + apply the first migration:

```bash
alembic revision --autogenerate -m "initial schema"
alembic upgrade head
```

Run the server:

```bash
uvicorn app.main:app --reload
```

Health check: `GET http://127.0.0.1:8000/health`

## Tables

`users`, `trainees`, `skills`, `trainee_skills`, `training_programs`,
`program_skills`, `employers`, `job_roles`, `jobs`, `job_requirements`,
`job_applications`, `employments`.

## Build order

Phase 1 (this): project + database foundation.
Later: auth → trainee/skills → jobs → skill-gap engine → recommendations →
applications → employment → analytics → optional AI.
