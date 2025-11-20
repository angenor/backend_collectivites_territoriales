# Guide d'installation rapide des améliorations

Ce guide vous permet d'appliquer rapidement toutes les améliorations du modèle de données en **3 étapes simples**.

---

## ⚡ Installation en 3 étapes

### Étape 1️⃣ : Appliquer la migration 001 (Améliorations structurelles)

**Via Supabase Dashboard :**

1. Connectez-vous à [Supabase](https://app.supabase.com)
2. Sélectionnez votre projet
3. Cliquez sur **SQL Editor** dans le menu de gauche
4. Cliquez sur **New query**
5. Copiez-collez le contenu du fichier [001_ameliorations_tableaux.sql](migrations/001_ameliorations_tableaux.sql)
6. Cliquez sur **Run** (ou appuyez sur `Ctrl+Enter`)

**Résultat attendu :**
```
✅ ALTER TABLE (ajout du champ applicable_a)
✅ UPDATE (mise à jour des colonnes existantes)
✅ CREATE OR REPLACE FUNCTION (trigger de calcul amélioré)
✅ CREATE OR REPLACE VIEW (vue d'équilibre)
```

---

### Étape 2️⃣ : Appliquer la migration 002 (Insertion des rubriques)

**Via Supabase Dashboard :**

1. Restez dans **SQL Editor**
2. Cliquez sur **New query**
3. Copiez-collez le contenu du fichier [002_insertion_rubriques_budgetaires.sql](migrations/002_insertion_rubriques_budgetaires.sql)
4. Cliquez sur **Run**

**⚠️ Important :** Cette migration insère 437 lignes et peut prendre **30 secondes à 1 minute**.

**Résultat attendu :**
```
✅ ALTER TABLE DISABLE TRIGGER
✅ INSERT INTO rubriques_budgetaires (437 lignes insérées)
✅ ALTER TABLE ENABLE TRIGGER
✅ Statistiques affichées
```

---

### Étape 3️⃣ : Vérifier l'installation

**Exécutez cette requête de vérification :**

```sql
-- Vérifier le nombre de rubriques par type/section/niveau
SELECT
    type,
    section,
    niveau,
    COUNT(*) as nombre_rubriques
FROM rubriques_budgetaires
GROUP BY type, section, niveau
ORDER BY type, section, niveau;
```

**Résultat attendu :**

| type | section | niveau | nombre_rubriques |
|------|---------|--------|------------------|
| depense | fonctionnement | 1 | 8 |
| depense | fonctionnement | 2 | 43 |
| depense | fonctionnement | 3 | 161 |
| depense | investissement | 1 | 5 |
| depense | investissement | 2 | 15 |
| depense | investissement | 3 | 40 |
| recette | fonctionnement | 1 | 7 |
| recette | fonctionnement | 2 | 25 |
| recette | fonctionnement | 3 | 110 |
| recette | investissement | 1 | 3 |
| recette | investissement | 2 | 6 |
| recette | investissement | 3 | 15 |

**Total : 437 rubriques** ✅

---

## 🧪 Test rapide des fonctionnalités

### Test 1 : Créer un compte administratif de test

```sql
-- Remplacez 'VOTRE_COMMUNE_ID' par un UUID de commune existant
INSERT INTO comptes_administratifs (
    commune_id,
    annee,
    statut
) VALUES (
    'VOTRE_COMMUNE_ID',
    2024,
    'brouillon'
);
```

### Test 2 : Insérer une ligne budgétaire avec calculs automatiques

```sql
-- Récupérer l'ID du compte admin créé
WITH dernier_compte AS (
    SELECT id FROM comptes_administratifs
    WHERE annee = 2024
    ORDER BY created_at DESC
    LIMIT 1
),
rubrique_7080 AS (
    SELECT id FROM rubriques_budgetaires
    WHERE code = '7080'
    LIMIT 1
)
INSERT INTO lignes_budgetaires (
    compte_administratif_id,
    rubrique_id,
    valeurs
)
SELECT
    dc.id,
    r.id,
    jsonb_build_object(
        'budget_primitif', 1000000,
        'budget_additionnel', 50000,
        'modifications', -20000,
        'or_admis', 950000,
        'recouvrement', 900000
    )
FROM dernier_compte dc, rubrique_7080 r;
```

### Test 3 : Vérifier les calculs automatiques

```sql
-- Vérifier que les valeurs calculées ont été générées automatiquement
SELECT
    rb.code,
    rb.intitule,
    lb.valeurs->>'budget_primitif' as budget_primitif,
    lb.valeurs->>'budget_additionnel' as budget_additionnel,
    lb.valeurs->>'modifications' as modifications,
    lb.valeurs->>'previsions_definitives' as previsions_definitives_calculee,
    lb.valeurs->>'or_admis' as or_admis,
    lb.valeurs->>'recouvrement' as recouvrement,
    lb.valeurs->>'reste_recouvrer' as reste_recouvrer_calcule,
    lb.valeurs->>'taux_execution' as taux_execution_calcule
FROM lignes_budgetaires lb
JOIN rubriques_budgetaires rb ON lb.rubrique_id = rb.id
ORDER BY lb.created_at DESC
LIMIT 1;
```

**Résultat attendu :**
```
code: 7080
budget_primitif: 1000000
budget_additionnel: 50000
modifications: -20000
previsions_definitives_calculee: 1030000  ← Calculé automatiquement
or_admis: 950000
recouvrement: 900000
reste_recouvrer_calcule: 50000  ← Calculé automatiquement (950000 - 900000)
taux_execution_calcule: 92.23   ← Calculé automatiquement ((950000/1030000)*100)
```

✅ Si les valeurs `previsions_definitives`, `reste_recouvrer` et `taux_execution` sont calculées, **tout fonctionne parfaitement** !

---

## 🎯 Prochaines étapes

Maintenant que votre base de données est améliorée, vous pouvez :

1. **Développer les APIs Nuxt** pour exposer les données :
   - `/api/comptes-administratifs/[id]/recettes.get.ts`
   - `/api/comptes-administratifs/[id]/depenses.get.ts`
   - `/api/comptes-administratifs/[id]/equilibre.get.ts`

2. **Créer les composants Vue** pour afficher les tableaux :
   - `TableauRecettes.vue`
   - `TableauDepenses.vue`
   - `TableauEquilibre.vue`

3. **Consulter les exemples d'utilisation** : [exemples_utilisation.sql](exemples_utilisation.sql)

---

## ❓ Dépannage

### Problème : "La migration 002 est trop longue"

**Solution :** La migration insère 437 lignes. C'est normal qu'elle prenne 30-60 secondes. Attendez la fin de l'exécution.

### Problème : "Erreur: table rubriques_budgetaires does not exist"

**Solution :** Vous devez d'abord créer le schéma de base avec [schema.sql](schema.sql), puis appliquer les migrations.

### Problème : "Les valeurs calculées ne sont pas générées"

**Solution :** Vérifiez que le trigger est bien activé :

```sql
-- Vérifier les triggers
SELECT tgname, tgenabled
FROM pg_trigger
WHERE tgrelid = 'lignes_budgetaires'::regclass;

-- Réactiver si nécessaire
ALTER TABLE lignes_budgetaires ENABLE TRIGGER trigger_calculer_valeurs_derivees;
```

### Problème : "Duplicate key value violates unique constraint"

**Solution :** Les rubriques ont déjà été insérées. Supprimez-les avant de réappliquer la migration 002 :

```sql
TRUNCATE TABLE rubriques_budgetaires CASCADE;
```

---

## 📚 Documentation complète

Pour plus de détails, consultez :

- **Documentation des migrations :** [migrations/README.md](migrations/README.md)
- **Rapport complet :** [RAPPORT_AMELIORATIONS.md](RAPPORT_AMELIORATIONS.md)
- **Exemples SQL :** [exemples_utilisation.sql](exemples_utilisation.sql)

---

## ✅ Checklist finale

- [ ] Migration 001 appliquée avec succès
- [ ] Migration 002 appliquée avec succès
- [ ] Vérification : 437 rubriques insérées
- [ ] Test : Compte administratif créé
- [ ] Test : Ligne budgétaire insérée avec calculs automatiques
- [ ] Résultat : Les valeurs calculées sont correctes

**Une fois toutes les cases cochées, votre base de données est prête ! 🎉**
