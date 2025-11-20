# 📊 Résumé : Seed de la base de données depuis Excel

## ✅ Travail réalisé

J'ai créé un système complet pour réinitialiser et peupler votre base de données à partir du fichier Excel `Tableaux_de_Compte_Administratif.xlsx`.

### 📁 Fichiers créés

| Fichier | Taille | Description |
|---------|--------|-------------|
| **003_reset_et_seed_donnees.sql** | 96 KB | Script principal : nettoyage + 436 rubriques + 12 colonnes |
| **004_seed_donnees_test.sql** | 15 KB | Données de test complètes (région, district, commune, compte 2024) |
| **README_SEED.md** | 11 KB | Documentation complète d'utilisation |

### 📊 Données extraites de l'Excel

✅ **166 rubriques de RECETTES** extraites de la feuille "RECETTE"
- Codes comptables : 70, 71, 72, 74, 75, 76, 77
- Structure hiérarchique à 3 niveaux (ex: 70 > 708 > 7080)

✅ **270 rubriques de DÉPENSES** extraites de la feuille "DEPENSES"
- Codes comptables : 60, 61, 62, 63, 64, 65, 66, 67
- Structure hiérarchique à 3 niveaux (ex: 60 > 601 > 6011)

✅ **12 colonnes dynamiques** définies selon la structure Excel :
- 4 colonnes communes (budget_primitif, budget_additionnel, modifications, previsions_definitives)
- 4 colonnes RECETTES (or_admis, recouvrement, reste_recouvrer, taux_execution)
- 5 colonnes DÉPENSES (engagement, mandat_admis, paiement, reste_payer, taux_execution)

## 🚀 Comment utiliser

### Option 1 : Réinitialisation complète (RECOMMANDÉ)

```bash
# 1. Ouvrir Supabase SQL Editor
# 2. Exécuter dans l'ordre :

-- Étape 1 : Réinitialiser et insérer les rubriques
\i bank/modele_de_donnees/migrations/003_reset_et_seed_donnees.sql

-- Étape 2 : Créer des données de test
\i bank/modele_de_donnees/migrations/004_seed_donnees_test.sql
```

⏱️ **Temps d'exécution** : ~30 secondes

### Option 2 : Seed manuel (si vous avez déjà des collectivités)

```sql
-- Exécuter uniquement le script principal
\i bank/modele_de_donnees/migrations/003_reset_et_seed_donnees.sql

-- Puis créer votre propre compte administratif :
INSERT INTO comptes_administratifs (commune_id, annee, statut)
VALUES ('<votre_commune_id>', 2024, 'brouillon');
```

## 📊 Résultat attendu

Après exécution, vous aurez :

```
✅ 436 rubriques budgétaires actives
   ├── 166 recettes (fonctionnement)
   └── 270 dépenses (fonctionnement + investissement)

✅ 12 colonnes dynamiques actives
   ├── 4 communes (tous)
   ├── 4 recettes
   └── 5 dépenses

✅ Données de test (si script 004 exécuté)
   ├── 1 région (RG-TEST)
   ├── 1 district (DT-TEST)
   ├── 1 commune (COM-TEST)
   ├── 1 compte administratif 2024
   └── 15 lignes budgétaires avec valeurs réalistes
```

## 🖥️ Vérification via l'interface web

### 1️⃣ Tableau d'équilibre
```
URL : http://localhost:3000/admin/comptes-administratifs/equilibre

Filtres :
- Année : 2024
- Type : Commune
- Collectivité : Commune Test

✅ Vous devriez voir :
   - Section Fonctionnement (Dépenses vs Recettes)
   - Totaux et soldes calculés automatiquement
   - Toutes les valeurs formatées en MGA
```

### 2️⃣ Saisie des lignes budgétaires
```
URL : http://localhost:3000/admin/comptes-administratifs/lignes-budgetaires

✅ Interface Excel-like avec :
   - Onglets Recettes / Dépenses
   - Colonnes dynamiques (Budget, OR/Mandat, Paiement/Recouvrement)
   - Champs calculés automatiquement (⚙️)
   - Sauvegarde en masse
```

### 3️⃣ Gestion des comptes
```
URL : http://localhost:3000/admin/comptes-administratifs/comptes

✅ Actions disponibles :
   - Créer nouveau compte
   - Modifier compte existant
   - Changer statut (brouillon/validé/publié)
```

## 📥 Extraction des données (comme dans Excel)

### Format RECETTES

```sql
SELECT
    rb.code as "COMPTE",
    rb.intitule as "INTITULES",
    (lb.valeurs->>'budget_primitif')::numeric as "BUDGET PRIMITIF",
    (lb.valeurs->>'or_admis')::numeric as "OR ADMIS",
    (lb.valeurs->>'recouvrement')::numeric as "RECOUVREMENT"
FROM lignes_budgetaires lb
JOIN rubriques_budgetaires rb ON lb.rubrique_id = rb.id
WHERE rb.type = 'recette'
ORDER BY rb.ordre;
```

**Résultat** : Tableau identique à la feuille "RECETTE" du fichier Excel

### Format DÉPENSES

