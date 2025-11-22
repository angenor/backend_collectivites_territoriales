# Modèle de Données - Plateforme de Suivi des Revenus Miniers

## 📋 Vue d'ensemble

Ce modèle de données a été conçu pour la **Plateforme Numérique de Suivi des Revenus Miniers des Collectivités Territoriales** développée pour **PCQVP Madagascar / Transparency International Madagascar (TI-MG)**.

### Objectifs du système
- ✅ Renforcer la transparence financière
- ✅ Réduire les risques de détournement de fonds
- ✅ Accroître la redevabilité des acteurs locaux

### Technologies
- **Base de données**: PostgreSQL
- **Backend**: FastAPI avec SQLAlchemy
- **Frontend**: Nuxt.js
- **Migrations**: Alembic

---

## 🗂️ Structure du Modèle

Le modèle est organisé en **8 modules fonctionnels** :

### 1. Module Géographique
Tables pour la hiérarchie territoriale de Madagascar.

#### Tables principales
- `regions` - Les 22 régions administratives
- `departements` - Districts/départements
- `communes` - Communes bénéficiaires des revenus miniers

#### Hiérarchie
```
Région → Département → Commune
```

### 2. Module Projets Miniers
Gestion des projets d'extraction et des sociétés minières.

#### Tables principales
- `types_minerais` - Types de minerais (nickel, cobalt, ilménite, graphite, or, etc.)
- `societes_minieres` - Sociétés exploitantes
- `projets_miniers` - Projets d'extraction sources de revenus

### 3. Module Revenus (Cœur du système)
Gestion flexible des revenus avec structure de tableau dynamique.

#### Tables principales
- `exercices` - Exercices fiscaux/années
- `periodes` - Périodes (colonnes du tableau) - mensuel, trimestriel, semestriel, annuel
- `categories_rubriques` - Catégories (Recettes, Dépenses, Soldes)
- `rubriques` - Rubriques (lignes du tableau) avec hiérarchie
- `revenus` - **Table centrale** contenant les montants et données financières

#### Caractéristiques clés
- **Structure hiérarchique des rubriques** (parent-enfant)
- **Périodes flexibles** (trimestre, mois, année personnalisables)
- **Calculs automatiques** (écart, taux de réalisation)
- **Validation des données** avec traçabilité

### 4. Module Configuration Dynamique
Permet d'étendre le tableau sans coder.

#### Tables principales
- `colonnes_personnalisees` - Définition de colonnes additionnelles
- `valeurs_colonnes_personnalisees` - Valeurs pour ces colonnes

**Fonctionnalité importante** : Permet d'ajouter des colonnes au tableau depuis l'interface d'administration sans intervention technique.

### 5. Module Utilisateurs et Sécurité
Gestion des accès et permissions.

#### Tables principales
- `roles` - Rôles (Administrateur, Éditeur, Lecteur) avec permissions JSON
- `utilisateurs` - Comptes utilisateurs avec authentification

#### Rôles par défaut
- **ADMIN** : Tous les droits
- **EDITEUR** : Lecture, création, modification
- **LECTEUR** : Lecture seule

### 6. Module Documents
Gestion des documents justificatifs avec recherche full-text.

#### Tables principales
- `types_documents` - Types de documents autorisés
- `documents` - Documents avec indexation full-text PostgreSQL

#### Fonctionnalités
- Upload de documents (PDF, Excel, Word, images)
- Indexation du contenu texte
- Recherche full-text en français
- Tags pour catégorisation

### 7. Module Newsletter
Gestion des abonnés et campagnes d'information.

#### Tables principales
- `newsletter_abonnes` - Abonnés avec confirmation double opt-in
- `newsletter_campagnes` - Campagnes d'envoi avec statistiques

### 8. Module Logs et Audit
Traçabilité complète des actions.

#### Tables principales
- `logs_visites` - Statistiques de visites
- `logs_telechargements` - Téléchargements (Excel, Word, PDF)
- `logs_activites` - Audit trail complet (CREATE, UPDATE, DELETE, LOGIN)
- `messages_securises` - Messagerie sécurisée entre utilisateurs

---

## 📊 Schéma de Base de Données

### Diagramme des relations principales

```
┌─────────────┐
│   Région    │
└──────┬──────┘
       │
       ├─────────────┐
       │             │
┌──────▼──────┐  ┌──▼──────┐
│ Département │  │ Commune │
└──────┬──────┘  └──┬──────┘
       │            │
       └────────────┼──────────┐
                    │          │
            ┌───────▼────┐  ┌──▼────────────┐
            │   Projet   │  │    Revenus    │◄───┐
            │   Minier   │  └───────┬───────┘    │
            └────────────┘          │            │
                                    │            │
                            ┌───────▼────┐  ┌────┴────┐
                            │  Période   │  │Rubrique │
                            └────────────┘  └─────────┘
```

