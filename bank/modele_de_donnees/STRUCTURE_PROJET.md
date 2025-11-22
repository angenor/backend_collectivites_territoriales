# Structure du Projet - Modèle de Données

## 📁 Arborescence des Fichiers

```
bank/modele_de_donnees/
│
├── 📄 README.md                      # Documentation complète du modèle
├── 📄 GUIDE_DEMARRAGE.md            # Guide de démarrage rapide
├── 📄 STRUCTURE_PROJET.md           # Ce fichier - Vue d'ensemble
│
├── 🗄️ Base de Données
│   ├── schema.sql                   # Schéma complet PostgreSQL avec tables, vues, triggers
│   └── database.py                  # Configuration SQLAlchemy et connexion DB
│
├── 🏗️ Modèles et Schémas
│   ├── models.py                    # Modèles SQLAlchemy (ORM)
│   └── schemas.py                   # Schémas Pydantic (validation FastAPI)
│
├── 🔧 Services et API
│   ├── services_examples.py         # Services métier (logique applicative)
│   └── api_examples.py              # Routes FastAPI (endpoints)
│
├── 📊 Données Initiales
│   └── scripts/
│       ├── seed_data.sql            # Données de base (rôles, types, rubriques)
│       └── seed_regions_madagascar.sql  # Données géographiques de Madagascar
│
├── 🔄 Migrations
│   └── migrations/
│       ├── alembic.ini.example      # Configuration Alembic
│       ├── env.py                   # Configuration environnement Alembic
│       └── script.py.mako           # Template pour les migrations
│
└── ⚙️ Configuration
    ├── .env.example                 # Variables d'environnement (template)
    └── requirements.txt             # Dépendances Python
```

---

## 📋 Description des Fichiers

### Documentation

#### `README.md`
- Documentation complète et détaillée
- Architecture du modèle de données
- Exemples de requêtes SQL
- Guide d'utilisation avec FastAPI
- Bonnes pratiques de sécurité

#### `GUIDE_DEMARRAGE.md`
- Guide pas-à-pas pour démarrer
- Installation et configuration
- Exemples pratiques
- Dépannage

#### `STRUCTURE_PROJET.md` (ce fichier)
- Vue d'ensemble de l'organisation
- Description des fichiers
- Relations entre les modules

---

### Base de Données

#### `schema.sql` (1200+ lignes)
**Contient:**
- ✅ 30+ tables relationnelles
- ✅ Contraintes d'intégrité (FK, UNIQUE, CHECK)
- ✅ Index pour optimisation
- ✅ Vues SQL utiles
- ✅ Triggers automatiques
- ✅ Fonctions PostgreSQL
- ✅ Commentaires détaillés

**Tables principales:**
- Géographie: `regions`, `departements`, `communes`
- Projets miniers: `projets_miniers`, `societes_minieres`, `types_minerais`
- Revenus: `exercices`, `periodes`, `rubriques`, `revenus` (table centrale)
- Configuration: `colonnes_personnalisees`, `valeurs_colonnes_personnalisees`
- Utilisateurs: `roles`, `utilisateurs`
- Documents: `types_documents`, `documents`
- Logs: `logs_visites`, `logs_telechargements`, `logs_activites`
- Newsletter: `newsletter_abonnes`, `newsletter_campagnes`
- Messagerie: `messages_securises`

#### `database.py` (100 lignes)
**Contient:**
- Configuration de connexion PostgreSQL
- Factory pour sessions SQLAlchemy
- Fonction `get_db()` pour FastAPI Dependency Injection
- Fonctions utilitaires `init_db()` et `drop_db()`

---

### Modèles et Schémas

#### `models.py` (800+ lignes)
**Contient:**
- 30+ classes SQLAlchemy (modèles ORM)
- Relations entre tables (ForeignKey, relationship)
- Mixins réutilisables (TimestampMixin, ActiveMixin)
- Configuration des index et contraintes

**Organisation:**
- Modèles géographiques
- Modèles projets miniers
- Modèles revenus
- Modèles configuration dynamique
- Modèles utilisateurs
- Modèles documents
- Modèles newsletter
- Modèles logs

#### `schemas.py` (600+ lignes)
**Contient:**
- 50+ schémas Pydantic pour validation
- Schémas de création (Create)
- Schémas de mise à jour (Update)
- Schémas de réponse (InDB)
- Schémas détaillés (Detail)
- Schémas de filtrage et pagination

**Types de schémas:**
- Base: données minimales
- Create: pour création
- Update: pour modification
- InDB: représentation complète
- Detail: avec relations imbriquées

---

### Services et API

#### `services_examples.py` (500+ lignes)
**Contient:**
- Classes de services métier
- Logique applicative complexe
- Requêtes SQL optimisées
- Calculs et transformations

**Services:**
- `CommuneService`: Gestion géographique
- `RevenuService`: Gestion des revenus et tableaux
- `StatistiquesService`: Calculs statistiques
- `ExportService`: Gestion des exports et logs

#### `api_examples.py` (500+ lignes)
**Contient:**
- Routers FastAPI
- Endpoints REST complets
- Documentation OpenAPI
- Gestion des erreurs

**Routers:**
- `/geo`: Endpoints géographiques
- `/revenus`: CRUD des revenus
- `/tableaux`: Génération de tableaux administratifs
- `/statistiques`: Statistiques et rapports
- `/export`: Export Excel/Word/PDF

