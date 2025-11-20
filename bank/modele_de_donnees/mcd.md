# Modèle Conceptuel de Données (MCD)

## Vue d'ensemble

Le modèle de données est organisé autour de **11 domaines fonctionnels** pour supporter la plateforme de suivi des revenus miniers des collectivités territoriales à Madagascar.

## 1. Hiérarchie Géographique

### Entités

#### REGION
- **Description** : Régions administratives de Madagascar
- **Attributs** :
  - `id` : Identifiant unique (UUID)
  - `code` : Code unique de la région (ex: "ANA", "VAK")
  - `nom` : Nom de la région
  - `description` : Description détaillée
  - `population` : Nombre d'habitants
  - `superficie` : Superficie en km²
  - `chef_lieu` : Ville principale
  - `created_at`, `updated_at` : Horodatage

#### DISTRICT
- **Description** : Districts (départements) administratifs
- **Attributs** :
  - `id` : Identifiant unique (UUID)
  - `region_id` : Référence vers la région
  - `code` : Code unique du district
  - `nom` : Nom du district
  - `population`, `superficie`, `chef_lieu`
  - `created_at`, `updated_at`

#### COMMUNE
- **Description** : Communes bénéficiaires des revenus miniers
- **Attributs** :
  - `id` : Identifiant unique (UUID)
  - `district_id` : Référence vers le district
  - `code` : Code unique de la commune
  - `nom` : Nom de la commune
  - `type` : 'urbaine' | 'rurale'
  - `population`, `superficie`
  - `maire` : Nom du maire
  - `contact_email`, `contact_telephone`
  - `created_at`, `updated_at`

### Relations
```
REGION (1) ──< (N) DISTRICT (1) ──< (N) COMMUNE
```

---

## 2. Projets Miniers et Revenus

### Entités

#### PROJET_MINIER
- **Description** : Projets d'extraction de minerais critiques
- **Attributs** :
  - `id` : Identifiant unique (UUID)
  - `nom` : Nom du projet
  - `code` : Code unique
  - `type_minerai` : Type de minerai (graphite, ilménite, cobalt, nickel, etc.)
  - `societe_exploitante` : Nom de la société
  - `region_id`, `district_id`, `commune_id` : Localisation
  - `date_debut`, `date_fin` : Période d'exploitation
  - `statut` : 'en_cours' | 'suspendu' | 'termine' | 'planifie'
  - `description`
  - `coordonnees_gps` : Coordonnées GPS (JSON)
  - `created_at`, `updated_at`

#### REVENU_MINIER
- **Description** : Revenus versés aux collectivités (ristournes et redevances)
- **Attributs** :
  - `id` : Identifiant unique (UUID)
  - `projet_minier_id` : Référence vers le projet
  - `commune_id`, `district_id`, `region_id` : Bénéficiaire
  - `annee` : Année fiscale
  - `trimestre` : Trimestre (1-4)
  - `type_revenu` : 'ristourne' | 'redevance' | 'autre'
  - `montant` : Montant en Ariary
  - `date_versement` : Date du versement
  - `description`
  - `created_at`, `updated_at`

### Relations
```
PROJET_MINIER (1) ──< (N) REVENU_MINIER
COMMUNE (1) ──< (N) REVENU_MINIER
DISTRICT (1) ──< (N) REVENU_MINIER
REGION (1) ──< (N) REVENU_MINIER
```

---

## 3. Comptes Administratifs

### Entités

#### COMPTE_ADMINISTRATIF
- **Description** : Compte administratif annuel d'une collectivité
- **Attributs** :
  - `id` : Identifiant unique (UUID)
  - `commune_id` / `district_id` / `region_id` : Collectivité (un seul parmi les trois)
  - `annee` : Année fiscale
  - `statut` : 'brouillon' | 'valide' | 'publie' | 'archive'
  - `date_validation`, `date_publication`
  - `validateur_id` : Utilisateur validateur
  - `notes`
  - `created_at`, `updated_at`, `created_by`

#### CATEGORIE_RUBRIQUE
- **Description** : Catégories hiérarchiques des rubriques budgétaires
- **Attributs** :
  - `id` : Identifiant unique (UUID)
  - `code` : Code de la catégorie
  - `nom` : Nom de la catégorie
  - `type` : 'recette' | 'depense' | 'equilibre'
  - `section` : 'fonctionnement' | 'investissement' | 'ordre' | 'equilibre'
  - `parent_id` : Catégorie parente (arborescence)
  - `ordre` : Ordre d'affichage
  - `description`
  - `created_at`

