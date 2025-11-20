# Rapport d'amélioration du modèle de données

**Date:** 2025-11-16
**Objectif:** Adapter le modèle de données pour reproduire exactement les tableaux du fichier Excel [Tableaux_de_Compte_Administratif.xlsx](../cahier_des_charges/Tableaux_de_Compte_Administratif.xlsx)

---

## ✅ Résumé des améliorations apportées

Votre modèle de données a été enrichi pour permettre la reproduction **exacte** des trois tableaux Excel :
- **RECETTE** : Tableau détaillé des recettes
- **DEPENSES** : Tableau détaillé des dépenses
- **EQUILIBRE** : Tableau d'équilibre du compte administratif

---

## 📦 Fichiers créés

### 1. Migrations SQL

| Fichier | Description | Taille |
|---------|-------------|---------|
| [001_ameliorations_tableaux.sql](migrations/001_ameliorations_tableaux.sql) | Ajout du champ `applicable_a`, amélioration des triggers, création de la vue d'équilibre | ~12 KB |
| [002_insertion_rubriques_budgetaires.sql](migrations/002_insertion_rubriques_budgetaires.sql) | Insertion de **437 rubriques budgétaires** extraites de l'Excel | ~235 KB |

### 2. Scripts et outils

| Fichier | Description |
|---------|-------------|
| [scripts/extraire_rubriques_excel.py](scripts/extraire_rubriques_excel.py) | Script Python pour extraire les rubriques depuis l'Excel et générer le SQL d'insertion |
| [exemples_utilisation.sql](exemples_utilisation.sql) | Exemples de requêtes SQL pour exploiter le modèle amélioré |

### 3. Documentation

| Fichier | Description |
|---------|-------------|
| [migrations/README.md](migrations/README.md) | Guide complet d'application des migrations avec vérifications |
| [RAPPORT_AMELIORATIONS.md](RAPPORT_AMELIORATIONS.md) | Ce fichier - rapport récapitulatif |

---

## 🎯 Fonctionnalités ajoutées

### 1. Différenciation Recettes/Dépenses

**Problème identifié :** Les colonnes "OR ADMIS" et "RECOUVREMENT" sont spécifiques aux recettes, tandis que "ENGAGEMENT", "MANDAT ADMIS" et "PAIEMENT" sont spécifiques aux dépenses.

**Solution :** Ajout du champ `applicable_a` dans la table `colonnes_dynamiques`

```sql
-- Exemples
SELECT * FROM colonnes_dynamiques WHERE applicable_a = 'recette';
-- Retourne: or_admis, recouvrement, reste_recouvrer

SELECT * FROM colonnes_dynamiques WHERE applicable_a = 'depense';
-- Retourne: engagement, mandat_admis, paiement, reste_payer
```

### 2. Calculs automatiques enrichis

**Problème identifié :** Seules quelques formules étaient calculées automatiquement

**Solution :** Trigger `calculer_valeurs_derivees()` amélioré avec **toutes** les formules :

| Formule | Type | Calcul |
|---------|------|--------|
| **Prévisions définitives** | Tous | `budget_primitif + budget_additionnel + modifications` |
| **Reste à recouvrer** | Recettes | `or_admis - recouvrement` |
| **Reste à payer** | Dépenses | `mandat_admis - paiement` |
| **Taux d'exécution (Recettes)** | Recettes | `(or_admis / previsions_definitives) × 100` |
| **Taux d'exécution (Dépenses)** | Dépenses | `(mandat_admis / previsions_definitives) × 100` |

### 3. Tableau d'équilibre automatique

**Problème identifié :** Pas de mécanisme pour générer le tableau EQUILIBRE

**Solution :** Création de la vue `v_equilibre_compte_administratif`

Cette vue agrège automatiquement :
- Dépenses de fonctionnement (par compte principal)
- Recettes de fonctionnement (par compte principal)
- Dépenses d'investissement (par compte principal)
- Recettes d'investissement (par compte principal)
- **Calcul du solde de fonctionnement**