---

## 🚀 Installation et Configuration

### 1. Prérequis
```bash
# Python 3.9+
# PostgreSQL 13+
# pip ou poetry pour la gestion des dépendances
```

### 2. Installation des dépendances
```bash
pip install sqlalchemy alembic psycopg2-binary fastapi python-dotenv
```

### 3. Configuration de la base de données

Créer un fichier `.env` à la racine du projet :

```env
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your_password
POSTGRES_SERVER=localhost
POSTGRES_PORT=5432
POSTGRES_DB=revenus_miniers_db
```

### 4. Création de la base de données

```bash
# Se connecter à PostgreSQL
psql -U postgres

# Créer la base de données
CREATE DATABASE revenus_miniers_db;

# Sortir de psql
\q
```

### 5. Exécution du schéma SQL

```bash
# Exécuter le schéma principal
psql -U postgres -d revenus_miniers_db -f bank/modele_de_donnees/schema.sql

# Charger les données initiales
psql -U postgres -d revenus_miniers_db -f bank/modele_de_donnees/scripts/seed_data.sql

# Charger les données géographiques de Madagascar
psql -U postgres -d revenus_miniers_db -f bank/modele_de_donnees/scripts/seed_regions_madagascar.sql
```

### 6. Utilisation avec Alembic (Migrations)

```bash
# Initialiser Alembic (première fois seulement)
cd bank/modele_de_donnees
cp migrations/alembic.ini.example alembic.ini

# Modifier alembic.ini avec vos paramètres de connexion

# Créer une migration
alembic revision --autogenerate -m "Description de la migration"

# Appliquer les migrations
alembic upgrade head

# Revenir en arrière
alembic downgrade -1
```

---

## 💻 Utilisation avec FastAPI

### Exemple d'endpoint pour récupérer les revenus

```python
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import get_db
from models import Revenu, Commune, Rubrique, Periode

app = FastAPI()

@app.get("/revenus/")
def get_revenus(
    commune_code: str = None,
    exercice_annee: int = None,
    db: Session = Depends(get_db)
):
    """Récupère les revenus avec filtres optionnels"""
    query = db.query(Revenu)

    if commune_code:
        query = query.join(Commune).filter(Commune.code == commune_code)

    if exercice_annee:
        query = query.join(Periode).join(Exercice).filter(
            Exercice.annee == exercice_annee
        )

    revenus = query.all()
    return revenus


@app.get("/communes/{region_code}")
def get_communes_by_region(region_code: str, db: Session = Depends(get_db)):
    """Récupère toutes les communes d'une région"""
    communes = db.query(Commune).join(Region).filter(
        Region.code == region_code
    ).all()
    return communes


@app.post("/revenus/")
def create_revenu(revenu_data: dict, db: Session = Depends(get_db)):
    """Crée une nouvelle entrée de revenu"""
    revenu = Revenu(**revenu_data)
    db.add(revenu)
    db.commit()
    db.refresh(revenu)
    return revenu
```

---

## 📈 Exemple de Requêtes Utiles

### 1. Récupérer le tableau de compte administratif d'une commune

```sql
SELECT
    r.nom as region,
    d.nom as departement,
    c.nom as commune,
    cat.nom as categorie,
    rub.code,
    rub.nom as rubrique,
    per.nom as periode,
    ex.annee,
    rev.montant,
    rev.montant_prevu,
    rev.ecart,
    rev.taux_realisation
FROM revenus rev
JOIN communes c ON rev.commune_id = c.id
JOIN departements d ON c.departement_id = d.id
JOIN regions r ON c.region_id = r.id
JOIN rubriques rub ON rev.rubrique_id = rub.id
LEFT JOIN categories_rubriques cat ON rub.categorie_id = cat.id
JOIN periodes per ON rev.periode_id = per.id
JOIN exercices ex ON per.exercice_id = ex.id
WHERE c.code = 'ANO-01-001' AND ex.annee = 2024
ORDER BY cat.ordre, rub.ordre, per.ordre;
```

### 2. Statistiques des revenus miniers par région

```sql
SELECT
    r.nom as region,
    SUM(rev.montant) as total_revenus,
    COUNT(DISTINCT c.id) as nb_communes,
    COUNT(DISTINCT pm.id) as nb_projets_miniers
FROM regions r
JOIN communes c ON c.region_id = r.id
LEFT JOIN revenus rev ON rev.commune_id = c.id
LEFT JOIN projets_miniers pm ON pm.commune_id = c.id
WHERE rev.montant > 0
GROUP BY r.id, r.nom
ORDER BY total_revenus DESC;
```

### 3. Top 10 des communes avec les revenus miniers les plus élevés

