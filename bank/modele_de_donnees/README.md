# Modèle de Données - Plateforme de Suivi des Revenus Miniers

## Vue d'ensemble

Ce modèle de données est conçu pour la plateforme numérique de suivi de l'utilisation des revenus miniers des collectivités territoriales à Madagascar, utilisant **Supabase** (PostgreSQL) comme backend.

## Architecture

Le modèle suit une architecture relationnelle avec :
- **Hiérarchie géographique** : Régions → Districts → Communes
- **Données financières flexibles** : Tableaux dynamiques et configurables
- **Gestion des utilisateurs** : Rôles et permissions via Supabase Auth
- **Traçabilité** : Historique des modifications et analytics

## Fichiers du modèle

1. **schema.sql** - Schéma SQL complet pour Supabase
2. **mcd.md** - Modèle Conceptuel de Données (description détaillée)
3. **seed-data.sql** - Données d'exemple pour tests
4. **policies.sql** - Politiques Row Level Security (RLS) de Supabase

## Entités Principales

### 1. Collectivités Territoriales
- `regions` - Régions de Madagascar
- `districts` - Districts (départements)
- `communes` - Communes

### 2. Données Minières
- `projets_miniers` - Projets d'extraction minière
- `revenus_miniers` - Revenus reçus par les collectivités

### 3. Comptes Administratifs
- `comptes_administratifs` - Comptes annuels par collectivité
- `rubriques_budgetaires` - Catalogue des rubriques (recettes/dépenses)
- `lignes_budgetaires` - Lignes de données financières
- `colonnes_dynamiques` - Configuration des colonnes des tableaux

### 4. Gestion du Contenu
- `documents` - Fichiers Excel/Word téléchargeables
- `newsletter_subscribers` - Abonnés à la newsletter
- `analytics` - Statistiques de visite et téléchargements

### 5. Utilisateurs (via Supabase Auth)
- `profiles` - Profils utilisateurs étendus
- `user_roles` - Rôles (administrateur, éditeur)

## Technologies

- **Base de données** : PostgreSQL (via Supabase)
- **Authentification** : Supabase Auth
- **Stockage fichiers** : Supabase Storage
- **Row Level Security** : Politiques RLS pour la sécurité
- **Realtime** : Supabase Realtime pour les mises à jour en temps réel

## Mise en œuvre

Voir le fichier `IMPLEMENTATION.md` pour les instructions détaillées de déploiement.