#### RUBRIQUE_BUDGETAIRE
- **Description** : Catalogue des rubriques budgétaires (recettes et dépenses)
- **Attributs** :
  - `id` : Identifiant unique (UUID)
  - `code` : Code comptable
  - `intitule` : Libellé de la rubrique
  - `categorie_id` : Référence vers la catégorie
  - `type` : 'recette' | 'depense' | 'equilibre'
  - `section` : 'fonctionnement' | 'investissement' | 'ordre' | 'equilibre'
  - `parent_id` : Rubrique parente (hiérarchie)
  - `niveau` : Niveau hiérarchique (1, 2, 3...)
  - `ordre` : Ordre d'affichage
  - `est_calculee` : Indique si la valeur est calculée automatiquement
  - `formule_calcul` : Formule de calcul
  - `est_active` : Actif/Inactif
  - `description`
  - `created_at`, `updated_at`

**Exemples de rubriques** :
- Recettes de fonctionnement :
  - Impôts sur les revenus - Impôt synthétique
  - Impôts fonciers sur les terrains (IFT)
  - Taxes sur la publicité
  - Dotations globales
  - Produits des ristournes
- Dépenses de fonctionnement :
  - Charges de personnel
  - Achats de biens
  - Services et charges permanentes
- Recettes d'investissement :
  - Subventions d'équipement
  - Cessions d'immobilisations
- Dépenses d'investissement :
  - Immobilisations corporelles
  - Immobilisations incorporelles

#### COLONNE_DYNAMIQUE
- **Description** : Configuration des colonnes pour les tableaux dynamiques
- **Attributs** :
  - `id` : Identifiant unique (UUID)
  - `code` : Code de la colonne
  - `nom` : Nom affiché
  - `type_donnee` : 'montant' | 'pourcentage' | 'texte' | 'date' | 'nombre'
  - `ordre` : Ordre d'affichage
  - `est_calculee` : Colonne calculée automatiquement
  - `formule_calcul` : Formule de calcul
  - `format_affichage` : Format d'affichage (ex: "0,0.00")
  - `est_active` : Actif/Inactif
  - `description`
  - `created_at`, `updated_at`

**Colonnes standards** :
1. COMPTE
2. BUDGET PRIMITIF
3. BUDGET ADDITIONNEL
4. MODIFICATIONS +/-
5. PREVISIONS DEFINITIVES (calculé)
6. ENGAGEMENT / OR ADMIS
7. MANDAT ADMIS / RECOUVREMENT
8. PAIEMENT
9. RESTE A RECOUVRER / RESTE A PAYER (calculé)
10. TAUX D'EXECUTION (calculé)

#### LIGNE_BUDGETAIRE
- **Description** : Données financières pour chaque rubrique et compte
- **Attributs** :
  - `id` : Identifiant unique (UUID)
  - `compte_administratif_id` : Référence vers le compte
  - `rubrique_id` : Référence vers la rubrique
  - `valeurs` : Données JSON flexibles
    ```json
    {
      "budget_primitif": 1000000,
      "budget_additionnel": 200000,
      "modifications": 50000,
      "previsions_definitives": 1250000,
      "or_admis": 1100000,
      "recouvrement": 950000,
      "reste_recouvrer": 150000,
      "taux_execution": 88.0
    }
    ```
  - `notes`
  - `created_at`, `updated_at`, `updated_by`

### Relations
```
COMPTE_ADMINISTRATIF (1) ──< (N) LIGNE_BUDGETAIRE
RUBRIQUE_BUDGETAIRE (1) ──< (N) LIGNE_BUDGETAIRE
CATEGORIE_RUBRIQUE (1) ──< (N) RUBRIQUE_BUDGETAIRE
RUBRIQUE_BUDGETAIRE (1) ──< (N) RUBRIQUE_BUDGETAIRE (parent-enfant)
```

---

## 4. Documents et Fichiers

### Entités

#### DOCUMENT
- **Description** : Documents téléchargeables (Excel, Word, PDF)
- **Attributs** :
  - `id` : Identifiant unique (UUID)
  - `compte_administratif_id` : Référence vers le compte
  - `titre` : Titre du document
  - `description`
  - `type_fichier` : 'excel' | 'word' | 'pdf' | 'autre'
  - `fichier_url` : URL Supabase Storage
  - `fichier_nom` : Nom du fichier
  - `taille_fichier` : Taille en octets
  - `nombre_telechargements` : Compteur
  - `est_public` : Public/Privé
  - `tags` : Array de tags pour recherche
  - `uploaded_by` : Utilisateur qui a uploadé
  - `created_at`, `updated_at`

