# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

FastAPI backend for **Plateforme de Suivi des Revenus Miniers** - a platform to track mining revenues for territorial collectivities in Madagascar. Built for **Transparency International - Initiative Madagascar (TI MG)**.

**Stack**: Python 3.9+, FastAPI 0.104+, PostgreSQL 13+, SQLAlchemy 2.0+, Alembic, Pydantic v2, JWT authentication

---

## Development Commands

### Environment Setup
```bash
# Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Install dependencies
.venv/bin/pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your PostgreSQL credentials and SECRET_KEY
```

### Database Setup
```bash
# Create PostgreSQL database
psql -U postgres -c "CREATE DATABASE revenus_miniers_db;"

# Load schema and seed data (in order)
psql -U postgres -d revenus_miniers_db -f scripts/schema.sql
psql -U postgres -d revenus_miniers_db -f scripts/seed_data.sql
psql -U postgres -d revenus_miniers_db -f scripts/seed_regions_madagascar.sql
```

### Running the Application
```bash
# Development mode (auto-reload)
./run.sh
# Or directly:
.venv/bin/uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Access points:
# - API Docs: http://localhost:8000/docs
# - ReDoc: http://localhost:8000/redoc
# - Health: http://localhost:8000/health
```

### Database Migrations (Alembic)
```bash
# Create new migration
alembic revision --autogenerate -m "Description of changes"

# Apply migrations
alembic upgrade head

# View migration history
alembic history

# Rollback one migration
alembic downgrade -1
```

### Testing
```bash
# Run all tests
.venv/bin/pytest

# Run with coverage
.venv/bin/pytest --cov=app

# Run specific test file
.venv/bin/pytest tests/test_api/test_geographie.py
```

---

## Architecture

### Layered Structure
```
app/
├── main.py                  # FastAPI application entry point
├── database.py              # SQLAlchemy engine, session, Base
├── dependencies.py          # Global dependencies
├── core/                    # Core configuration
│   ├── config.py           # Pydantic Settings (env vars)
│   ├── security.py         # JWT token creation/verification
│   └── logger.py           # Logging setup
├── models/                  # SQLAlchemy models (domain entities)
│   ├── geographie.py       # Region, Departement, Commune
│   ├── projets_miniers.py  # ProjetMinier, SocieteMiniere
│   ├── revenus.py          # RevenuMinier, Exercice
│   ├── utilisateurs.py     # Utilisateur, Role
│   ├── documents.py        # Document attachments
│   ├── newsletter.py       # Newsletter subscriptions
│   └── logs.py             # Audit logs
├── schemas/                 # Pydantic schemas (validation/serialization)
│   ├── geographie.py
│   ├── revenus.py
│   ├── utilisateurs.py
│   └── statistiques.py
├── services/                # Business logic layer
│   ├── commune_service.py
│   ├── revenu_service.py
│   └── auth_service.py
└── api/
    ├── deps.py              # API dependencies (get_current_user, etc.)
    └── v1/
        ├── api.py           # Router aggregation
        └── endpoints/       # API routes
            ├── geographie.py    # /api/v1/geo/*
            ├── revenus.py       # /api/v1/revenus/*
            ├── utilisateurs.py  # /api/v1/auth/*
            └── export.py        # /api/v1/export/*
```

### Key Architectural Patterns

**1. Dependency Injection**
- Database sessions: Use `db: Session = Depends(get_db)` in route handlers
- Authentication: Use `current_user: Utilisateur = Depends(get_current_active_user)` for protected routes
- Dependencies defined in [app/api/deps.py](app/api/deps.py) and [app/database.py](app/database.py)

**2. Domain-Driven Organization**
- Models organized by business domain (geographie, revenus, utilisateurs, projets_miniers)
- Each domain has corresponding schemas and services
- Services contain business logic, keeping routes thin