```sql
SELECT
    rb.code as "COMPTE",
    rb.intitule as "INTITULES",
    (lb.valeurs->>'budget_primitif')::numeric as "BUDGET PRIMITIF",
    (lb.valeurs->>'mandat_admis')::numeric as "MANDAT ADMIS",
    (lb.valeurs->>'paiement')::numeric as "PAIEMENT"
FROM lignes_budgetaires lb
JOIN rubriques_budgetaires rb ON lb.rubrique_id = rb.id
WHERE rb.type = 'depense'
ORDER BY rb.ordre;
```

**Résultat** : Tableau identique à la feuille "DEPENSES" du fichier Excel

### Format ÉQUILIBRE

```sql
SELECT * FROM v_equilibre_compte_administratif
WHERE annee = 2024;
```

**Résultat** : Tableau identique à la feuille "EQUILIBRE" du fichier Excel

## 🎯 Objectif atteint

✅ **AVANT** : Vous aviez un fichier Excel avec des tableaux de compte administratif

✅ **MAINTENANT** : Vous avez un système complet qui permet de :
1. ✅ Saisir les données budgétaires via une interface web
2. ✅ Calculer automatiquement les valeurs dérivées (soldes, taux, etc.)
3. ✅ Visualiser le tableau d'équilibre en temps réel
4. ✅ Extraire les données au format Excel via SQL
5. ✅ Gérer plusieurs comptes administratifs (différentes collectivités/années)

## 🔄 Workflow complet

```
1. Utilisateur saisit les données via /lignes-budgetaires
   ↓
2. Triggers SQL calculent automatiquement les valeurs dérivées
   ↓
3. Vue v_equilibre_compte_administratif agrège les données
   ↓
4. Interface /equilibre affiche le résultat
   ↓
5. Requêtes SQL extraient les données au format Excel
```

## 📊 Comparaison Excel vs Base de données

| Aspect | Excel | Base de données |
|--------|-------|-----------------|
| **Saisie** | Manuelle, cellule par cellule | Interface web intuitive |
| **Calculs** | Formules Excel fragiles | Triggers SQL automatiques |
| **Validation** | Aucune | Contraintes SQL (CHECK, FK) |
| **Multi-utilisateurs** | ❌ Conflits de versions | ✅ Concurrent, transactionnel |
| **Historique** | ❌ Versions manuelles | ✅ Timestamps automatiques |
| **Agrégation** | ❌ Tableaux croisés manuels | ✅ Vues SQL pré-calculées |
| **Export** | ❌ Format propriétaire | ✅ SQL, CSV, JSON, Excel |

## 🎓 Exemples d'utilisation

### Cas 1 : Créer un compte pour une nouvelle commune

```sql
-- 1. Créer la commune (si nécessaire)
INSERT INTO communes (code, nom, district_id, population)
VALUES ('COM-ALO', 'Aloalobe', '<district_id>', 15000);

-- 2. Créer le compte administratif
INSERT INTO comptes_administratifs (commune_id, annee, statut)
SELECT id, 2025, 'brouillon'
FROM communes
WHERE code = 'COM-ALO';

-- 3. Saisir les lignes via l'interface web
-- URL: /admin/comptes-administratifs/lignes-budgetaires
```

### Cas 2 : Comparer plusieurs années

```sql
-- Comparaison recettes 2023 vs 2024
SELECT
    ca.annee,
    SUM((lb.valeurs->>'or_admis')::numeric) as total_or_admis,
    SUM((lb.valeurs->>'recouvrement')::numeric) as total_recouvrement
FROM lignes_budgetaires lb
JOIN rubriques_budgetaires rb ON lb.rubrique_id = rb.id
JOIN comptes_administratifs ca ON lb.compte_administratif_id = ca.id
WHERE rb.type = 'recette'
  AND ca.annee IN (2023, 2024)
GROUP BY ca.annee
ORDER BY ca.annee;
```

### Cas 3 : Exporter tout en CSV

```sql
-- Utiliser psql ou pgAdmin pour exporter
\copy (
    SELECT
        c.nom as commune,
        ca.annee,
        rb.code,
        rb.intitule,
        rb.type,
        lb.valeurs
    FROM lignes_budgetaires lb
    JOIN rubriques_budgetaires rb ON lb.rubrique_id = rb.id
    JOIN comptes_administratifs ca ON lb.compte_administratif_id = ca.id
    JOIN communes c ON ca.commune_id = c.id
    ORDER BY ca.annee, rb.ordre
) TO '/tmp/export_comptes_administratifs.csv' WITH CSV HEADER;
```

## 📚 Documentation complète

Pour plus de détails, consultez :
- **README_SEED.md** : Guide complet d'utilisation (11 KB)
- **003_reset_et_seed_donnees.sql** : Script principal avec commentaires
- **004_seed_donnees_test.sql** : Exemples de données de test

## 🆘 Support

En cas de problème :
1. Vérifiez que le `schema.sql` principal a été exécuté
2. Consultez la section "Dépannage" dans `README_SEED.md`
3. Vérifiez les logs Supabase pour les erreurs SQL

---

**✅ Votre système est prêt à être utilisé !**

**Prochaines étapes :**
1. Exécutez les scripts SQL dans Supabase
2. Testez l'interface web
3. Saisissez vos vraies données
4. Exportez les résultats

**Bonne utilisation ! 🚀**
