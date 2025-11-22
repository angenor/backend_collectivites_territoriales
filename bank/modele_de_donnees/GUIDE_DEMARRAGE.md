# Guide de Démarrage Rapide

## 🚀 Mise en route en 5 minutes

Ce guide vous permettra de démarrer rapidement avec le modèle de données de la plateforme de suivi des revenus miniers.

---

## Étape 1: Installation des dépendances

```bash
# Créer un environnement virtuel
python -m venv venv

# Activer l'environnement virtuel
# Sur macOS/Linux:
source venv/bin/activate
# Sur Windows:
venv\Scripts\activate

# Installer les dépendances
pip install -r requirements.txt
```

---

## Étape 2: Configuration de la base de données

### 2.1 Créer la base de données PostgreSQL

```bash
# Se connecter à PostgreSQL
psql -U postgres

# Dans psql, exécuter:
CREATE DATABASE revenus_miniers_db;
CREATE USER revenus_user WITH PASSWORD 'votre_mot_de_passe';
GRANT ALL PRIVILEGES ON DATABASE revenus_miniers_db TO revenus_user;

# Sortir de psql
\q
```

### 2.2 Configurer les variables d'environnement

```bash
# Copier le fichier .env.example
cp .env.example .env

# Éditer .env avec vos paramètres
nano .env
```

Modifier ces lignes dans `.env`:
```env
POSTGRES_USER=revenus_user
POSTGRES_PASSWORD=votre_mot_de_passe
POSTGRES_SERVER=localhost
POSTGRES_PORT=5432
POSTGRES_DB=revenus_miniers_db
```

---

## Étape 3: Initialiser la base de données

### Option A: Utiliser le script SQL complet (Recommandé pour le démarrage)

```bash
# Exécuter le schéma
psql -U revenus_user -d revenus_miniers_db -f schema.sql

# Charger les données initiales
psql -U revenus_user -d revenus_miniers_db -f scripts/seed_data.sql

# Charger les données géographiques de Madagascar
psql -U revenus_user -d revenus_miniers_db -f scripts/seed_regions_madagascar.sql
```

### Option B: Utiliser SQLAlchemy (Pour le développement)

```python
# Dans un fichier Python ou en ligne de commande interactive
from database import init_db
init_db()
```

---

## Étape 4: Tester la connexion

Créez un fichier `test_connection.py`:

```python
from database import SessionLocal
from models import Region

# Créer une session
db = SessionLocal()

# Tester la récupération des régions
regions = db.query(Region).all()
print(f"Nombre de régions: {len(regions)}")

for region in regions[:3]:
    print(f"- {region.nom} ({region.code})")

db.close()
```

Exécuter:
```bash
python test_connection.py
```

Résultat attendu:
```
Nombre de régions: 22
- Analamanga (ANA)
- Vakinankaratra (VAK)
- Itasy (ITO)
```

---

## Étape 5: Lancer l'API FastAPI (Exemple)

Créez un fichier `main.py`:

```python
from fastapi import FastAPI
from database import engine
from models import Base
from api_examples import (
    router_geo, router_revenus, router_tableaux,
    router_stats, router_export
)

# Créer l'application FastAPI
app = FastAPI(
    title="Plateforme Revenus Miniers",
    description="API de suivi des revenus miniers des collectivités territoriales",
    version="1.0.0"
)

# Inclure les routers
app.include_router(router_geo, prefix="/api/v1")
app.include_router(router_revenus, prefix="/api/v1")
app.include_router(router_tableaux, prefix="/api/v1")
app.include_router(router_stats, prefix="/api/v1")
app.include_router(router_export, prefix="/api/v1")

@app.get("/")
def root():
    return {
        "message": "Bienvenue sur l'API de la Plateforme de Suivi des Revenus Miniers",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc"
    }

@app.get("/health")
def health_check():
    return {"status": "healthy"}
```

Lancer le serveur:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Accéder à la documentation interactive:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

---

## Étape 6: Tester les endpoints

### Via curl

```bash
# Récupérer toutes les régions
curl http://localhost:8000/api/v1/geo/regions

# Récupérer les départements d'une région
curl http://localhost:8000/api/v1/geo/regions/ANA/departements

# Récupérer une commune
curl http://localhost:8000/api/v1/geo/communes/ANO-01-001
```

### Via l'interface Swagger

1. Aller sur http://localhost:8000/docs
2. Développer un endpoint (ex: `/api/v1/geo/regions`)
3. Cliquer sur "Try it out"
4. Cliquer sur "Execute"

---

## 🎯 Exemples d'utilisation

### Exemple 1: Créer une nouvelle entrée de revenu

```python
from database import SessionLocal
from models import Revenu
from decimal import Decimal
from uuid import UUID

db = SessionLocal()

# IDs à récupérer depuis la base
commune_id = UUID("...")  # ID de la commune
rubrique_id = UUID("...")  # ID de la rubrique
periode_id = UUID("...")  # ID de la période

# Créer le revenu
revenu = Revenu(
    commune_id=commune_id,
    rubrique_id=rubrique_id,
    periode_id=periode_id,
    montant=Decimal("1500000.00"),
    montant_prevu=Decimal("1200000.00"),
    observations="Ristournes minières Q1 2024"
)

db.add(revenu)
db.commit()
db.refresh(revenu)

print(f"Revenu créé: {revenu.id}")
print(f"Écart: {revenu.ecart}")
print(f"Taux de réalisation: {revenu.taux_realisation}%")

db.close()
```

