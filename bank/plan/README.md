# Plan d'Implementation - BackOffice Admin

## Vue d'ensemble
BackOffice de gestion de la plateforme de suivi des revenus miniers des collectivites territoriales de Madagascar.

---

## 1. Gestion des Collectivites Territoriales

### 1.1 Gestion des Regions
- Lister toutes les regions
- Creer une nouvelle region
- Modifier une region existante
- Supprimer une region
- Rechercher/filtrer les regions

### 1.2 Gestion des Districts
- Lister tous les districts (avec filtre par region)
- Creer un nouveau district
- Modifier un district existant
- Supprimer un district
- Rechercher/filtrer les districts

### 1.3 Gestion des Communes
- Lister toutes les communes (avec filtre par district/region)
- Creer une nouvelle commune
- Modifier une commune existante
- Supprimer une commune
- Rechercher/filtrer les communes
- Filtrer par type (urbaine/rurale)

---

## 2. Gestion des Projets Miniers

### 2.1 Gestion des Projets
- Lister tous les projets miniers
- Creer un nouveau projet
- Modifier un projet existant
- Supprimer un projet
- Rechercher/filtrer par type de minerai, statut, localisation
- Visualiser la localisation GPS sur carte

### 2.2 Gestion des Revenus Miniers
- Lister tous les revenus (avec filtre par projet, collectivite, annee)
- Creer un nouveau revenu
- Modifier un revenu existant
- Supprimer un revenu
- Filtrer par type (ristourne/redevance), annee, trimestre
- Export des donnees (Excel/CSV)

---

## 3. Gestion des Comptes Administratifs

