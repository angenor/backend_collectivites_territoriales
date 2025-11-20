-- ============================================================================
-- Script d'insertion de données de test complètes
-- Permet de tester immédiatement le système avec des valeurs réalistes
-- ============================================================================

-- ============================================================================
-- ÉTAPE 1: CRÉER DES COLLECTIVITÉS DE TEST
-- ============================================================================

-- Créer une région de test
INSERT INTO regions (code, nom, description, chef_lieu, superficie, created_at)
VALUES ('RG-TEST', 'Région Test', 'Région créée pour les tests', 'Chef-lieu Test', 50000.00, NOW())
ON CONFLICT (code) DO NOTHING;

-- Créer un district de test
INSERT INTO districts (code, nom, region_id, description, chef_lieu, superficie, created_at)
SELECT 'DT-TEST', 'District Test', r.id, 'District créé pour les tests', 'Chef-lieu District', 10000.00, NOW()
FROM regions r
WHERE r.code = 'RG-TEST'
ON CONFLICT (code) DO NOTHING;

-- Créer une commune de test
INSERT INTO communes (code, nom, district_id, description, population, superficie, maire, created_at)
SELECT 'COM-TEST', 'Commune Test', d.id, 'Commune créée pour les tests', 25000, 500.00, 'Maire Test', NOW()
FROM districts d
WHERE d.code = 'DT-TEST'
ON CONFLICT (code) DO NOTHING;

-- ============================================================================
-- ÉTAPE 2: CRÉER UN COMPTE ADMINISTRATIF DE TEST POUR 2024
-- ============================================================================

-- Supprimer le compte existant si présent
DELETE FROM comptes_administratifs
WHERE annee = 2024
  AND commune_id IN (SELECT id FROM communes WHERE code = 'COM-TEST');

-- Créer le compte administratif
INSERT INTO comptes_administratifs (commune_id, annee, statut, notes, created_at)
SELECT
    c.id,
    2024,
    'brouillon',
    'Compte administratif de test - Données générées automatiquement',
    NOW()
FROM communes c
WHERE c.code = 'COM-TEST';

-- ============================================================================
-- ÉTAPE 3: INSÉRER DES LIGNES BUDGÉTAIRES POUR LES RECETTES
-- ============================================================================

-- Récupérer l'ID du compte administratif
DO $$
DECLARE
    v_compte_id UUID;
    v_rubrique_id UUID;
