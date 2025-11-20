# Migrations de la base de données

Ce répertoire contient les migrations SQL pour améliorer le modèle de données et permettre la reproduction exacte des tableaux de compte administratif issus du fichier Excel.

## 📋 Liste des migrations

### 001_ameliorations_tableaux.sql

**Description:** Améliorations du schéma pour reproduire fidèlement les tableaux Excel (RECETTE, DEPENSE, EQUILIBRE)

**Modifications:**
1. ✅ Ajout du champ `applicable_a` dans `colonnes_dynamiques`
   - Permet de différencier les colonnes applicables aux recettes, dépenses ou aux deux
   - Valeurs possibles: `'recette'`, `'depense'`, `'tous'`, `'equilibre'`

2. ✅ Amélioration du trigger `calculer_valeurs_derivees()`
   - Calcul automatique des **prévisions définitives** (budget primitif + additionnel + modifications)
   - Calcul du **reste à recouvrer** pour les recettes (OR Admis - Recouvrement)
   - Calcul du **reste à payer** pour les dépenses (Mandat Admis - Paiement)
   - Calcul du **taux d'exécution** différencié selon le type:
     - Recettes: (OR Admis / Prévisions Définitives) × 100
     - Dépenses: (Mandat Admis / Prévisions Définitives) × 100

3. ✅ Création de la vue `v_equilibre_compte_administratif`
   - Vue pour générer le tableau d'équilibre (comme la feuille EQUILIBRE de l'Excel)
   - Agrège les dépenses et recettes par section (fonctionnement/investissement)
   - Calcule les totaux et soldes automatiquement

**Dépendances:** Aucune (peut être appliquée directement sur le schéma de base)

---

### 002_insertion_rubriques_budgetaires.sql

**Description:** Insertion de toutes les rubriques budgétaires extraites du fichier Excel

**Contenu:**
- **437 rubriques budgétaires** au total:
  - 166 recettes
  - 271 dépenses
  - Réparties sur 3 niveaux hiérarchiques:
    - Niveau 1: 26 comptes principaux (ex: 70, 71, 72, 60, 61)
    - Niveau 2: 95 sous-comptes (ex: 708, 714, 601)
    - Niveau 3: 316 comptes détaillés (ex: 7080, 7140, 6011)

**Structure hiérarchique:**
- Les rubriques sont insérées niveau par niveau pour respecter les contraintes de clé étrangère
- Chaque rubrique de niveau 2 ou 3 a un `parent_id` pointant vers son compte parent
- Exemple de hiérarchie:
  ```
  70 - IMPOTS SUR LES REVENUS, BENEFICES ET GAINS (niveau 1)
   └─ 708 - Autres impôts sur les revenus (niveau 2)
       └─ 7080 - Autres impôts sur les revenus - Impôt synthétique (niveau 3)
  ```

**Dépendances:** Nécessite que la table `rubriques_budgetaires` existe (schéma de base ou migration 001)

---

## 🚀 Application des migrations

### Option 1: Via Supabase Dashboard (Recommandé pour débuter)

1. Connectez-vous à votre projet Supabase
2. Allez dans **SQL Editor**
3. Copiez le contenu de chaque fichier de migration dans l'ordre:
   - D'abord `001_ameliorations_tableaux.sql`
   - Puis `002_insertion_rubriques_budgetaires.sql`
4. Exécutez chaque migration en cliquant sur "Run"

### Option 2: Via Supabase CLI

```bash
# Appliquer la migration 001
supabase db execute --file bank/modele_de_donnees/migrations/001_ameliorations_tableaux.sql

# Appliquer la migration 002
supabase db execute --file bank/modele_de_donnees/migrations/002_insertion_rubriques_budgetaires.sql
```

### Option 3: Via psql (Si vous avez accès direct à PostgreSQL)

```bash
# Se connecter à la base de données
psql -h <SUPABASE_HOST> -U postgres -d postgres

# Appliquer les migrations
\i bank/modele_de_donnees/migrations/001_ameliorations_tableaux.sql
\i bank/modele_de_donnees/migrations/002_insertion_rubriques_budgetaires.sql
```

---

## ✅ Vérification après migration

Après avoir appliqué les migrations, vous pouvez vérifier que tout fonctionne correctement:

