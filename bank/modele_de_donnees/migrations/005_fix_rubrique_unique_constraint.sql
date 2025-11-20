-- Migration 005: Correction de la contrainte UNIQUE sur rubriques_budgetaires
--
-- PROBLÈME: La contrainte actuelle UNIQUE(code) empêche d'avoir le même code
--           pour les recettes ET les dépenses, ce qui est requis par le plan comptable M57.
--           Par exemple, le code "16" (EMPRUNTS ET DETTES ASSIMILEES) existe légitimement
--           dans les deux types.
--
-- SOLUTION: Remplacer la contrainte UNIQUE(code) par UNIQUE(code, type)
--           pour permettre le même code avec des types différents.
--
-- Date: 2025-11-17
-- Auteur: System Migration

-- ÉTAPE 1: Supprimer la contrainte existante sur code uniquement
ALTER TABLE rubriques_budgetaires
DROP CONSTRAINT IF EXISTS rubriques_budgetaires_code_key;

-- ÉTAPE 2: Ajouter la nouvelle contrainte sur (code, type)
ALTER TABLE rubriques_budgetaires
ADD CONSTRAINT rubriques_budgetaires_code_type_key UNIQUE (code, type);

-- ÉTAPE 3: Vérification
-- Cette requête affiche les codes qui apparaissent maintenant dans les deux types
SELECT
    code,
    COUNT(DISTINCT type) as nb_types,
    STRING_AGG(DISTINCT type, ', ') as types,
    STRING_AGG(intitule, ' | ') as intitules
FROM rubriques_budgetaires
GROUP BY code
HAVING COUNT(DISTINCT type) > 1
ORDER BY code;

-- NOTES:
-- Après cette migration, les codes suivants pourront exister dans les deux types:
-- 16, 161, 162, 165, 167, 168, 1611, 1612, 1621, 1622, 1650, 1670, 1680, 1688
-- (tous liés aux EMPRUNTS ET DETTES ASSIMILEES)
