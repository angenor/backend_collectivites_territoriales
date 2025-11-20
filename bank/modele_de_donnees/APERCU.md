# Aperçu du Modèle de Données

## Résumé Exécutif

Ce modèle de données a été conçu pour la **Plateforme Numérique de Suivi de l'Utilisation des Revenus Miniers des Collectivités Territoriales** à Madagascar, dans le cadre du projet PCQVP/TI Madagascar.

### Objectifs
- ✅ Renforcer la transparence financière
- ✅ Réduire les risques de détournement de fonds
- ✅ Accroître la redevabilité des acteurs locaux

### Technologies
- **Backend** : Supabase (PostgreSQL + Auth + Storage + Realtime)
- **Frontend** : Nuxt 4 + Vue 3 + Tailwind CSS
- **Sécurité** : Row Level Security (RLS) avec politiques granulaires

---

## Fichiers Créés

### 1. README.md
**Description** : Documentation principale du modèle
**Contenu** : Vue d'ensemble, architecture, entités principales, technologies utilisées

### 2. schema.sql (1200+ lignes)
**Description** : Schéma SQL complet pour Supabase
**Contenu** :
- 18 tables principales
- Relations avec clés étrangères
- Triggers et fonctions PostgreSQL
- Index pour performance
- 2 vues utiles
- Contraintes métier

**Tables créées** :
1. `regions` - Régions de Madagascar
2. `districts` - Districts (départements)
3. `communes` - Communes bénéficiaires
4. `projets_miniers` - Projets d'extraction
5. `revenus_miniers` - Revenus versés aux collectivités
6. `comptes_administratifs` - Comptes annuels
7. `categories_rubriques` - Catégories budgétaires
8. `rubriques_budgetaires` - Catalogue des rubriques
9. `colonnes_dynamiques` - Configuration des tableaux
10. `lignes_budgetaires` - Données financières
11. `documents` - Fichiers téléchargeables
12. `newsletter_subscribers` - Abonnés
13. `analytics_visites` - Statistiques de visite
14. `analytics_telechargements` - Statistiques de téléchargement
15. `profiles` - Profils utilisateurs
16. `activity_logs` - Journal d'audit
17. `messages_securises` - Messagerie sécurisée

### 3. policies.sql (850+ lignes)
**Description** : Politiques de sécurité Row Level Security
**Contenu** :
- Activation RLS sur toutes les tables
- 50+ politiques de sécurité granulaires
- Fonctions utilitaires (is_admin, can_edit)
- Triggers pour création automatique de profils
- Triggers pour journalisation des activités
- Grants de permissions

**Principes de sécurité** :
- Données publiques accessibles sans authentification
- Données en brouillon visibles uniquement par le créateur
- Administrateurs : accès complet
- Éditeurs : création et modification
- Lecteurs : lecture uniquement

### 4. seed-data.sql (400+ lignes)
**Description** : Données d'exemple pour tests
**Contenu** :
- 6 régions
- 6 districts
- 6 communes
- 3 projets miniers
- Revenus miniers (2023-2024)
- 50+ rubriques budgétaires
- 1 compte administratif complet avec lignes
- 3 abonnés newsletter

### 5. mcd.md (1500+ lignes)
**Description** : Modèle Conceptuel de Données détaillé
**Contenu** :
- Description de chaque entité
- Attributs et types de données
- Relations entre entités
- Diagrammes textuels
- Règles de validation
- Stratégie de stockage
- Optimisations de performance
- Évolutions futures

### 6. IMPLEMENTATION.md (1000+ lignes)
**Description** : Guide complet d'implémentation
**Contenu** :
- 10 étapes détaillées
- Configuration Supabase
- Configuration Nuxt
- Exemples de code
- Tests fonctionnels
- Optimisations
- Déploiement production
- Dépannage

### 7. erd-diagram.md (600+ lignes)
**Description** : Diagrammes Entité-Relation au format Mermaid
**Contenu** :
- 6 diagrammes ERD
- Diagramme complet simplifié
- Diagrammes par domaine fonctionnel
- Flux de données
- Légende complète
- Notes techniques