```sql
SELECT
    c.nom as commune,
    r.nom as region,
    SUM(rev.montant) as total_revenus,
    COUNT(DISTINCT pm.id) as nb_projets
FROM communes c
JOIN regions r ON c.region_id = r.id
LEFT JOIN revenus rev ON rev.commune_id = c.id
LEFT JOIN projets_miniers pm ON pm.commune_id = c.id
WHERE rev.montant > 0
GROUP BY c.id, c.nom, r.nom
ORDER BY total_revenus DESC
LIMIT 10;
```

### 4. Historique des revenus d'une commune sur plusieurs exercices

```sql
SELECT
    ex.annee,
    per.nom as periode,
    rub.nom as rubrique,
    rev.montant,
    rev.montant_prevu,
    rev.ecart,
    rev.taux_realisation
FROM revenus rev
JOIN periodes per ON rev.periode_id = per.id
JOIN exercices ex ON per.exercice_id = ex.id
JOIN rubriques rub ON rev.rubrique_id = rub.id
WHERE rev.commune_id = (SELECT id FROM communes WHERE code = 'ANO-01-001')
ORDER BY ex.annee, per.ordre, rub.ordre;
```

---

## 🔐 Sécurité et Bonnes Pratiques

### 1. Authentification
- Utiliser des tokens JWT pour l'authentification
- Hasher les mots de passe avec bcrypt ou argon2
- Implémenter le rate limiting

### 2. Permissions
- Vérifier les permissions basées sur les rôles
- Logger toutes les actions sensibles dans `logs_activites`
- Validation des données côté serveur

### 3. Audit Trail
Le système enregistre automatiquement :
- Toutes les visites de pages
- Tous les téléchargements
- Toutes les modifications de données (CRUD)
- Les connexions/déconnexions

### 4. Backup
```bash
# Backup complet
pg_dump -U postgres revenus_miniers_db > backup_$(date +%Y%m%d).sql

# Backup avec compression
pg_dump -U postgres revenus_miniers_db | gzip > backup_$(date +%Y%m%d).sql.gz

# Restauration
psql -U postgres revenus_miniers_db < backup_20250920.sql
```

---

## 🛠️ Maintenance et Évolution

### Ajout d'une nouvelle rubrique
```sql
INSERT INTO rubriques (id, code, nom, categorie_id, parent_id, niveau, ordre, type, actif)
VALUES (
    uuid_generate_v4(),
    'R150',
    'Nouvelle Rubrique',
    (SELECT id FROM categories_rubriques WHERE code = 'RECETTES'),
    (SELECT id FROM rubriques WHERE code = 'R100'),
    3,
    5,
    'recette',
    TRUE
);
```

### Ajout d'une nouvelle colonne personnalisée
```sql
INSERT INTO colonnes_personnalisees (id, code, nom, type_donnee, ordre, visible, editable, actif)
VALUES (
    uuid_generate_v4(),
    'NOTE_VALIDATION',
    'Note de validation',
    'text',
    1,
    TRUE,
    TRUE,
    TRUE
);
```

### Monitoring des performances
```sql
-- Voir les tables les plus volumineuses
SELECT
    schemaname,
    tablename,
    pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) AS size
FROM pg_tables
WHERE schemaname = 'public'
ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC;

-- Voir les index non utilisés
SELECT
    schemaname,
    tablename,
    indexname,
    idx_scan
FROM pg_stat_user_indexes
WHERE idx_scan = 0
ORDER BY schemaname, tablename;
```

---

## 📚 Ressources

### Documentation PostgreSQL
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [PostgreSQL JSON Functions](https://www.postgresql.org/docs/current/functions-json.html)

### Documentation SQLAlchemy
- [SQLAlchemy ORM](https://docs.sqlalchemy.org/en/14/orm/)
- [SQLAlchemy Core](https://docs.sqlalchemy.org/en/14/core/)

### Documentation FastAPI
- [FastAPI](https://fastapi.tiangolo.com/)
- [FastAPI with Databases](https://fastapi.tiangolo.com/tutorial/sql-databases/)

### Documentation Alembic
- [Alembic](https://alembic.sqlalchemy.org/)

---

## 📞 Support

Pour toute question ou problème concernant ce modèle de données :
- **Email**: vramaherison@transparency.mg
- **Organisation**: Transparency International - Initiative Madagascar (TI MG)

---

## 📄 Licence

© 2025 Transparency International - Initiative Madagascar (TI MG)
Projet : Plateforme de Suivi des Revenus Miniers des Collectivités Territoriales

---

## 📝 Notes de Version

### Version 1.0.0 (Initial)
- Modèle de données complet
- Support pour les 22 régions de Madagascar
- Structure flexible pour tableaux dynamiques
- Audit trail complet
- Gestion de documents avec recherche full-text
- Newsletter intégrée
- Messagerie sécurisée
