# Diagramme Entité-Relation (ERD)

Ce fichier contient les diagrammes ERD du modèle de données au format Mermaid.

## Diagramme Complet Simplifié

```mermaid
erDiagram
    REGION ||--o{ DISTRICT : contient
    DISTRICT ||--o{ COMMUNE : contient

    COMMUNE ||--o{ PROJET_MINIER : "a des projets"
    COMMUNE ||--o{ REVENU_MINIER : "reçoit"
    COMMUNE ||--o{ COMPTE_ADMINISTRATIF : "a des comptes"

    PROJET_MINIER ||--o{ REVENU_MINIER : génère

    COMPTE_ADMINISTRATIF ||--o{ LIGNE_BUDGETAIRE : contient
    COMPTE_ADMINISTRATIF ||--o{ DOCUMENT : "a des documents"

    RUBRIQUE_BUDGETAIRE ||--o{ LIGNE_BUDGETAIRE : "classifie"
    CATEGORIE_RUBRIQUE ||--o{ RUBRIQUE_BUDGETAIRE : "regroupe"

    REGION {
        uuid id PK
        string code UK
        string nom
        int population
        decimal superficie
        string chef_lieu
    }

    DISTRICT {
        uuid id PK
        uuid region_id FK
        string code UK
        string nom
        int population
        decimal superficie
    }

    COMMUNE {
        uuid id PK
        uuid district_id FK
        string code UK
        string nom
        string type
        int population
        string maire
    }

    PROJET_MINIER {
        uuid id PK
        string code UK
        string nom
        string type_minerai
        string societe_exploitante
        string statut
    }

    REVENU_MINIER {
        uuid id PK
        uuid projet_minier_id FK
        uuid commune_id FK
        int annee
        int trimestre
        string type_revenu
        decimal montant
    }

    COMPTE_ADMINISTRATIF {
        uuid id PK
        uuid commune_id FK
        int annee
        string statut
        date date_publication
    }

    LIGNE_BUDGETAIRE {
        uuid id PK
        uuid compte_administratif_id FK
        uuid rubrique_id FK
        jsonb valeurs
    }

    RUBRIQUE_BUDGETAIRE {
        uuid id PK
        string code UK
        string intitule
        string type
        string section
        int niveau
    }
```

## Diagramme: Hiérarchie Géographique

```mermaid
erDiagram
    REGION ||--o{ DISTRICT : "1 région contient N districts"
    DISTRICT ||--o{ COMMUNE : "1 district contient N communes"

    REGION {
        uuid id PK
        string code UK "Code région (ex: ANA, VAK)"
        string nom "Nom de la région"
        int population "Nombre habitants"
        decimal superficie "Superficie en km²"
        string chef_lieu "Ville principale"
        timestamp created_at
        timestamp updated_at
    }

    DISTRICT {
        uuid id PK
        uuid region_id FK "Référence vers région"
        string code UK "Code district"
        string nom "Nom du district"
        int population
        decimal superficie
        string chef_lieu
        timestamp created_at
        timestamp updated_at
    }

    COMMUNE {
        uuid id PK
        uuid district_id FK "Référence vers district"
        string code UK "Code commune"
        string nom "Nom de la commune"
        string type "urbaine ou rurale"
        int population
        decimal superficie
        string maire "Nom du maire"
        string contact_email
        string contact_telephone
        timestamp created_at
        timestamp updated_at
    }
```

## Diagramme: Projets Miniers et Revenus

```mermaid
erDiagram
    REGION ||--o{ PROJET_MINIER : localise
    DISTRICT ||--o{ PROJET_MINIER : localise
    COMMUNE ||--o{ PROJET_MINIER : localise

    PROJET_MINIER ||--o{ REVENU_MINIER : génère
    COMMUNE ||--o{ REVENU_MINIER : reçoit

    PROJET_MINIER {
        uuid id PK
        string nom "Nom du projet"
        string code UK "Code unique"
        string type_minerai "graphite, ilménite, etc."
        string societe_exploitante
        uuid region_id FK
        uuid district_id FK
        uuid commune_id FK
        date date_debut
        date date_fin
        string statut "en_cours, suspendu, termine"
        jsonb coordonnees_gps
        timestamp created_at
        timestamp updated_at
    }

    REVENU_MINIER {
        uuid id PK
        uuid projet_minier_id FK
        uuid commune_id FK
        uuid district_id FK
        uuid region_id FK
        int annee "Année fiscale"
        int trimestre "1 à 4"
        string type_revenu "ristourne, redevance"
        decimal montant "Montant en Ariary"
        date date_versement
        text description
        timestamp created_at
        timestamp updated_at
    }
```

## Diagramme: Comptes Administratifs