### 8. APERCU.md (ce fichier)
**Description** : Résumé et vue d'ensemble du projet

---

## Statistiques du Modèle

### Tables
- **Total** : 17 tables + 2 vues
- **Collectivités** : 3 tables (hiérarchie géographique)
- **Finances** : 6 tables (comptes, rubriques, lignes)
- **Documents** : 1 table
- **Analytics** : 2 tables
- **Utilisateurs** : 2 tables
- **Newsletter** : 1 table
- **Messages** : 1 table

### Champs
- **Total estimé** : ~250 colonnes
- **Types UUID** : Tous les ID
- **Types JSONB** : 6 champs (données flexibles)
- **Horodatage** : created_at/updated_at sur 15 tables

### Relations
- **One-to-Many** : 25+ relations
- **Hiérarchiques** : 3 (région→district→commune, rubriques parentes)
- **Polymorphiques** : 1 (comptes peuvent être liés à commune/district/région)

### Index
- **Index PK** : 17 (automatiques)
- **Index FK** : 20+ (pour jointures)
- **Index GIN** : 4 (pour JSON et full-text)
- **Index trigrammes** : 2 (recherche floue)

### Triggers
- **update_updated_at** : 11 triggers (mise à jour automatique)
- **increment_download_count** : 1 trigger (compteur téléchargements)
- **calculer_valeurs_derivees** : 1 trigger (calculs automatiques)
- **log_activity** : 4 triggers (audit trail)
- **handle_new_user** : 1 trigger (création profil)

### Politiques RLS
- **Total** : 50+ politiques
- **Lecture publique** : 10 politiques
- **Lecture authentifiée** : 15 politiques
- **Modification** : 20 politiques
- **Suppression** : 5 politiques

---

## Structure des Données Financières

### Tableau Dynamique

Le modèle permet des tableaux entièrement configurables :

```json
{
  "colonnes": [
    "budget_primitif",
    "budget_additionnel",
    "modifications",
    "previsions_definitives",
    "or_admis",
    "recouvrement",
    "reste_recouvrer",
    "taux_execution"
  ],
  "rubriques": [
    {
      "code": "R-1",
      "intitule": "RECETTES FISCALES",
      "niveau": 1,
      "sous_rubriques": [...]
    }
  ]
}
```

### Hiérarchie des Rubriques

```
RECETTES FISCALES (R-1)
├── IMPOTS SUR LES REVENUS (R-1-1)
│   └── Impôt synthétique (R-1-1-1)
├── IMPOTS SUR LE PATRIMOINE (R-1-2)
│   ├── IFT (R-1-2-1)
│   └── IFPB (R-1-2-2)
└── IMPOTS SUR BIENS ET SERVICES (R-1-3)
    ├── Taxes publicité (R-1-3-1)
    └── Taxe abattage (R-1-3-2)
```

---

## Points Clés du Modèle

### 🎯 Flexibilité
- **Tableaux dynamiques** : Colonnes et lignes configurables sans coder
- **Stockage JSON** : Données financières dans un format flexible
- **Hiérarchies** : Support de structures hiérarchiques (rubriques, géographie)

### 🔒 Sécurité
- **RLS activé** : Toutes les tables protégées
- **Rôles multiples** : Administrateur, Éditeur, Lecteur
- **Audit complet** : Toutes les actions tracées dans activity_logs
- **Chiffrement** : Support pour messages chiffrés

### 📊 Analytics
- **Visites** : Tracking des consultations par collectivité
- **Téléchargements** : Compteur automatique
- **Géolocalisation** : Pays et ville des visiteurs
- **Session tracking** : Suivi des parcours utilisateurs

### 🚀 Performance
- **Index optimisés** : Sur toutes les FK et champs de recherche
- **Vues dénormalisées** : Pour requêtes fréquentes
- **Triggers efficaces** : Calculs automatiques au niveau DB
- **Cache-friendly** : Structure adaptée au caching