### Relations
```
COMPTE_ADMINISTRATIF (1) ──< (N) DOCUMENT
```

---

## 5. Newsletter

### Entités

#### NEWSLETTER_SUBSCRIBER
- **Description** : Abonnés à la newsletter
- **Attributs** :
  - `id` : Identifiant unique (UUID)
  - `email` : Email (unique)
  - `nom`, `prenom`
  - `organisation`
  - `statut` : 'actif' | 'inactif' | 'desabonne'
  - `preferences` : Préférences JSON
  - `token_confirmation` : Token pour confirmation email
  - `date_confirmation`
  - `created_at`, `updated_at`

---

## 6. Analytics

### Entités

#### ANALYTICS_VISITE
- **Description** : Statistiques des visites de la plateforme
- **Attributs** :
  - `id` : Identifiant unique (UUID)
  - `session_id` : Identifiant de session
  - `page_url` : URL visitée
  - `commune_id`, `district_id`, `region_id` : Collectivité consultée
  - `user_agent` : Navigateur
  - `ip_address` : Adresse IP
  - `referrer` : Page d'origine
  - `pays`, `ville` : Géolocalisation
  - `duree_visite` : Durée en secondes
  - `created_at`

#### ANALYTICS_TELECHARGEMENT
- **Description** : Statistiques des téléchargements de documents
- **Attributs** :
  - `id` : Identifiant unique (UUID)
  - `document_id` : Référence vers le document
  - `session_id` : Session
  - `user_id` : Utilisateur (si connecté)
  - `ip_address`
  - `user_agent`
  - `created_at`

### Relations
```
DOCUMENT (1) ──< (N) ANALYTICS_TELECHARGEMENT
```

---

## 7. Utilisateurs et Authentification

### Entités

#### PROFILE
- **Description** : Profils utilisateurs (extension de Supabase Auth)
- **Attributs** :
  - `id` : Identifiant unique (UUID) - référence auth.users
  - `email` : Email
  - `nom`, `prenom`
  - `role` : 'administrateur' | 'editeur' | 'lecteur'
  - `organisation`
  - `telephone`
  - `avatar_url`
  - `bio`
  - `permissions` : Permissions JSON spécifiques
  - `est_actif` : Actif/Inactif
  - `derniere_connexion`
  - `created_at`, `updated_at`

**Rôles et permissions** :
- **Administrateur** : Accès complet, gestion des utilisateurs, configuration
- **Éditeur** : Création et modification des comptes administratifs
- **Lecteur** : Consultation uniquement

#### ACTIVITY_LOG
- **Description** : Journal d'activité pour audit et traçabilité
- **Attributs** :
  - `id` : Identifiant unique (UUID)
  - `user_id` : Utilisateur
  - `action` : Type d'action ('create', 'update', 'delete', 'login', etc.)
  - `table_name` : Table concernée
  - `record_id` : ID de l'enregistrement
  - `old_values` : Anciennes valeurs (JSON)
  - `new_values` : Nouvelles valeurs (JSON)
  - `ip_address`
  - `user_agent`
  - `created_at`

---

## 8. Messagerie Sécurisée

### Entités

#### MESSAGE_SECURISE
- **Description** : Système de messagerie sécurisée interne (alternative à GlobalLeaks)
- **Attributs** :
  - `id` : Identifiant unique (UUID)
  - `expediteur_id` : Utilisateur expéditeur
  - `destinataire_id` : Utilisateur destinataire
  - `sujet` : Sujet du message
  - `contenu` : Contenu du message
  - `est_chiffre` : Message chiffré
  - `est_lu` : Lu/Non lu
  - `date_lecture`
  - `fichiers_joints` : Array d'URLs (JSON)
  - `expiration_date` : Date d'expiration
  - `created_at`

---

## 9. Vues et Requêtes Complexes

### V_HIERARCHIE_COLLECTIVITES
Vue dénormalisée de la hiérarchie complète : Commune → District → Région

### V_REVENUS_PAR_COLLECTIVITE
Vue agrégée des revenus miniers par collectivité et année

---

## 10. Fonctionnalités Automatiques

### Triggers