BEGIN
    -- Obtenir l'ID du compte
    SELECT ca.id INTO v_compte_id
    FROM comptes_administratifs ca
    JOIN communes c ON ca.commune_id = c.id
    WHERE c.code = 'COM-TEST' AND ca.annee = 2024;

    -- Insérer des données pour les principales rubriques de RECETTES

    -- 70 - IMPOTS SUR LES REVENUS, BENEFICES ET GAINS
    SELECT id INTO v_rubrique_id FROM rubriques_budgetaires WHERE code = '70' AND type = 'recette' LIMIT 1;
    IF v_rubrique_id IS NOT NULL THEN
        INSERT INTO lignes_budgetaires (compte_administratif_id, rubrique_id, valeurs)
        VALUES (v_compte_id, v_rubrique_id, jsonb_build_object(
            'budget_primitif', 5000000,
            'budget_additionnel', 200000,
            'modifications', -50000,
            'or_admis', 4800000,
            'recouvrement', 4500000
        ));
    END IF;

    -- 71 - IMPOTS SUR LE PATRIMOINE
    SELECT id INTO v_rubrique_id FROM rubriques_budgetaires WHERE code = '71' AND type = 'recette' LIMIT 1;
    IF v_rubrique_id IS NOT NULL THEN
        INSERT INTO lignes_budgetaires (compte_administratif_id, rubrique_id, valeurs)
        VALUES (v_compte_id, v_rubrique_id, jsonb_build_object(
            'budget_primitif', 12000000,
            'budget_additionnel', 500000,
            'modifications', 100000,
            'or_admis', 12200000,
            'recouvrement', 11800000
        ));
    END IF;

    -- 72 - IMPOTS SUR LES BIENS ET SERVICES
    SELECT id INTO v_rubrique_id FROM rubriques_budgetaires WHERE code = '72' AND type = 'recette' LIMIT 1;
    IF v_rubrique_id IS NOT NULL THEN
        INSERT INTO lignes_budgetaires (compte_administratif_id, rubrique_id, valeurs)
        VALUES (v_compte_id, v_rubrique_id, jsonb_build_object(
            'budget_primitif', 8000000,
            'budget_additionnel', 300000,
            'modifications', 0,
            'or_admis', 8100000,
            'recouvrement', 7900000
        ));
    END IF;

    -- 74 - AUTRES RECETTES FISCALES
    SELECT id INTO v_rubrique_id FROM rubriques_budgetaires WHERE code = '74' AND type = 'recette' LIMIT 1;
    IF v_rubrique_id IS NOT NULL THEN
        INSERT INTO lignes_budgetaires (compte_administratif_id, rubrique_id, valeurs)
        VALUES (v_compte_id, v_rubrique_id, jsonb_build_object(
            'budget_primitif', 3000000,
            'budget_additionnel', 100000,
            'modifications', 50000,
            'or_admis', 3000000,
            'recouvrement', 2850000
        ));
    END IF;

    -- 75 - CONTRIBUTIONS RECUES DES TIERS
    SELECT id INTO v_rubrique_id FROM rubriques_budgetaires WHERE code = '75' AND type = 'recette' LIMIT 1;
    IF v_rubrique_id IS NOT NULL THEN
        INSERT INTO lignes_budgetaires (compte_administratif_id, rubrique_id, valeurs)
        VALUES (v_compte_id, v_rubrique_id, jsonb_build_object(
            'budget_primitif', 15000000,
            'budget_additionnel', 2000000,
            'modifications', 500000,
            'or_admis', 17000000,
            'recouvrement', 16500000
        ));
    END IF;

    -- 76 - PRODUITS FINANCIERS
    SELECT id INTO v_rubrique_id FROM rubriques_budgetaires WHERE code = '76' AND type = 'recette' LIMIT 1;
    IF v_rubrique_id IS NOT NULL THEN
        INSERT INTO lignes_budgetaires (compte_administratif_id, rubrique_id, valeurs)
        VALUES (v_compte_id, v_rubrique_id, jsonb_build_object(
            'budget_primitif', 500000,
            'budget_additionnel', 0,
            'modifications', 0,
            'or_admis', 480000,
            'recouvrement', 450000
        ));
    END IF;

    -- 77 - RECETTES NON FISCALES
    SELECT id INTO v_rubrique_id FROM rubriques_budgetaires WHERE code = '77' AND type = 'recette' LIMIT 1;
    IF v_rubrique_id IS NOT NULL THEN
        INSERT INTO lignes_budgetaires (compte_administratif_id, rubrique_id, valeurs)
        VALUES (v_compte_id, v_rubrique_id, jsonb_build_object(
            'budget_primitif', 6000000,
            'budget_additionnel', 400000,
            'modifications', -100000,
            'or_admis', 6200000,
            'recouvrement', 5900000
        ));
    END IF;

    RAISE NOTICE 'Lignes budgétaires RECETTES insérées avec succès';
END $$;

-- ============================================================================
-- ÉTAPE 4: INSÉRER DES LIGNES BUDGÉTAIRES POUR LES DÉPENSES
-- ============================================================================

DO $$
DECLARE
    v_compte_id UUID;
    v_rubrique_id UUID;