### Exemple 2: Récupérer le tableau de compte administratif

```python
from services_examples import RevenuService
from database import SessionLocal

db = SessionLocal()

# Récupérer le tableau pour une commune
tableau = RevenuService.get_tableau_compte_administratif(
    db=db,
    commune_code="ANO-01-001",
    exercice_annee=2024
)

print(f"Commune: {tableau['commune'].nom}")
print(f"Exercice: {tableau['exercice'].annee}")
print(f"Nombre de périodes: {len(tableau['periodes'])}")
print(f"Nombre de rubriques: {len(tableau['rubriques'])}")

db.close()
```

### Exemple 3: Obtenir des statistiques

```python
from services_examples import StatistiquesService
from database import SessionLocal

db = SessionLocal()

# Statistiques d'une commune
stats = StatistiquesService.get_statistiques_commune(
    db=db,
    commune_code="ANO-01-001",
    exercice_annee=2024
)

print(f"Total recettes: {stats['total_recettes']}")
print(f"Total dépenses: {stats['total_depenses']}")
print(f"Solde: {stats['solde']}")

db.close()
```

---

## 🔧 Configuration Alembic (Migrations)

### Initialiser Alembic

```bash
# Copier la configuration
cd migrations
cp alembic.ini.example alembic.ini

# Modifier sqlalchemy.url dans alembic.ini
nano alembic.ini
```

### Créer une migration

```bash
# Générer automatiquement depuis les modèles
alembic revision --autogenerate -m "Description de la migration"

# Appliquer la migration
alembic upgrade head

# Voir l'historique
alembic history

# Revenir en arrière
alembic downgrade -1
```

---

## 📊 Vérifier les données

### Compter les entrées

```sql
-- Nombre de régions
SELECT COUNT(*) FROM regions;

-- Nombre de départements
SELECT COUNT(*) FROM departements;

-- Nombre de communes
SELECT COUNT(*) FROM communes;

-- Nombre de rubriques
SELECT COUNT(*) FROM rubriques;
```

### Afficher les hiérarchies

```sql
-- Hiérarchie géographique
SELECT
    r.nom as region,
    d.nom as departement,
    c.nom as commune
FROM communes c
JOIN departements d ON c.departement_id = d.id
JOIN regions r ON c.region_id = r.id
ORDER BY r.nom, d.nom, c.nom
LIMIT 10;

-- Hiérarchie des rubriques
SELECT
    cat.nom as categorie,
    r1.nom as rubrique_niveau_1,
    r2.nom as rubrique_niveau_2,
    r3.nom as rubrique_niveau_3
FROM rubriques r1
LEFT JOIN categories_rubriques cat ON r1.categorie_id = cat.id
LEFT JOIN rubriques r2 ON r2.parent_id = r1.id
LEFT JOIN rubriques r3 ON r3.parent_id = r2.id
WHERE r1.niveau = 1
ORDER BY cat.ordre, r1.ordre;
```

---

## 🐛 Dépannage

### Problème: Cannot connect to PostgreSQL

**Solution**:
1. Vérifier que PostgreSQL est démarré:
   ```bash
   # Sur macOS
   brew services list

   # Sur Linux
   sudo systemctl status postgresql
   ```

2. Vérifier les identifiants dans `.env`

3. Tester la connexion:
   ```bash
   psql -U revenus_user -d revenus_miniers_db -h localhost
   ```

### Problème: Import errors

**Solution**:
```bash
# Réinstaller les dépendances
pip install --upgrade -r requirements.txt

# Vérifier l'activation de l'environnement virtuel
which python
```

### Problème: Alembic migration errors

**Solution**:
1. Supprimer les migrations existantes:
   ```bash
   rm migrations/versions/*.py
   ```

2. Recréer la migration:
   ```bash
   alembic revision --autogenerate -m "Initial migration"
   alembic upgrade head
   ```

---

## 📚 Prochaines étapes

1. **Lire le README complet**: [README.md](README.md)
2. **Explorer les exemples d'API**: [api_examples.py](api_examples.py)
3. **Comprendre les services**: [services_examples.py](services_examples.py)
4. **Personnaliser les schémas**: [schemas.py](schemas.py)

---

## 💡 Conseils

- **Toujours utiliser des transactions** pour les opérations multiples
- **Logger les actions importantes** avec `LogActivite`
- **Valider les données** côté serveur avec Pydantic
- **Tester régulièrement** avec des données réelles
- **Faire des backups réguliers** de la base de données

---

## 📞 Support

Pour toute question:
- **Email**: vramaherison@transparency.mg
- **Documentation complète**: [README.md](README.md)

---

Bonne chance avec votre développement ! 🚀
