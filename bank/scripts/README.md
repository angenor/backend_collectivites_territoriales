# Scripts SQL - Base de Données

Scripts SQL temporaires pour initialiser la base de données PostgreSQL.
Ces scripts seront remplacés par des migrations Alembic une fois l'application structurée.

## Fichiers

| Fichier | Description |
|---------|-------------|
| `schema.sql` | Tables, indexes, vues, triggers (17 tables, 3 vues) |
| `seed_plan_comptable.sql` | Plan comptable hiérarchique (~300 comptes) |
| `seed_regions_madagascar.sql` | Géographie: 6 provinces, 22 régions, communes exemples |
| `seed_data.sql` | Données de démonstration (sociétés minières, projets, données financières) |

## Exécution

```bash
# 1. Créer la base de données
psql -U postgres -c "CREATE DATABASE revenus_miniers_db;"

# 2. Exécuter les scripts dans l'ordre
psql -U postgres -d revenus_miniers_db -f schema.sql
psql -U postgres -d revenus_miniers_db -f seed_plan_comptable.sql
psql -U postgres -d revenus_miniers_db -f seed_regions_madagascar.sql
psql -U postgres -d revenus_miniers_db -f seed_data.sql
```

Ou en une seule commande:

```bash
psql -U postgres -d revenus_miniers_db \
  -f schema.sql \
  -f seed_plan_comptable.sql \
  -f seed_regions_madagascar.sql \
  -f seed_data.sql
```

## Structure du Schéma

### Tables Principales

- **Géographie**: `provinces`, `regions`, `communes`
- **Plan Comptable**: `plan_comptable` (hiérarchie 3 niveaux)
- **Données Financières**: `exercices`, `donnees_recettes`, `donnees_depenses`
- **Projets Miniers**: `societes_minieres`, `projets_miniers`, `projets_communes`, `revenus_miniers`
- **Utilisateurs**: `utilisateurs`, `sessions`
- **Autres**: `documents`, `newsletter_abonnes`, `statistiques_visites`, `audit_log`

### Vues SQL pour Export Excel

- `vue_tableau_recettes` - Génère la feuille RECETTE
- `vue_tableau_depenses` - Génère la feuille DEPENSES
- `vue_tableau_equilibre` - Génère la feuille EQUILIBRE

## Réinitialisation

Pour réinitialiser complètement la base:

```bash
psql -U postgres -c "DROP DATABASE IF EXISTS revenus_miniers_db;"
psql -U postgres -c "CREATE DATABASE revenus_miniers_db;"
# Puis ré-exécuter les scripts ci-dessus
```