```mermaid
erDiagram
    COMMUNE ||--o{ COMPTE_ADMINISTRATIF : "a des comptes annuels"
    COMPTE_ADMINISTRATIF ||--o{ LIGNE_BUDGETAIRE : "contient des lignes"
    COMPTE_ADMINISTRATIF ||--o{ DOCUMENT : "a des documents"

    RUBRIQUE_BUDGETAIRE ||--o{ LIGNE_BUDGETAIRE : "classifie"
    CATEGORIE_RUBRIQUE ||--o{ RUBRIQUE_BUDGETAIRE : "regroupe"
    RUBRIQUE_BUDGETAIRE ||--o{ RUBRIQUE_BUDGETAIRE : "parent-enfant"

    COMPTE_ADMINISTRATIF {
        uuid id PK
        uuid commune_id FK
        int annee UK "Année du compte"
        string statut "brouillon, valide, publie"
        date date_validation
        date date_publication
        uuid validateur_id FK
        uuid created_by FK
        text notes
        timestamp created_at
        timestamp updated_at
    }

    CATEGORIE_RUBRIQUE {
        uuid id PK
        string code UK
        string nom
        string type "recette, depense, equilibre"
        string section "fonctionnement, investissement"
        uuid parent_id FK "Hiérarchie"
        int ordre
    }

    RUBRIQUE_BUDGETAIRE {
        uuid id PK
        string code UK "Code comptable"
        text intitule "Libellé de la rubrique"
        uuid categorie_id FK
        string type "recette, depense"
        string section "fonctionnement, investissement"
        uuid parent_id FK "Rubrique parente"
        int niveau "1, 2, 3..."
        int ordre "Ordre d'affichage"
        boolean est_calculee
        text formule_calcul
        boolean est_active
    }

    LIGNE_BUDGETAIRE {
        uuid id PK
        uuid compte_administratif_id FK
        uuid rubrique_id FK
        jsonb valeurs "Données JSON flexibles"
        text notes
        uuid updated_by FK
        timestamp created_at
        timestamp updated_at
    }

    COLONNE_DYNAMIQUE {
        uuid id PK
        string code UK
        string nom "Nom affiché"
        string type_donnee "montant, pourcentage, texte"
        int ordre
        boolean est_calculee
        text formule_calcul
        boolean est_active
    }
```

## Diagramme: Gestion des Utilisateurs

```mermaid
erDiagram
    AUTH_USERS ||--|| PROFILE : "a un profil"
    PROFILE ||--o{ ACTIVITY_LOG : "effectue des actions"
    PROFILE ||--o{ MESSAGE_SECURISE : "envoie/reçoit"

    AUTH_USERS {
        uuid id PK "Géré par Supabase Auth"
        string email UK
        timestamp created_at
    }

    PROFILE {
        uuid id PK-FK "Même ID que auth.users"
        string email UK
        string nom
        string prenom
        string role "administrateur, editeur, lecteur"
        string organisation
        string telephone
        string avatar_url
        jsonb permissions
        boolean est_actif
        timestamp derniere_connexion
        timestamp created_at
        timestamp updated_at
    }

    ACTIVITY_LOG {
        uuid id PK
        uuid user_id FK
        string action "create, update, delete"
        string table_name
        uuid record_id
        jsonb old_values
        jsonb new_values
        inet ip_address
        timestamp created_at
    }

    MESSAGE_SECURISE {
        uuid id PK
        uuid expediteur_id FK
        uuid destinataire_id FK
        string sujet
        text contenu
        boolean est_chiffre
        boolean est_lu
        date date_lecture
        jsonb fichiers_joints
        timestamp expiration_date
        timestamp created_at
    }
```

## Diagramme: Documents et Analytics

```mermaid
erDiagram
    COMPTE_ADMINISTRATIF ||--o{ DOCUMENT : "a des documents"
    DOCUMENT ||--o{ ANALYTICS_TELECHARGEMENT : "trackés par"
    COMMUNE ||--o{ ANALYTICS_VISITE : "visitées"

    DOCUMENT {
        uuid id PK
        uuid compte_administratif_id FK
        string titre
        string type_fichier "excel, word, pdf"
        string fichier_url "URL Supabase Storage"
        string fichier_nom
        int taille_fichier
        int nombre_telechargements "Auto-incrémenté"
        boolean est_public
        array tags
        uuid uploaded_by FK
        timestamp created_at
        timestamp updated_at
    }

    ANALYTICS_VISITE {
        uuid id PK
        string session_id
        text page_url
        uuid commune_id FK
        uuid district_id FK
        uuid region_id FK
        text user_agent
        inet ip_address
        text referrer
        string pays
        string ville
        int duree_visite "en secondes"
        timestamp created_at
    }

    ANALYTICS_TELECHARGEMENT {
        uuid id PK
        uuid document_id FK
        string session_id
        uuid user_id FK
        inet ip_address
        text user_agent
        timestamp created_at
    }

    NEWSLETTER_SUBSCRIBER {
        uuid id PK
        string email UK
        string nom
        string prenom
        string organisation
        string statut "actif, inactif, desabonne"
        jsonb preferences
        string token_confirmation
        timestamp date_confirmation
        timestamp created_at
        timestamp updated_at
    }
```