### 📱 Extensibilité
- **Supabase Realtime** : Support des mises à jour en temps réel
- **Supabase Storage** : Gestion des fichiers intégrée
- **API automatique** : PostgREST génère API REST automatiquement
- **GraphQL ready** : Support GraphQL via pg_graphql

---

## Cas d'Usage Principaux

### 1. Consultation Publique
```
Visiteur → Sélectionne Région → District → Commune
→ Visualise compte administratif 2024
→ Télécharge tableau Excel
→ Stats enregistrées automatiquement
```

### 2. Saisie de Données (Éditeur)
```
Éditeur se connecte → Choisit commune + année
→ Crée/modifie lignes budgétaires
→ Calculs automatiques (reste à recouvrer, taux exécution)
→ Valide le compte → Admin publie
→ Toutes actions loggées
```

### 3. Administration
```
Admin se connecte → Dashboard analytics
→ Voit toutes les activités (activity_logs)
→ Gère utilisateurs (change rôles)
→ Configure rubriques/colonnes
→ Modère messages sécurisés
```

---

## Prochaines Étapes Recommandées

### Phase 1 : Mise en Place (Semaines 1-2)
1. ✅ Créer projet Supabase
2. ✅ Exécuter schema.sql
3. ✅ Exécuter policies.sql
4. ✅ Charger seed-data.sql
5. ✅ Configurer Storage buckets
6. ✅ Tester authentification

### Phase 2 : Développement Frontend (Semaines 3-6)
1. Composants de sélection (région/district/commune)
2. Tableau dynamique avec Vue
3. Export Excel/Word
4. Dashboard admin
5. Formulaires de saisie
6. Système de recherche

### Phase 3 : Intégrations (Semaines 7-8)
1. Newsletter (MailChimp ou SendGrid)
2. Analytics avancés (Google Analytics 4)
3. GlobalLeaks ou alternative
4. Backup automatique

### Phase 4 : Tests et Déploiement (Semaines 9-10)
1. Tests unitaires et E2E
2. Tests de charge
3. Audit sécurité
4. Formation utilisateurs
5. Déploiement production
6. Monitoring

---

## Ressources et Support

### Documentation Interne
- `README.md` - Vue d'ensemble
- `mcd.md` - Détails du modèle
- `IMPLEMENTATION.md` - Guide d'implémentation
- `erd-diagram.md` - Diagrammes visuels

### Documentation Externe
- [Supabase Docs](https://supabase.com/docs)
- [PostgreSQL Docs](https://www.postgresql.org/docs/)
- [Nuxt 3 Docs](https://nuxt.com)

### Support
- Email : vramaherison@transparency.mg
- Projet GitHub : (à créer)
- Documentation projet : `/bank/cahier_des_charges/`

---

## Licence et Crédits

**Projet** : Plateforme de Suivi des Revenus Miniers
**Client** : PCQVP Madagascar / TI Madagascar
**Contexte** : Projet "Minerais critiques : justice fiscale et redistribution de revenus"
**Année** : 2025
**Technologies** : Supabase, Nuxt 4, Vue 3, PostgreSQL

---

## Changelog

### Version 1.0 (2025-10-31)
- ✅ Création du modèle de données complet
- ✅ Schéma SQL avec 17 tables
- ✅ Politiques RLS complètes
- ✅ Documentation exhaustive
- ✅ Données d'exemple
- ✅ Guide d'implémentation
- ✅ Diagrammes ERD

### Prochaines versions prévues
- v1.1 : Ajout de vues matérialisées pour performance
- v1.2 : Support multi-langues (FR/MG/EN)
- v1.3 : Intégration API gouvernementale
- v2.0 : Dashboard BI avancé

---

## Contact

Pour toute question sur ce modèle de données :

**Responsable Technique** : TI Madagascar
**Email** : vramaherison@transparency.mg
**Date limite soumission** : 24 août 2025
**Livraison estimée** : 30 novembre 2025

---

**Note** : Ce modèle de données est prêt pour l'implémentation. Tous les fichiers SQL peuvent être exécutés directement dans Supabase. Consultez `IMPLEMENTATION.md` pour les instructions détaillées.