1. **update_updated_at_column** : Met à jour automatiquement le champ `updated_at`
2. **increment_download_count** : Incrémente le compteur de téléchargements
3. **calculer_valeurs_derivees** : Calcule automatiquement les valeurs dérivées (reste à recouvrer, taux d'exécution)

### Fonctions de Calcul

#### Calculs automatiques dans LIGNE_BUDGETAIRE :
- `previsions_definitives` = budget_primitif + budget_additionnel + modifications
- `reste_recouvrer` = or_admis - recouvrement
- `reste_payer` = mandat_admis - paiement
- `taux_execution` = (or_admis / previsions_definitives) × 100

---

## 11. Stratégie de Stockage

### Supabase Storage Buckets

1. **documents** : Fichiers Excel, Word, PDF
   - Organisation : `/comptes/{annee}/{collectivite_id}/`
   - Politique : Public ou protégé selon `documents.est_public`

2. **avatars** : Photos de profil utilisateurs
   - Organisation : `/avatars/{user_id}/`
   - Politique : Public

3. **messages-attachments** : Pièces jointes des messages sécurisés
   - Organisation : `/messages/{message_id}/`
   - Politique : Privé

---

## 12. Règles de Validation

### Contraintes Métier

1. **Unicité des comptes administratifs** : Un seul compte par collectivité et par année
2. **Hiérarchie géographique** : Une commune appartient à un seul district, un district à une seule région
3. **Type de collectivité** : Un compte administratif doit être lié à exactement un type de collectivité (commune XOR district XOR région)
4. **Revenus miniers** : Unicité par (projet, collectivité, année, trimestre, type_revenu)
5. **Lignes budgétaires** : Unicité par (compte_administratif, rubrique)

### Validations Front-End

- Email valide pour newsletter et utilisateurs
- Montants positifs pour les données financières
- Dates cohérentes (date_debut < date_fin)
- Format téléphone Madagascar (+261...)
- Taux d'exécution entre 0 et 200%

---

## 13. Performance et Optimisation

### Index
- Index sur toutes les clés étrangères
- Index sur les champs de recherche fréquents (annee, nom, code, type)
- Index GIN sur les colonnes JSON (valeurs, preferences, permissions)
- Index trigram (pg_trgm) pour la recherche full-text sur nom et intitule

### Dénormalisation
- Vue `v_hierarchie_collectivites` pour éviter les jointures répétées
- Vue `v_revenus_par_collectivite` pour les rapports agrégés

---

## 14. Sécurité - Row Level Security (RLS)

Les politiques RLS seront définies dans `policies.sql` :

### Politiques de base
- **Public** : Lecture des données publiées (comptes administratifs avec statut 'publie')
- **Éditeurs** : CRUD sur leurs propres comptes administratifs (brouillon, validé)
- **Administrateurs** : Accès complet
- **Authentifié** : Lecture de toutes les données, écriture selon le rôle

### Isolation des données
- Les utilisateurs ne voient que les données de leur organisation (si applicable)
- Les comptes en brouillon ne sont visibles que par leur créateur
- Les messages sécurisés sont visibles uniquement par expéditeur et destinataire

---

## Diagramme Entité-Relation (Simplifié)

```
┌──────────────┐
│   REGION     │
└──────┬───────┘
       │ 1
       │
       │ N
┌──────▼───────┐
│   DISTRICT   │
└──────┬───────┘
       │ 1
       │
       │ N
┌──────▼───────┐       ┌─────────────────┐
│   COMMUNE    │◄──────┤ PROJET_MINIER   │
└──────┬───────┘  N  1 └────────┬────────┘
       │                         │
       │ 1                       │ 1
       │                         │
       │ N                       │ N
┌──────▼───────────────┐  ┌─────▼──────────┐
│ COMPTE_ADMINISTRATIF │  │ REVENU_MINIER  │
└──────┬───────────────┘  └────────────────┘
       │ 1
       │
       │ N
┌──────▼─────────────┐
│ LIGNE_BUDGETAIRE   │
└──────┬─────────────┘
       │ N
       │
       │ 1
┌──────▼──────────────┐
│ RUBRIQUE_BUDGETAIRE │
└─────────────────────┘
```

---

## Évolutions Futures

### Phase 2
- Workflow de validation multi-niveaux
- Intégration API avec le système de comptabilité de l'État
- Export automatique vers OpenData
- Système de notifications en temps réel (via Supabase Realtime)

### Phase 3
- Dashboard d'analyse avancée
- Prédictions basées sur l'IA
- Comparaison inter-collectivités
- Application mobile (React Native + Supabase)