## Flux de Données: Consultation d'un Compte

```mermaid
flowchart TD
    A[Utilisateur arrive sur la plateforme] --> B[Sélectionne une RÉGION]
    B --> C[Charge les DISTRICTS de la région]
    C --> D[Utilisateur sélectionne un DISTRICT]
    D --> E[Charge les COMMUNES du district]
    E --> F[Utilisateur sélectionne une COMMUNE]
    F --> G[Charge le COMPTE_ADMINISTRATIF de l'année]
    G --> H{Compte trouvé et publié?}
    H -->|Oui| I[Charge les LIGNES_BUDGETAIRES]
    H -->|Non| J[Affiche message: Aucune donnée disponible]
    I --> K[Charge les RUBRIQUES_BUDGETAIRES]
    K --> L[Charge la config COLONNES_DYNAMIQUES]
    L --> M[Génère le tableau dynamique]
    M --> N[Affiche le tableau à l'utilisateur]
    N --> O{Utilisateur télécharge?}
    O -->|Oui| P[Génère fichier Excel/Word]
    P --> Q[Enregistre ANALYTICS_TELECHARGEMENT]
    Q --> R[Incrémente compteur DOCUMENT]
    O -->|Non| S[Enregistre ANALYTICS_VISITE]
```

## Flux de Données: Création d'un Compte

```mermaid
flowchart TD
    A[Éditeur se connecte] --> B[Vérifie rôle dans PROFILE]
    B --> C{Peut éditer?}
    C -->|Non| D[Accès refusé]
    C -->|Oui| E[Choisit COMMUNE + ANNEE]
    E --> F{Compte existe déjà?}
    F -->|Oui| G[Charge le compte existant]
    F -->|Non| H[Crée nouveau COMPTE_ADMINISTRATIF]
    G --> I[Affiche formulaire d'édition]
    H --> I
    I --> J[Éditeur remplit les LIGNES_BUDGETAIRES]
    J --> K[Sauvegarde dans valeurs JSON]
    K --> L{Trigger calcul auto}
    L --> M[Calcule reste_recouvrer, taux_execution]
    M --> N[Enregistre dans ACTIVITY_LOG]
    N --> O{Statut = publié?}
    O -->|Oui| P[RLS: Visible publiquement]
    O -->|Non| Q[RLS: Visible uniquement par créateur]
```

---

## Légende

### Types de Relations
- `||--o{` : Un à plusieurs (1:N)
- `||--||` : Un à un (1:1)
- `o{--o{` : Plusieurs à plusieurs (N:M)

### Contraintes
- `PK` : Primary Key (Clé primaire)
- `FK` : Foreign Key (Clé étrangère)
- `UK` : Unique Key (Contrainte d'unicité)

### Types de Données
- `uuid` : Identifiant universel unique
- `string` : Chaîne de caractères
- `text` : Texte long
- `int` : Nombre entier
- `decimal` : Nombre décimal
- `boolean` : Vrai/Faux
- `date` : Date
- `timestamp` : Date et heure
- `jsonb` : JSON binaire (PostgreSQL)
- `inet` : Adresse IP
- `array` : Tableau

---

## Visualisation en ligne

Pour visualiser ces diagrammes :

1. **Copier le code Mermaid**
2. **Coller dans un éditeur Mermaid en ligne** :
   - [Mermaid Live Editor](https://mermaid.live)
   - [GitHub](https://github.com) (supporte Mermaid nativement dans les README.md)
   - [VS Code](https://marketplace.visualstudio.com/items?itemName=bierner.markdown-mermaid) avec extension Markdown Preview Mermaid Support

3. **Exporter en image** :
   - PNG, SVG, ou PDF pour documentation

---

## Notes Techniques

### Performances
- Tous les `id` sont indexés automatiquement (PK)
- Les `FK` ont des index pour optimiser les jointures
- Les colonnes JSON (`valeurs`, `preferences`) ont des index GIN
- Les champs `nom` et `intitule` ont des index trigram pour la recherche full-text

### Sécurité
- Row Level Security (RLS) activé sur toutes les tables
- Les politiques RLS contrôlent l'accès selon le rôle utilisateur
- Les données sensibles sont protégées (ex: service_role_key)
- Audit trail complet via `activity_logs`

### Scalabilité
- Design normalisé pour éviter la redondance
- Vues matérialisées possibles pour les agrégations
- Partitionnement de tables possible (par année)
- Support natif PostgreSQL pour millions de lignes