**3. SQLAlchemy 2.0 Modern Style**
- Uses `future=True` flag for forward compatibility
- Declarative base from `sqlalchemy.orm.declarative_base()`
- Connection pooling disabled (`NullPool`) to avoid connection issues

**4. Configuration Management**
- All configuration in [app/core/config.py](app/core/config.py) using Pydantic Settings
- Environment variables loaded from `.env` file
- Settings accessed via singleton: `from app.core.config import settings`
- Database URL constructed dynamically from `POSTGRES_*` variables

**5. Authentication Flow**
- JWT tokens (OAuth2PasswordBearer scheme)
- Token endpoint: `POST /api/v1/auth/login`
- Token verification in [app/core/security.py](app/core/security.py)
- User extraction in [app/api/deps.py](app/api/deps.py):
  - `get_current_user()` - validates token, returns Utilisateur
  - `get_current_active_user()` - additionally checks user is active

**6. Testing Strategy**
- SQLite in-memory database for tests (configured in [tests/conftest.py](tests/conftest.py))
- FastAPI TestClient for API endpoint testing
- Database fixtures with function scope (fresh DB per test)
- Override `get_db` dependency for test database

---

## Important Implementation Notes

### Adding New Endpoints
1. Create/update model in `app/models/` if needed
2. Create Pydantic schemas in `app/schemas/` for request/response validation
3. Implement business logic in `app/services/`
4. Create route handler in `app/api/v1/endpoints/`
5. Register router in [app/api/v1/api.py](app/api/v1/api.py)

### Database Changes
1. Update SQLAlchemy model in `app/models/`
2. Generate migration: `alembic revision --autogenerate -m "description"`
3. Review generated migration in `alembic/versions/`
4. Apply: `alembic upgrade head`
5. **Never** edit models without creating a migration

### Protected Routes
```python
from fastapi import Depends
from app.api.deps import get_current_active_user
from app.models.utilisateurs import Utilisateur

@router.get("/protected")
def protected_route(
    current_user: Utilisateur = Depends(get_current_active_user)
):
    return {"user": current_user.email}
```

### Database Sessions
Always use dependency injection for database sessions:
```python
from sqlalchemy.orm import Session
from app.database import get_db

@router.get("/items")
def get_items(db: Session = Depends(get_db)):
    return db.query(Model).all()
```

### Configuration Access
```python
from app.core.config import settings

# Access any setting
debug_mode = settings.DEBUG
db_url = settings.DATABASE_URL
secret = settings.SECRET_KEY
```

---

## Domain Context

### Core Entities
- **Geographie**: Region → Departement → Commune (administrative hierarchy of Madagascar)
- **ProjetMinier**: Mining projects with associated SocieteMiniere
- **RevenuMinier**: Revenue records per commune per exercise (fiscal year)
- **Utilisateur**: Users with role-based access (admin, commune, viewer)
- **Document**: File attachments for revenue records

### Business Logic Location
- Geographic queries: [app/services/commune_service.py](app/services/commune_service.py)
- Revenue operations: [app/services/revenu_service.py](app/services/revenu_service.py)
- Authentication: [app/services/auth_service.py](app/services/auth_service.py)

### SQL Scripts
- [scripts/schema.sql](scripts/schema.sql): Full database schema
- [scripts/seed_data.sql](scripts/seed_data.sql): Initial data
- [scripts/seed_regions_madagascar.sql](scripts/seed_regions_madagascar.sql): Madagascar administrative regions

---

## Environment Variables

Critical variables (see [.env.example](.env.example)):
- `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_SERVER`, `POSTGRES_PORT`, `POSTGRES_DB`
- `SECRET_KEY`: Must be 32+ characters for JWT security
- `BACKEND_CORS_ORIGINS`: JSON array of allowed origins
- `DEBUG`: Set to `True` for development (enables SQL logging)

---

## Contact

**Organization**: Transparency International - Initiative Madagascar (TI MG)
**Email**: vramaherison@transparency.mg
