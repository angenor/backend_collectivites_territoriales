# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

FastAPI backend for **Plateforme de Suivi des Revenus Miniers** - a mining revenues tracking platform for territorial collectivities in Madagascar. Built for Transparency International - Initiative Madagascar (TI MG).

**Stack**: Python 3.9+ | FastAPI 0.104+ | PostgreSQL 13+ | SQLAlchemy 2.0+ | Alembic | Pydantic v2 | JWT Auth

## Development Commands

```bash
# Activate virtual environment
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Install dependencies
.venv/bin/pip install -r requirements.txt

# Run development server
.venv/bin/uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Run tests
.venv/bin/pytest
.venv/bin/pytest --cov=app                    # with coverage
.venv/bin/pytest tests/test_api/test_auth.py  # single file

# Database migrations (when app/ structure exists)
alembic revision --autogenerate -m "description"
alembic upgrade head
alembic downgrade -1
```

## Architecture

Target layered structure (to be implemented):

```
app/
├── main.py              # FastAPI entry point, CORS, routers
├── database.py          # SQLAlchemy engine and session
├── core/
│   ├── config.py        # Pydantic Settings (loads .env)
│   └── security.py      # JWT tokens, password hashing
├── models/              # SQLAlchemy models (one file per domain)
├── schemas/             # Pydantic schemas (request/response)
├── services/            # Business logic layer
└── api/v1/endpoints/    # Route handlers
```

**Key Patterns**:
- Dependency injection for DB sessions: `db: Session = Depends(get_db)`
- Auth dependency: `current_user: User = Depends(get_current_active_user)`
- Domain-driven organization: geographie, revenus, utilisateurs, projets_miniers

## Domain Model

Core entities for the mining revenues platform:

- **Geographie**: Province → Region → Commune (Madagascar admin hierarchy)
- **ProjetMinier / SocieteMiniere**: Mining projects and companies
- **RevenuMinier**: Revenue records per commune per fiscal year (Exercice)
- **Utilisateur**: Users with roles (admin, commune, viewer)
- **Document**: File attachments for revenue records
- **Newsletter**: Email subscriptions

## API Endpoints Structure

```
/api/v1/
├── auth/          # login, register, me
├── geo/           # regions, departements, communes
├── revenus/       # revenue CRUD, statistics, tables
├── projets/       # mining projects
├── export/        # Excel/PDF export
└── utilisateurs/  # user management (admin)
```

## Database Setup

```bash
# Create database
psql -U postgres -c "CREATE DATABASE revenus_miniers_db;"

# Load schema and seed data (when scripts exist)
psql -U postgres -d revenus_miniers_db -f scripts/schema.sql
psql -U postgres -d revenus_miniers_db -f scripts/seed_data.sql
psql -U postgres -d revenus_miniers_db -f scripts/seed_regions_madagascar.sql
```

## Configuration

Copy `.env.example` to `.env` and configure:

- `POSTGRES_*`: Database connection
- `SECRET_KEY`: JWT secret (32+ chars required)
- `BACKEND_CORS_ORIGINS`: Allowed origins for CORS (include frontend URL)

## Frontend Integration

- **Frontend**: Nuxt 4 at http://localhost:3000
- **Backend**: FastAPI at http://localhost:8000
- **CORS**: Configured in `.env` via `BACKEND_CORS_ORIGINS`
- **API Docs**: Swagger UI at /docs, ReDoc at /redoc

## Reference Documentation

- Requirements spec: [bank/cahier_des_charges/cahier_des_charges_PCQVP_Plateforme_TdR_Conception.md](bank/cahier_des_charges/cahier_des_charges_PCQVP_Plateforme_TdR_Conception.md)
- Excel template: [bank/exemples/Tableaux_de_Compte_Administratif.xlsx](bank/exemples/Tableaux_de_Compte_Administratif.xlsx)