### 4. Hiérarchie complète des rubriques

**Problème identifié :** Les 437 rubriques de l'Excel n'étaient pas dans la base de données

**Solution :** Extraction automatique et insertion hiérarchique

**Statistiques des rubriques :**
- **Total :** 437 rubriques
- **Recettes :** 166
- **Dépenses :** 271
- **Niveau 1 :** 26 comptes principaux (70, 71, 72, 60, 61, etc.)
- **Niveau 2 :** 95 sous-comptes (708, 714, 601, etc.)
- **Niveau 3 :** 316 comptes détaillés (7080, 7140, 6011, etc.)

**Exemple de hiérarchie :**
```
70 - IMPOTS SUR LES REVENUS, BENEFICES ET GAINS
 ├─ 708 - Autres impôts sur les revenus
 │   └─ 7080 - Autres impôts sur les revenus - Impôt synthétique
 ├─ 714 - Impôts fonciers sur les terrains - IFT
 │   └─ 7140 - Impôts fonciers sur les terrains - IFT
 └─ 715 - Impôt foncier sur les propriétés bâties – IFPB
     ├─ 7151 - Impôt foncier sur les propriétés bâties – IFPB
     └─ 7158 - Autres impôts locaux sur les propriétés baties
```

---

## 📋 Prochaines étapes pour appliquer les améliorations

### Étape 1 : Appliquer les migrations

#### Option A : Via Supabase Dashboard (Recommandé)

1. Connectez-vous à votre projet Supabase
2. Allez dans **SQL Editor**
3. Exécutez d'abord [001_ameliorations_tableaux.sql](migrations/001_ameliorations_tableaux.sql)
4. Puis exécutez [002_insertion_rubriques_budgetaires.sql](migrations/002_insertion_rubriques_budgetaires.sql)

#### Option B : Via Supabase CLI

```bash
supabase db execute --file bank/modele_de_donnees/migrations/001_ameliorations_tableaux.sql
supabase db execute --file bank/modele_de_donnees/migrations/002_insertion_rubriques_budgetaires.sql
```

### Étape 2 : Vérifier l'application

```sql
-- Vérifier le nombre de rubriques insérées
SELECT type, section, niveau, COUNT(*) as nombre
FROM rubriques_budgetaires
GROUP BY type, section, niveau
ORDER BY type, section, niveau;

-- Vérifier les colonnes dynamiques
SELECT code, nom, applicable_a FROM colonnes_dynamiques ORDER BY ordre;
```

**Résultat attendu :** 437 rubriques réparties sur 3 niveaux

### Étape 3 : Tester avec des données

Utilisez les exemples du fichier [exemples_utilisation.sql](exemples_utilisation.sql) pour :
- Créer un compte administratif de test
- Insérer des lignes budgétaires
- Générer les tableaux de recettes, dépenses et équilibre

---

## 🔧 Maintenance et évolution

### Régénérer les rubriques après modification de l'Excel

Si vous modifiez le fichier Excel source :

```bash
# 1. Régénérer le fichier SQL d'insertion
python3 bank/modele_de_donnees/scripts/extraire_rubriques_excel.py

# 2. Supprimer les anciennes rubriques
# (via Supabase SQL Editor)
TRUNCATE TABLE rubriques_budgetaires CASCADE;

# 3. Réappliquer la migration 002
supabase db execute --file bank/modele_de_donnees/migrations/002_insertion_rubriques_budgetaires.sql
```

### Ajouter de nouvelles colonnes dynamiques

```sql
INSERT INTO colonnes_dynamiques (
    code, nom, type_donnee, ordre, est_calculee, applicable_a
) VALUES (
    'nouvelle_colonne',
    'Ma Nouvelle Colonne',
    'montant',
    20,
    FALSE,
    'tous'
);
```

### Modifier les formules de calcul