BEGIN
    -- Obtenir l'ID du compte
    SELECT ca.id INTO v_compte_id
    FROM comptes_administratifs ca
    JOIN communes c ON ca.commune_id = c.id
    WHERE c.code = 'COM-TEST' AND ca.annee = 2024;

    -- Insérer des données pour les principales rubriques de DÉPENSES

    -- 60 - CHARGES DE PERSONNEL
    SELECT id INTO v_rubrique_id FROM rubriques_budgetaires WHERE code = '60' AND type = 'depense' LIMIT 1;
    IF v_rubrique_id IS NOT NULL THEN
        INSERT INTO lignes_budgetaires (compte_administratif_id, rubrique_id, valeurs)
        VALUES (v_compte_id, v_rubrique_id, jsonb_build_object(
            'budget_primitif', 18000000,
            'budget_additionnel', 1000000,
            'modifications', 200000,
            'engagement', 19000000,
            'mandat_admis', 18800000,
            'paiement', 18500000
        ));
    END IF;

    -- 61 - ACHATS DE BIENS
    SELECT id INTO v_rubrique_id FROM rubriques_budgetaires WHERE code = '61' AND type = 'depense' LIMIT 1;
    IF v_rubrique_id IS NOT NULL THEN
        INSERT INTO lignes_budgetaires (compte_administratif_id, rubrique_id, valeurs)
        VALUES (v_compte_id, v_rubrique_id, jsonb_build_object(
            'budget_primitif', 5000000,
            'budget_additionnel', 300000,
            'modifications', 0,
            'engagement', 5200000,
            'mandat_admis', 5100000,
            'paiement', 4900000
        ));
    END IF;

    -- 62 - ACHATS DE SERVICES ET CHARGES PERMANENTES
    SELECT id INTO v_rubrique_id FROM rubriques_budgetaires WHERE code = '62' AND type = 'depense' LIMIT 1;
    IF v_rubrique_id IS NOT NULL THEN
        INSERT INTO lignes_budgetaires (compte_administratif_id, rubrique_id, valeurs)
        VALUES (v_compte_id, v_rubrique_id, jsonb_build_object(
            'budget_primitif', 8000000,
            'budget_additionnel', 500000,
            'modifications', -200000,
            'engagement', 8200000,
            'mandat_admis', 8000000,
            'paiement', 7800000
        ));
    END IF;

    -- 63 - DÉPENSES D'INTERVENTION
    SELECT id INTO v_rubrique_id FROM rubriques_budgetaires WHERE code = '63' AND type = 'depense' LIMIT 1;
    IF v_rubrique_id IS NOT NULL THEN
        INSERT INTO lignes_budgetaires (compte_administratif_id, rubrique_id, valeurs)
        VALUES (v_compte_id, v_rubrique_id, jsonb_build_object(
            'budget_primitif', 10000000,
            'budget_additionnel', 800000,
            'modifications', 300000,
            'engagement', 10800000,
            'mandat_admis', 10500000,
            'paiement', 10200000
        ));
    END IF;

    -- 64 - IMPOTS ET TAXES
    SELECT id INTO v_rubrique_id FROM rubriques_budgetaires WHERE code = '64' AND type = 'depense' LIMIT 1;
    IF v_rubrique_id IS NOT NULL THEN
        INSERT INTO lignes_budgetaires (compte_administratif_id, rubrique_id, valeurs)
        VALUES (v_compte_id, v_rubrique_id, jsonb_build_object(
            'budget_primitif', 1000000,
            'budget_additionnel', 0,
            'modifications', 0,
            'engagement', 980000,
            'mandat_admis', 950000,
            'paiement', 950000
        ));
    END IF;

    -- 65 - TRANSFERTS ET SUBVENTIONS
    SELECT id INTO v_rubrique_id FROM rubriques_budgetaires WHERE code = '65' AND type = 'depense' LIMIT 1;
    IF v_rubrique_id IS NOT NULL THEN
        INSERT INTO lignes_budgetaires (compte_administratif_id, rubrique_id, valeurs)
        VALUES (v_compte_id, v_rubrique_id, jsonb_build_object(
            'budget_primitif', 4000000,
            'budget_additionnel', 200000,
            'modifications', 100000,
            'engagement', 4200000,
            'mandat_admis', 4100000,
            'paiement', 3900000
        ));
    END IF;

    -- 66 - CHARGES FINANCIERES
    SELECT id INTO v_rubrique_id FROM rubriques_budgetaires WHERE code = '66' AND type = 'depense' LIMIT 1;
    IF v_rubrique_id IS NOT NULL THEN
        INSERT INTO lignes_budgetaires (compte_administratif_id, rubrique_id, valeurs)
        VALUES (v_compte_id, v_rubrique_id, jsonb_build_object(
            'budget_primitif', 2000000,
            'budget_additionnel', 100000,
            'modifications', 0,
            'engagement', 2050000,
            'mandat_admis', 2000000,
            'paiement', 2000000
        ));
    END IF;

    -- 67 - CHARGES DIVERSES
    SELECT id INTO v_rubrique_id FROM rubriques_budgetaires WHERE code = '67' AND type = 'depense' LIMIT 1;
    IF v_rubrique_id IS NOT NULL THEN
        INSERT INTO lignes_budgetaires (compte_administratif_id, rubrique_id, valeurs)
        VALUES (v_compte_id, v_rubrique_id, jsonb_build_object(
            'budget_primitif', 1500000,
            'budget_additionnel', 100000,
            'modifications', -50000,
            'engagement', 1550000,
            'mandat_admis', 1500000,
            'paiement', 1450000
        ));
    END IF;

    RAISE NOTICE 'Lignes budgétaires DÉPENSES insérées avec succès';
