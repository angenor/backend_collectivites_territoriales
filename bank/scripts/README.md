# Scripts SQL - Base de Données

Scripts SQL temporaires pour initialiser la base de données PostgreSQL.
Ces scripts seront remplacés par des migrations Alembic une fois l'application structurée.

## Fichiers

| Fichier | Description |
|---------|-------------|
| `schema.sql` | Tables, indexes, vues, triggers (25 tables, 5 vues) - inclut le système CMS |
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

### Système CMS - Pages Compte Administratif (v2.0)

Tables pour gérer le contenu éditorialisé des pages de compte administratif :

- **`pages_compte_administratif`** - Page principale (1 par commune/exercice)
- **`sections_cms`** - Sections de contenu avec ordre et visibilité

Tables de contenu spécifiques :

| Table | Type de section | Description |
|-------|-----------------|-------------|
| `contenus_editorjs` | `editorjs` | Texte enrichi au format EditorJS (obligatoire) |
| `blocs_image_texte` | `bloc_image_gauche`, `bloc_image_droite` | Bloc image + texte |
| `blocs_carte_fond` | `carte_fond_image` | Carte avec image de fond et contenu superposé |
| `cartes_informatives` | `grille_cartes` | Cartes pour les grilles (3 colonnes) |
| `photos_galerie` | `galerie_photos` | Photos pour les galeries |
| `liens_utiles` | `liens_utiles` | Liens vers documentation externe |

#### Types de sections disponibles

| Type | Obligatoire | Description |
|------|-------------|-------------|
| `editorjs` | Oui | Texte enrichi (EditorJS) |
| `bloc_image_gauche` | Non | Image à gauche + contenu à droite |
| `bloc_image_droite` | Non | Image à droite + contenu à gauche |
| `carte_fond_image` | Non | Carte plein écran avec image de fond |
| `grille_cartes` | Non | Grille de cartes informatives |
| `galerie_photos` | Non | Galerie de photos |
| `note_informative` | Non | Note informative |
| `liens_utiles` | Non | Section liens utiles |
| `tableau_financier` | Oui | Tableau financier intégré |
| `graphiques_analytiques` | Non | Section graphiques analytiques |

#### Fonctionnalités CMS

- **Ordre personnalisable** : Chaque section a un champ `ordre` pour définir sa position
- **Visibilité** : `visible` pour la page détail, `visible_accueil` pour la page d'accueil
- **Statut de publication** : `brouillon`, `publie`, `archive`
- **Configuration JSON** : Champ `config` pour options spécifiques à chaque type

### Vues SQL pour Export Excel

- `vue_tableau_recettes` - Génère la feuille RECETTE
- `vue_tableau_depenses` - Génère la feuille DEPENSES
- `vue_tableau_equilibre` - Génère la feuille EQUILIBRE

### Vues SQL pour le CMS

- `vue_page_compte_administratif` - Page avec infos géographiques et compteurs
- `vue_sections_cms_detaillees` - Sections avec contenu et compteurs d'éléments

## Réinitialisation

Pour réinitialiser complètement la base:

```bash
psql -U postgres -c "DROP DATABASE IF EXISTS revenus_miniers_db;"
psql -U postgres -c "CREATE DATABASE revenus_miniers_db;"
# Puis ré-exécuter les scripts ci-dessus
```