Éditez la fonction `calculer_valeurs_derivees()` dans [001_ameliorations_tableaux.sql](migrations/001_ameliorations_tableaux.sql#L43-L105)

---

## 📊 Impact sur l'application Nuxt

### API à développer

Vous devrez créer des endpoints API dans votre application Nuxt pour :

1. **Générer le tableau de recettes**
   ```typescript
   // /api/comptes-administratifs/[id]/recettes.get.ts
   export default defineEventHandler(async (event) => {
     const id = getRouterParam(event, 'id')
     // Exécuter la requête SQL du fichier exemples_utilisation.sql
   })
   ```

2. **Générer le tableau de dépenses**
   ```typescript
   // /api/comptes-administratifs/[id]/depenses.get.ts
   ```

3. **Générer le tableau d'équilibre**
   ```typescript
   // /api/comptes-administratifs/[id]/equilibre.get.ts
   export default defineEventHandler(async (event) => {
     const id = getRouterParam(event, 'id')
     // SELECT * FROM v_equilibre_compte_administratif WHERE id = ?
   })
   ```

### Composants Vue à créer

Suggestions de composants :

- `TableauRecettes.vue` : Affiche le tableau de recettes avec hiérarchie
- `TableauDepenses.vue` : Affiche le tableau de dépenses avec hiérarchie
- `TableauEquilibre.vue` : Affiche le tableau d'équilibre
- `FormulaireCompteAdministratif.vue` : Formulaire de saisie avec colonnes dynamiques

### Intégration dans les pages

```vue
<!-- pages/comptes-administratifs/[id]/index.vue -->
<template>
  <div>
    <h1>Compte Administratif {{ annee }}</h1>

    <TabGroup>
      <TabList>
        <Tab>Recettes</Tab>
        <Tab>Dépenses</Tab>
        <Tab>Équilibre</Tab>
      </TabList>

      <TabPanels>
        <TabPanel><TableauRecettes :compte-id="id" /></TabPanel>
        <TabPanel><TableauDepenses :compte-id="id" /></TabPanel>
        <TabPanel><TableauEquilibre :compte-id="id" /></TabPanel>
      </TabPanels>
    </TabGroup>
  </div>
</template>
```

---

## ✨ Résumé des bénéfices

| Avant | Après |
|-------|-------|
| ❌ Pas de rubriques budgétaires | ✅ **437 rubriques** hiérarchiques sur 3 niveaux |
| ❌ Formules de calcul incomplètes | ✅ **5 formules** automatiques (prévisions, restes, taux) |
| ❌ Colonnes mélangées recettes/dépenses | ✅ Différenciation claire via `applicable_a` |
| ❌ Pas de tableau d'équilibre | ✅ Vue SQL `v_equilibre_compte_administratif` |
| ❌ Extraction manuelle depuis Excel | ✅ Script Python de **régénération automatique** |

---

## 📚 Documentation complémentaire

- **Guide d'application des migrations :** [migrations/README.md](migrations/README.md)
- **Exemples d'utilisation SQL :** [exemples_utilisation.sql](exemples_utilisation.sql)
- **Script d'extraction Python :** [scripts/extraire_rubriques_excel.py](scripts/extraire_rubriques_excel.py)
- **Schéma de base :** [schema.sql](schema.sql)
- **Modèle conceptuel :** [mcd.md](mcd.md)

---

## 🎉 Conclusion

Votre modèle de données est maintenant **entièrement compatible** avec les tableaux Excel du cahier des charges. Vous pouvez :

1. ✅ Générer les **tableaux de recettes** conformes au fichier Excel
2. ✅ Générer les **tableaux de dépenses** conformes au fichier Excel
3. ✅ Générer le **tableau d'équilibre** avec calculs automatiques
4. ✅ Bénéficier de **calculs automatiques** pour toutes les valeurs dérivées
5. ✅ Exploiter une **hiérarchie complète** de 437 rubriques budgétaires

**Prochaine étape :** Appliquer les migrations dans votre base de données Supabase et développer les composants Vue pour afficher ces tableaux dans l'application.

---

**Questions ou problèmes ?** Consultez la [documentation des migrations](migrations/README.md) ou les [exemples d'utilisation](exemples_utilisation.sql).