END $$;

-- ============================================================================
-- ÉTAPE 5: VÉRIFICATIONS ET RÉSULTATS
-- ============================================================================

-- Afficher le compte administratif créé
SELECT
    ca.id,
    ca.annee,
    c.nom as commune,
    ca.statut,
    ca.notes
FROM comptes_administratifs ca
JOIN communes c ON ca.commune_id = c.id
WHERE c.code = 'COM-TEST' AND ca.annee = 2024;

-- Afficher les totaux des recettes
SELECT
    'RECETTES' as type,
    COUNT(*) as nb_lignes,
    SUM((valeurs->>'budget_primitif')::numeric) as budget_primitif,
    SUM((valeurs->>'or_admis')::numeric) as or_admis,
    SUM((valeurs->>'recouvrement')::numeric) as recouvrement
FROM lignes_budgetaires lb
JOIN rubriques_budgetaires rb ON lb.rubrique_id = rb.id
JOIN comptes_administratifs ca ON lb.compte_administratif_id = ca.id
JOIN communes c ON ca.commune_id = c.id
WHERE c.code = 'COM-TEST'
  AND ca.annee = 2024
  AND rb.type = 'recette';

-- Afficher les totaux des dépenses
SELECT
    'DÉPENSES' as type,
    COUNT(*) as nb_lignes,
    SUM((valeurs->>'budget_primitif')::numeric) as budget_primitif,
    SUM((valeurs->>'mandat_admis')::numeric) as mandat_admis,
    SUM((valeurs->>'paiement')::numeric) as paiement
FROM lignes_budgetaires lb
JOIN rubriques_budgetaires rb ON lb.rubrique_id = rb.id
JOIN comptes_administratifs ca ON lb.compte_administratif_id = ca.id
JOIN communes c ON ca.commune_id = c.id
WHERE c.code = 'COM-TEST'
  AND ca.annee = 2024
  AND rb.type = 'depense';

-- ============================================================================
-- INSTRUCTIONS D'UTILISATION
-- ============================================================================

/*
✅ Ce script a créé:
   - 1 région de test (RG-TEST)
   - 1 district de test (DT-TEST)
   - 1 commune de test (COM-TEST)
   - 1 compte administratif pour l'année 2024
   - 7 lignes de recettes avec des valeurs réalistes
   - 8 lignes de dépenses avec des valeurs réalistes

📊 Pour visualiser les données:

1. Tableau d'équilibre:
   Allez sur: /admin/comptes-administratifs/equilibre
   Sélectionnez: Année 2024, Commune, "Commune Test"

2. Saisie des lignes budgétaires:
   Allez sur: /admin/comptes-administratifs/lignes-budgetaires
   Sélectionnez: Année 2024, Commune, "Commune Test"

3. Requête SQL pour voir l'équilibre:
   SELECT * FROM v_equilibre_compte_administratif
   WHERE annee = 2024;

4. Extraction des données comme dans Excel:

   -- RECETTES détaillées
   SELECT
       rb.code,
       rb.intitule,
       (lb.valeurs->>'budget_primitif')::numeric as budget_primitif,
       (lb.valeurs->>'or_admis')::numeric as or_admis,
       (lb.valeurs->>'recouvrement')::numeric as recouvrement
   FROM lignes_budgetaires lb
   JOIN rubriques_budgetaires rb ON lb.rubrique_id = rb.id
   JOIN comptes_administratifs ca ON lb.compte_administratif_id = ca.id
   WHERE ca.annee = 2024 AND rb.type = 'recette'
   ORDER BY rb.ordre;

   -- DÉPENSES détaillées
   SELECT
       rb.code,
       rb.intitule,
       (lb.valeurs->>'budget_primitif')::numeric as budget_primitif,
       (lb.valeurs->>'mandat_admis')::numeric as mandat_admis,
       (lb.valeurs->>'paiement')::numeric as paiement
   FROM lignes_budgetaires lb
   JOIN rubriques_budgetaires rb ON lb.rubrique_id = rb.id
   JOIN comptes_administratifs ca ON lb.compte_administratif_id = ca.id
   WHERE ca.annee = 2024 AND rb.type = 'depense'
   ORDER BY rb.ordre;

💡 Vous pouvez maintenant:
   - Modifier les montants via l'interface web
   - Ajouter d'autres rubriques
   - Créer d'autres comptes administratifs
   - Exporter les données au format Excel
*/
