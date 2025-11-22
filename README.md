# Backend - Plateforme de Suivi des Revenus Miniers

API FastAPI pour la gestion des revenus miniers des collectivités territoriales de Madagascar.

**Projet**: Transparency International - Initiative Madagascar (TI MG)
**Version**: 1.0.0

---

## 📋 Table des matières

- [Technologies](#technologies)
- [Architecture](#architecture)
- [Installation](#installation)
- [Configuration](#configuration)
- [Démarrage](#démarrage)
- [API Documentation](#api-documentation)
- [Migrations](#migrations)

---

## 🛠️ Technologies

- **Python**: 3.9+
- **FastAPI**: 0.104+
- **PostgreSQL**: 13+
- **SQLAlchemy**: 2.0+
- **Alembic**: Migrations de base de données
- **Pydantic**: Validation des données
- **JWT**: Authentification

---

## 🏗️ Architecture

```
backend_collectivites_territoriales/
├── app/
│   ├── main.py                     # Point d'entrée FastAPI
│   ├── database.py                 # Configuration SQLAlchemy
│   ├── core/                       # Configuration core
│   ├── models/                     # Modèles SQLAlchemy (par domaine)
│   ├── schemas/                    # Schémas Pydantic (validation)
│   ├── services/                   # Logique métier
│   └── api/v1/endpoints/           # Routes API
├── alembic/                        # Migrations
├── scripts/                        # Scripts SQL
└── tests/                          # Tests
```

### Principes

- **Separation of Concerns**: Chaque couche a sa responsabilité
- **Dependency Injection**: Dependencies FastAPI
- **Type Safety**: Validation Pydantic
- **Configuration centralisée**: Pydantic Settings

---

## 🚀 Installation

```bash
# Créer environnement virtuel
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Installer dépendances
pip install -r requirements.txt
```

---

## ⚙️ Configuration

```bash
# Copier template
cp .env.example .env

# Éditer avec vos paramètres
nano .env
```

**Variables importantes**:
- `POSTGRES_*`: Configuration PostgreSQL
- `SECRET_KEY`: Clé secrète JWT (32+ caractères)
- `BACKEND_CORS_ORIGINS`: URLs autorisées

### Base de données

```bash
# Créer la base
psql -U postgres -c "CREATE DATABASE revenus_miniers_db;"

# Charger le schéma
psql -U postgres -d revenus_miniers_db -f scripts/schema.sql
psql -U postgres -d revenus_miniers_db -f scripts/seed_data.sql
psql -U postgres -d revenus_miniers_db -f scripts/seed_regions_madagascar.sql
```

---

## 🏃 Démarrage

```bash
# Mode développement
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**URLs**:
- API Docs: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
- Health: http://localhost:8000/health

---

## 📚 API Documentation

### Endpoints principaux

**Géographie**
```http
GET /api/v1/geo/regions
GET /api/v1/geo/regions/{region_code}/departements
GET /api/v1/geo/communes/{commune_code}
```

**Revenus**
```http
POST /api/v1/revenus/
GET  /api/v1/revenus/commune/{commune_code}
GET  /api/v1/revenus/tableau/{commune_code}/{exercice_annee}
GET  /api/v1/revenus/statistiques/{commune_code}
```

**Authentification**
```http
POST /api/v1/auth/login
POST /api/v1/auth/register
GET  /api/v1/auth/me
```

---

## 🔄 Migrations

```bash
# Créer migration
alembic revision --autogenerate -m "Description"

# Appliquer
alembic upgrade head

# Historique
alembic history

# Rollback
alembic downgrade -1
```

---

## 📞 Contact

**Email**: vramaherison@transparency.mg
**Organisation**: Transparency International - Initiative Madagascar (TI MG)

---

**Version**: 1.0.0
**Dernière mise à jour**: 2025-11-21