```sql
-- 1. Vérifier que le champ applicable_a a été ajouté
SELECT code, nom, applicable_a
FROM colonnes_dynamiques
ORDER BY ordre;

-- 2. Vérifier le nombre de rubriques insérées
SELECT
    type,
    section,
    niveau,
    COUNT(*) as nombre_rubriques
FROM rubriques_budgetaires
GROUP BY type, section, niveau
ORDER BY type, section, niveau;

-- Résultat attendu:
-- recette | fonctionnement | 1 | 7
-- recette | fonctionnement | 2 | 25
-- recette | fonctionnement | 3 | 110
-- recette | investissement | 1 | 3
-- recette | investissement | 2 | 6
-- recette | investissement | 3 | 15
-- depense | fonctionnement | 1 | 8
-- depense | fonctionnement | 2 | 43
-- depense | fonctionnement | 3 | 161
-- depense | investissement | 1 | 5
-- depense | investissement | 2 | 15
-- depense | investissement | 3 | 40

-- 3. Vérifier la hiérarchie des rubriques (exemple)
SELECT
    r1.code as code_n1,
    r1.intitule as intitule_n1,
    r2.code as code_n2,
    r2.intitule as intitule_n2,
    r3.code as code_n3,
    r3.intitule as intitule_n3
FROM rubriques_budgetaires r1
LEFT JOIN rubriques_budgetaires r2 ON r2.parent_id = r1.id
LEFT JOIN rubriques_budgetaires r3 ON r3.parent_id = r2.id
WHERE r1.code = '70'
ORDER BY r2.code, r3.code;

-- 4. Tester la vue d'équilibre (nécessite des données de test)
SELECT * FROM v_equilibre_compte_administratif LIMIT 1;
```

---

## 🔧 Régénération de la migration 002

Si vous modifiez le fichier Excel et souhaitez régénérer la migration des rubriques:

```bash
# Exécuter le script Python d'extraction
python3 bank/modele_de_donnees/scripts/extraire_rubriques_excel.py

# Le fichier 002_insertion_rubriques_budgetaires.sql sera automatiquement mis à jour
```

**Note:** Avant de réappliquer la migration 002, pensez à supprimer les rubriques existantes:

```sql
TRUNCATE TABLE rubriques_budgetaires CASCADE;
```

---

## 📊 Impact sur l'application

Après ces migrations, votre application pourra:

1. ✅ Générer automatiquement les **tableaux de recettes** conformes au fichier Excel
2. ✅ Générer automatiquement les **tableaux de dépenses** conformes au fichier Excel
3. ✅ Générer le **tableau d'équilibre** avec calcul automatique des soldes
4. ✅ Différencier les colonnes applicables aux recettes vs dépenses
5. ✅ Calculer automatiquement les valeurs dérivées (restes, taux d'exécution, etc.)
6. ✅ Gérer une hiérarchie complète de 437 rubriques budgétaires sur 3 niveaux

---

## ⚠️ Notes importantes

1. **Ordre d'application:** Les migrations doivent être appliquées dans l'ordre numérique (001, 002, etc.)

2. **Sauvegarde:** Avant d'appliquer les migrations en production, faites toujours une sauvegarde de votre base de données

3. **Performances:** La migration 002 insère 437 lignes. Les triggers sont temporairement désactivés pour améliorer les performances

4. **Rollback:** Si vous souhaitez annuler les migrations:
   ```sql
   -- Annuler migration 002
   TRUNCATE TABLE rubriques_budgetaires CASCADE;

   -- Annuler migration 001
   ALTER TABLE colonnes_dynamiques DROP COLUMN IF EXISTS applicable_a;
   DROP VIEW IF EXISTS v_equilibre_compte_administratif;
   -- (La fonction calculer_valeurs_derivees sera remplacée par l'ancienne version)
   ```

---

## 📚 Documentation complémentaire

- **Schéma de base:** [schema.sql](../schema.sql)
- **Modèle conceptuel:** [mcd.md](../mcd.md)
- **Fichier Excel source:** [Tableaux_de_Compte_Administratif.xlsx](../../cahier_des_charges/Tableaux_de_Compte_Administratif.xlsx)
- **Script d'extraction:** [extraire_rubriques_excel.py](../scripts/extraire_rubriques_excel.py)