---

### Données Initiales

#### `scripts/seed_data.sql` (400 lignes)
**Contient:**
- Rôles par défaut (ADMIN, EDITEUR, LECTEUR)
- Types de documents
- Types de minerais
- Catégories de rubriques
- Rubriques de base (structure hiérarchique)

#### `scripts/seed_regions_madagascar.sql` (500 lignes)
**Contient:**
- 22 régions de Madagascar
- Départements/districts principaux
- Communes importantes (zones minières)
- Données géographiques réelles

---

### Migrations

#### `migrations/alembic.ini.example`
- Configuration Alembic
- URL de connexion
- Paramètres de logging

#### `migrations/env.py`
- Configuration environnement Alembic
- Import des modèles
- Récupération variables d'environnement

#### `migrations/script.py.mako`
- Template pour générer les migrations
- Structure standardisée

---

### Configuration

#### `.env.example`
**Variables:**
- Connexion PostgreSQL
- Configuration FastAPI
- Sécurité JWT
- Configuration CORS
- Upload de fichiers
- Configuration email (SMTP)
- URLs frontend/backend

#### `requirements.txt`
**Dépendances:**
- SQLAlchemy 2.0+
- FastAPI 0.104+
- Pydantic 2.5+
- psycopg2-binary
- Alembic
- python-jose (JWT)
- passlib (hashing)
- openpyxl (Excel)
- python-docx (Word)
- reportlab (PDF)

---

## 🔄 Flux de Données

### 1. Requête utilisateur
```
Frontend (Nuxt) → API FastAPI (api_examples.py)
```

### 2. Traitement
```
API → Service (services_examples.py) → Validation (schemas.py)
```

### 3. Base de données
```
Service → Modèle (models.py) → PostgreSQL (schema.sql)
```

### 4. Réponse
```
PostgreSQL → Modèle → Service → Schéma Pydantic → API → Frontend
```

---

## 🎯 Points d'Entrée

### Pour le Développement Backend

1. **Démarrer avec la base de données:**
   ```bash
   psql -U postgres -f schema.sql
   psql -U postgres -f scripts/seed_data.sql
   ```

2. **Tester les modèles:**
   ```python
   from models import Region, Commune
   from database import SessionLocal
   ```

3. **Créer l'API:**
   ```python
   from api_examples import router_geo, router_revenus
   app.include_router(router_geo)
   ```

### Pour l'Intégration Frontend

1. **Récupérer les régions:**
   ```
   GET /api/v1/geo/regions
   ```

2. **Récupérer un tableau:**
   ```
   GET /api/v1/tableaux/compte-administratif/{commune_code}/{exercice_annee}
   ```

3. **Exporter en Excel:**
   ```
   GET /api/v1/export/excel/{commune_code}/{exercice_annee}
   ```

---

## 🔐 Sécurité

### Fonctionnalités implémentées

- ✅ Soft delete (champ `actif`)
- ✅ Timestamps automatiques
- ✅ Audit trail complet (`logs_activites`)
- ✅ Validation des données (Pydantic)
- ✅ Gestion des rôles et permissions
- ✅ Tokens JWT (à implémenter)
- ✅ Hashing de mots de passe (à implémenter)

### À implémenter

- ⏳ Authentification JWT complète
- ⏳ Middleware de vérification des permissions
- ⏳ Rate limiting
- ⏳ Validation des fichiers uploadés
- ⏳ Chiffrement des données sensibles

---

## 📊 Statistiques du Projet

### Code
- **Lignes de SQL**: ~2500
- **Lignes de Python**: ~3500
- **Tables**: 30+
- **Modèles SQLAlchemy**: 30+
- **Schémas Pydantic**: 50+
- **Endpoints API**: 20+

### Documentation
- **Fichiers markdown**: 3
- **Lignes de documentation**: ~2000

### Couverture fonctionnelle
- ✅ Gestion géographique complète
- ✅ Gestion des projets miniers
- ✅ Gestion des revenus (tableau dynamique)
- ✅ Statistiques et rapports
- ✅ Export de données
- ✅ Gestion utilisateurs
- ✅ Documents et recherche
- ✅ Newsletter
- ✅ Audit trail
- ⏳ Messagerie sécurisée (structure prête)

---

## 🚀 Prochaines Étapes

### Phase 1: Backend Core
1. ✅ Modèle de données complet
2. ⏳ Authentification JWT
3. ⏳ Gestion des permissions
4. ⏳ Tests unitaires

### Phase 2: Features
1. ⏳ Export Excel/Word/PDF complet
2. ⏳ Upload et indexation de documents
3. ⏳ Moteur de recherche full-text
4. ⏳ Newsletter (envoi d'emails)

### Phase 3: Integration
1. ⏳ API complète pour Nuxt
2. ⏳ WebSockets pour notifications temps réel
3. ⏳ Intégration Global Leaks
4. ⏳ Dashboard d'administration

---

## 📞 Contact

**Projet:** Plateforme de Suivi des Revenus Miniers
**Client:** Transparency International - Initiative Madagascar (TI MG)
**Email:** vramaherison@transparency.mg

---

**Dernière mise à jour:** 2025-11-20
**Version:** 1.0.0