### 3.1 Comptes Administratifs
- Lister tous les comptes (avec filtre par collectivite, annee, statut)
- Creer un nouveau compte administratif
- Modifier un compte existant
- Supprimer un compte
- Changer le statut (brouillon -> valide -> publie -> archive)
- Valider un compte (avec workflow d'approbation)
- Publier un compte
- Visualiser l'historique des modifications

### 3.2 Categories de Rubriques
- Lister toutes les categories
- Creer une nouvelle categorie
- Modifier une categorie existante
- Supprimer une categorie
- Gerer la hierarchie (parent/enfant)
- Reorganiser l'ordre d'affichage

### 3.3 Rubriques Budgetaires
- Lister toutes les rubriques
- Creer une nouvelle rubrique
- Modifier une rubrique existante
- Supprimer une rubrique
- Gerer la hierarchie (niveaux)
- Activer/desactiver une rubrique
- Definir les formules de calcul
- Filtrer par type (recette/depense) et section

### 3.4 Colonnes Dynamiques
- Lister toutes les colonnes configurees
- Creer une nouvelle colonne
- Modifier une colonne existante
- Supprimer une colonne
- Activer/desactiver une colonne
- Definir les formules de calcul
- Reorganiser l'ordre d'affichage

### 3.5 Lignes Budgetaires
- Lister les lignes d'un compte administratif
- Creer/modifier les valeurs pour chaque rubrique
- Saisie en masse (import Excel)
- Visualiser les calculs automatiques
- Valider les donnees saisies
- Export des tableaux financiers

---

## 4. Gestion des Documents

### 4.1 Documents
- Lister tous les documents
- Uploader un nouveau document
- Modifier les metadonnees d'un document
- Supprimer un document
- Gerer les tags
- Gerer la visibilite (public/prive)
- Telecharger un document
- Visualiser les statistiques de telechargement

---

## 5. Gestion de la Newsletter

### 5.1 Abonnes
- Lister tous les abonnes
- Voir le detail d'un abonne
- Modifier le statut (actif/inactif/desabonne)
- Supprimer un abonne
- Filtrer par statut
- Export des listes d'abonnes

### 5.2 Envoi de Newsletter
- Creer une nouvelle newsletter
- Previsualiser avant envoi
- Envoyer a tous les abonnes actifs
- Envoyer a une selection d'abonnes
- Programmer l'envoi
- Historique des envois

---

## 6. Gestion des Utilisateurs

### 6.1 Profils Utilisateurs
- Lister tous les utilisateurs
- Creer un nouveau compte utilisateur
- Modifier un profil existant
- Supprimer/desactiver un utilisateur
- Gerer les roles (administrateur/editeur/lecteur)
- Gerer les permissions specifiques
- Reinitialiser le mot de passe
- Voir la derniere connexion

### 6.2 Journal d'Activite
- Consulter le journal d'audit
- Filtrer par utilisateur, action, date, table
- Voir les anciennes/nouvelles valeurs
- Export des logs

---

## 7. Analytics et Statistiques

### 7.1 Statistiques de Visites
- Tableau de bord des visites
- Filtrer par periode, page, collectivite
- Visualiser les graphiques de trafic
- Voir les sources de trafic (referrers)
- Geolocalisation des visiteurs

### 7.2 Statistiques de Telechargements
- Tableau de bord des telechargements
- Filtrer par document, periode
- Voir les documents les plus telecharges
- Export des statistiques

### 7.3 Tableaux de Bord
- Dashboard general (KPIs)
- Nombre total de collectivites
- Nombre de comptes administratifs par statut
- Total des revenus miniers par annee
- Projets miniers actifs
- Utilisateurs actifs
- Tendances et graphiques

---

## 8. Messagerie Securisee

### 8.1 Messages
- Boite de reception
- Envoyer un nouveau message
- Repondre a un message
- Marquer comme lu/non lu
- Joindre des fichiers
- Supprimer un message
- Filtrer par statut

---

## 9. Configuration et Parametres

### 9.1 Parametres Generaux
- Configuration de la plateforme
- Parametres SMTP pour emails
- Parametres de stockage
- Limites et quotas

### 9.2 Gestion des Permissions
- Definir les roles et permissions
- Matrice de permissions par role

### 9.3 Maintenance
- Voir l'etat du systeme
- Vider les caches
- Sauvegardes manuelles
- Voir les logs systeme

---

## 10. Fonctionnalites Transversales

### 10.1 Recherche Globale
- Recherche full-text dans toutes les entites
- Filtres avances
- Suggestions automatiques

### 10.2 Export de Donnees
- Export Excel/CSV pour toutes les listes
- Export PDF des rapports
- Export des comptes administratifs complets

### 10.3 Import de Donnees
- Import en masse (Excel/CSV)
- Validation des donnees
- Gestion des erreurs d'import
- Preview avant import

### 10.4 Notifications
- Notifications systeme
- Alertes sur actions importantes
- Historique des notifications

---

## Architecture des Pages du BackOffice

```
/admin
├── /dashboard                    # Tableau de bord principal
├── /collectivites
│   ├── /regions                  # CRUD Regions
│   ├── /districts                # CRUD Districts
│   └── /communes                 # CRUD Communes
├── /projets-miniers
│   ├── /projets                  # CRUD Projets
│   └── /revenus                  # CRUD Revenus miniers
├── /comptes-administratifs
│   ├── /comptes                  # CRUD Comptes
│   ├── /categories-rubriques     # CRUD Categories
│   ├── /rubriques                # CRUD Rubriques budgetaires
│   ├── /colonnes                 # CRUD Colonnes dynamiques
│   └── /saisie                   # Saisie des lignes budgetaires
├── /documents                    # Gestion des documents
├── /newsletter
│   ├── /abonnes                  # Gestion des abonnes
│   └── /envois                   # Envoi de newsletters
├── /utilisateurs
│   ├── /profils                  # CRUD Utilisateurs
│   └── /activite                 # Journal d'activite
├── /analytics
│   ├── /visites                  # Stats visites
│   └── /telechargements          # Stats telechargements
├── /messages                     # Messagerie securisee
└── /parametres                   # Configuration
```

---

## Ordre d'Implementation Recommande

### Phase 1 : Fondations (Semaines 1-2)
1. Layout BackOffice + Navigation
2. Dashboard principal
3. Authentification et gestion des roles
4. Gestion des utilisateurs

### Phase 2 : Donnees de Base (Semaines 3-4)
5. Gestion des regions
6. Gestion des districts
7. Gestion des communes
8. Gestion des projets miniers

### Phase 3 : Comptes Administratifs (Semaines 5-7)
9. Gestion des categories de rubriques
10. Gestion des rubriques budgetaires
11. Gestion des colonnes dynamiques
12. CRUD Comptes administratifs
13. Saisie des lignes budgetaires

### Phase 4 : Revenus et Documents (Semaine 8)
14. Gestion des revenus miniers
15. Gestion des documents

### Phase 5 : Communication et Analytics (Semaine 9)
16. Newsletter
17. Messagerie securisee
18. Analytics et statistiques

### Phase 6 : Finalisation (Semaine 10)
19. Import/Export
20. Configuration et parametres
21. Tests et optimisations
