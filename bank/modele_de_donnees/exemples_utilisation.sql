-- ============================================================================
-- EXEMPLES D'UTILISATION DU MODÈLE DE DONNÉES
-- ============================================================================
-- Ce fichier contient des exemples de requêtes SQL pour exploiter le modèle
-- de données après application des migrations.
-- ============================================================================

-- ============================================================================
-- 1. GÉNÉRATION DU TABLEAU DÉTAILLÉ DES RECETTES
-- ============================================================================

-- Exemple: Générer le tableau de recettes pour une commune donnée, année 2024
WITH recettes_hierarchiques AS (
    SELECT
        r1.code as code_niveau_1,
        r1.intitule as intitule_niveau_1,
        r2.code as code_niveau_2,
        r2.intitule as intitule_niveau_2,
        r3.code as code_niveau_3,
        r3.intitule as intitule_niveau_3,
        r3.id as rubrique_id,
        COALESCE(r3.niveau, r2.niveau, r1.niveau) as niveau_max
    FROM rubriques_budgetaires r1
    LEFT JOIN rubriques_budgetaires r2 ON r2.parent_id = r1.id
    LEFT JOIN rubriques_budgetaires r3 ON r3.parent_id = r2.id
    WHERE r1.type = 'recette'
      AND r1.section = 'fonctionnement'
      AND r1.niveau = 1
)
SELECT
    rh.code_niveau_1,
    rh.intitule_niveau_1,
    rh.code_niveau_2,
    rh.intitule_niveau_2,
    rh.code_niveau_3,
    rh.intitule_niveau_3,

    -- Colonnes du tableau Excel
    COALESCE((lb.valeurs->>'budget_primitif')::NUMERIC, 0) as budget_primitif,
    COALESCE((lb.valeurs->>'budget_additionnel')::NUMERIC, 0) as budget_additionnel,
    COALESCE((lb.valeurs->>'modifications')::NUMERIC, 0) as modifications,
    COALESCE((lb.valeurs->>'previsions_definitives')::NUMERIC, 0) as previsions_definitives,
    COALESCE((lb.valeurs->>'or_admis')::NUMERIC, 0) as or_admis,
    COALESCE((lb.valeurs->>'recouvrement')::NUMERIC, 0) as recouvrement,
    COALESCE((lb.valeurs->>'reste_recouvrer')::NUMERIC, 0) as reste_recouvrer,
    COALESCE((lb.valeurs->>'taux_execution')::NUMERIC, 0) as taux_execution

FROM recettes_hierarchiques rh
LEFT JOIN lignes_budgetaires lb ON rh.rubrique_id = lb.rubrique_id
LEFT JOIN comptes_administratifs ca ON lb.compte_administratif_id = ca.id
WHERE ca.annee = 2024
  AND ca.commune_id = 'VOTRE_COMMUNE_ID'  -- Remplacer par l'ID réel
ORDER BY
    rh.code_niveau_1,
    rh.code_niveau_2 NULLS FIRST,
    rh.code_niveau_3 NULLS FIRST;

-- ============================================================================
-- 2. GÉNÉRATION DU TABLEAU DÉTAILLÉ DES DÉPENSES
-- ============================================================================

-- Exemple: Générer le tableau de dépenses pour une commune donnée, année 2024
WITH depenses_hierarchiques AS (
    SELECT
        r1.code as code_niveau_1,
        r1.intitule as intitule_niveau_1,
        r2.code as code_niveau_2,
        r2.intitule as intitule_niveau_2,
        r3.code as code_niveau_3,
        r3.intitule as intitule_niveau_3,
        r3.id as rubrique_id,
        COALESCE(r3.niveau, r2.niveau, r1.niveau) as niveau_max
    FROM rubriques_budgetaires r1
    LEFT JOIN rubriques_budgetaires r2 ON r2.parent_id = r1.id
    LEFT JOIN rubriques_budgetaires r3 ON r3.parent_id = r2.id
    WHERE r1.type = 'depense'
      AND r1.section = 'fonctionnement'
      AND r1.niveau = 1
)
SELECT
    dh.code_niveau_1,
    dh.intitule_niveau_1,
    dh.code_niveau_2,
    dh.intitule_niveau_2,
    dh.code_niveau_3,
    dh.intitule_niveau_3,

    -- Colonnes du tableau Excel
    COALESCE((lb.valeurs->>'budget_primitif')::NUMERIC, 0) as budget_primitif,
    COALESCE((lb.valeurs->>'budget_additionnel')::NUMERIC, 0) as budget_additionnel,
    COALESCE((lb.valeurs->>'modifications')::NUMERIC, 0) as modifications,
    COALESCE((lb.valeurs->>'previsions_definitives')::NUMERIC, 0) as previsions_definitives,
    COALESCE((lb.valeurs->>'engagement')::NUMERIC, 0) as engagement,
    COALESCE((lb.valeurs->>'mandat_admis')::NUMERIC, 0) as mandat_admis,
    COALESCE((lb.valeurs->>'paiement')::NUMERIC, 0) as paiement,
    COALESCE((lb.valeurs->>'reste_payer')::NUMERIC, 0) as reste_payer,
    COALESCE((lb.valeurs->>'taux_execution')::NUMERIC, 0) as taux_execution

FROM depenses_hierarchiques dh
LEFT JOIN lignes_budgetaires lb ON dh.rubrique_id = lb.rubrique_id
LEFT JOIN comptes_administratifs ca ON lb.compte_administratif_id = ca.id
WHERE ca.annee = 2024
  AND ca.commune_id = 'VOTRE_COMMUNE_ID'  -- Remplacer par l'ID réel
ORDER BY
    dh.code_niveau_1,
    dh.code_niveau_2 NULLS FIRST,
    dh.code_niveau_3 NULLS FIRST;

-- ============================================================================
-- 3. GÉNÉRATION DU TABLEAU D'ÉQUILIBRE
-- ============================================================================

-- Utilisation de la vue créée par la migration 001
SELECT
    annee,

    -- Récupérer les totaux de fonctionnement
    total_depenses_fonct,
    total_recettes_fonct,
    solde_fonctionnement,

    -- Détails des sections (format JSONB)
    depenses_fonctionnement,
    recettes_fonctionnement,
    depenses_investissement,
    recettes_investissement

FROM v_equilibre_compte_administratif
WHERE commune_id = 'VOTRE_COMMUNE_ID'  -- Remplacer par l'ID réel
  AND annee = 2024;

-- ============================================================================
-- 4. INSERTION DE DONNÉES POUR UN COMPTE ADMINISTRATIF
-- ============================================================================

-- Exemple: Créer un compte administratif pour une commune
DO $$
DECLARE
    v_compte_admin_id UUID;
    v_commune_id UUID := 'VOTRE_COMMUNE_ID';  -- Remplacer par l'ID réel
    v_annee INTEGER := 2024;
    v_rubrique_id UUID;
BEGIN
    -- 1. Créer le compte administratif
    INSERT INTO comptes_administratifs (
        commune_id,
        annee,
        statut,
        created_by
    ) VALUES (
        v_commune_id,
        v_annee,
        'brouillon',
        NULL  -- Remplacer par l'ID de l'utilisateur connecté
    ) RETURNING id INTO v_compte_admin_id;

    RAISE NOTICE 'Compte administratif créé: %', v_compte_admin_id;

    -- 2. Insérer une ligne budgétaire (exemple: compte 7080 - Impôt synthétique)
    SELECT id INTO v_rubrique_id
    FROM rubriques_budgetaires
    WHERE code = '7080'
    LIMIT 1;

    INSERT INTO lignes_budgetaires (
        compte_administratif_id,
        rubrique_id,
        valeurs
    ) VALUES (
        v_compte_admin_id,
        v_rubrique_id,
        jsonb_build_object(
            'budget_primitif', 1000000,
            'budget_additionnel', 50000,
            'modifications', 0,
            'or_admis', 900000,
            'recouvrement', 850000
        )
    );

    -- Les valeurs calculées (previsions_definitives, reste_recouvrer, taux_execution)
    -- seront automatiquement calculées par le trigger

    RAISE NOTICE 'Ligne budgétaire créée pour la rubrique %', v_rubrique_id;

END $$;

-- ============================================================================
-- 5. AGRÉGATION DES TOTAUX PAR COMPTE PRINCIPAL (NIVEAU 1)
-- ============================================================================

-- Exemple: Calculer les totaux de recettes par compte de niveau 1
SELECT
    r1.code,
    r1.intitule,
    SUM(COALESCE((lb.valeurs->>'budget_primitif')::NUMERIC, 0)) as total_budget_primitif,
    SUM(COALESCE((lb.valeurs->>'or_admis')::NUMERIC, 0)) as total_or_admis,
    SUM(COALESCE((lb.valeurs->>'recouvrement')::NUMERIC, 0)) as total_recouvrement,
    SUM(COALESCE((lb.valeurs->>'reste_recouvrer')::NUMERIC, 0)) as total_reste_recouvrer
FROM rubriques_budgetaires r1
LEFT JOIN rubriques_budgetaires r2 ON r2.parent_id = r1.id
LEFT JOIN rubriques_budgetaires r3 ON r3.parent_id = r2.id
LEFT JOIN lignes_budgetaires lb ON lb.rubrique_id IN (r1.id, r2.id, r3.id)
LEFT JOIN comptes_administratifs ca ON lb.compte_administratif_id = ca.id
WHERE r1.type = 'recette'
  AND r1.niveau = 1
  AND ca.annee = 2024
  AND ca.commune_id = 'VOTRE_COMMUNE_ID'  -- Remplacer par l'ID réel
GROUP BY r1.code, r1.intitule
ORDER BY r1.code;

-- ============================================================================
-- 6. COMPARAISON INTER-ANNUELLE
-- ============================================================================

-- Exemple: Comparer les recettes entre 2023 et 2024
WITH recettes_2023 AS (
    SELECT
        rb.code,
        rb.intitule,
        SUM(COALESCE((lb.valeurs->>'or_admis')::NUMERIC, 0)) as or_admis_2023
    FROM lignes_budgetaires lb
    JOIN rubriques_budgetaires rb ON lb.rubrique_id = rb.id
    JOIN comptes_administratifs ca ON lb.compte_administratif_id = ca.id
    WHERE rb.type = 'recette'
      AND rb.niveau = 1
      AND ca.annee = 2023
      AND ca.commune_id = 'VOTRE_COMMUNE_ID'
    GROUP BY rb.code, rb.intitule
),
recettes_2024 AS (
    SELECT
        rb.code,
        rb.intitule,
        SUM(COALESCE((lb.valeurs->>'or_admis')::NUMERIC, 0)) as or_admis_2024
    FROM lignes_budgetaires lb
    JOIN rubriques_budgetaires rb ON lb.rubrique_id = rb.id
    JOIN comptes_administratifs ca ON lb.compte_administratif_id = ca.id
    WHERE rb.type = 'recette'
      AND rb.niveau = 1
      AND ca.annee = 2024
      AND ca.commune_id = 'VOTRE_COMMUNE_ID'
    GROUP BY rb.code, rb.intitule
)
SELECT
    COALESCE(r23.code, r24.code) as code,
    COALESCE(r23.intitule, r24.intitule) as intitule,
    COALESCE(r23.or_admis_2023, 0) as or_admis_2023,
    COALESCE(r24.or_admis_2024, 0) as or_admis_2024,
    COALESCE(r24.or_admis_2024, 0) - COALESCE(r23.or_admis_2023, 0) as evolution,
    CASE
        WHEN COALESCE(r23.or_admis_2023, 0) > 0 THEN
            ROUND((COALESCE(r24.or_admis_2024, 0) - COALESCE(r23.or_admis_2023, 0)) / r23.or_admis_2023 * 100, 2)
        ELSE
            NULL
    END as evolution_pct
FROM recettes_2023 r23
FULL OUTER JOIN recettes_2024 r24 ON r23.code = r24.code
ORDER BY code;

-- ============================================================================
-- 7. EXPORT AU FORMAT EXCEL (via COPY)
-- ============================================================================

-- Exemple: Exporter les recettes au format CSV pour import dans Excel
-- (À exécuter via psql ou un client PostgreSQL)

/*
COPY (
    WITH recettes_hierarchiques AS (
        SELECT
            r1.code as code_niveau_1,
            r1.intitule as intitule_niveau_1,
            r2.code as code_niveau_2,
            r2.intitule as intitule_niveau_2,
            r3.code as code_niveau_3,
            r3.intitule as intitule_niveau_3,
            r3.id as rubrique_id
        FROM rubriques_budgetaires r1
        LEFT JOIN rubriques_budgetaires r2 ON r2.parent_id = r1.id
        LEFT JOIN rubriques_budgetaires r3 ON r3.parent_id = r2.id
        WHERE r1.type = 'recette' AND r1.section = 'fonctionnement' AND r1.niveau = 1
    )
    SELECT
        rh.code_niveau_1 as "COMPTE_N1",
        rh.code_niveau_2 as "COMPTE_N2",
        rh.code_niveau_3 as "COMPTE_N3",
        COALESCE(rh.intitule_niveau_3, rh.intitule_niveau_2, rh.intitule_niveau_1) as "INTITULE",
        COALESCE((lb.valeurs->>'budget_primitif')::NUMERIC, 0) as "BUDGET PRIMITIF",
        COALESCE((lb.valeurs->>'or_admis')::NUMERIC, 0) as "OR ADMIS",
        COALESCE((lb.valeurs->>'recouvrement')::NUMERIC, 0) as "RECOUVREMENT",
        COALESCE((lb.valeurs->>'reste_recouvrer')::NUMERIC, 0) as "RESTE A RECOUVRER"
    FROM recettes_hierarchiques rh
    LEFT JOIN lignes_budgetaires lb ON rh.rubrique_id = lb.rubrique_id
    LEFT JOIN comptes_administratifs ca ON lb.compte_administratif_id = ca.id
    WHERE ca.annee = 2024 AND ca.commune_id = 'VOTRE_COMMUNE_ID'
    ORDER BY rh.code_niveau_1, rh.code_niveau_2, rh.code_niveau_3
) TO '/tmp/recettes_2024.csv' WITH (FORMAT CSV, HEADER, DELIMITER ';', ENCODING 'UTF8');
*/

-- ============================================================================
-- 8. REQUÊTES UTILITAIRES
-- ============================================================================

-- 8.1 Lister toutes les colonnes dynamiques et leur applicabilité
SELECT
    code,
    nom,
    applicable_a,
    type_donnee,
    est_calculee,
    ordre
FROM colonnes_dynamiques
WHERE est_active = TRUE
ORDER BY ordre;

-- 8.2 Compter le nombre de rubriques par type/section/niveau
SELECT
    type,
    section,
    niveau,
    COUNT(*) as nombre
FROM rubriques_budgetaires
WHERE est_active = TRUE
GROUP BY type, section, niveau
ORDER BY type, section, niveau;

-- 8.3 Vérifier la cohérence des valeurs calculées
-- (Les valeurs calculées doivent correspondre aux formules)
SELECT
    ca.annee,
    rb.code,
    rb.intitule,
    lb.valeurs->>'budget_primitif' as bp,
    lb.valeurs->>'budget_additionnel' as ba,
    lb.valeurs->>'modifications' as modif,
    lb.valeurs->>'previsions_definitives' as prev_def_calculee,
    (
        COALESCE((lb.valeurs->>'budget_primitif')::NUMERIC, 0) +
        COALESCE((lb.valeurs->>'budget_additionnel')::NUMERIC, 0) +
        COALESCE((lb.valeurs->>'modifications')::NUMERIC, 0)
    ) as prev_def_attendue
FROM lignes_budgetaires lb
JOIN comptes_administratifs ca ON lb.compte_administratif_id = ca.id
JOIN rubriques_budgetaires rb ON lb.rubrique_id = rb.id
WHERE ca.annee = 2024
  AND (
      COALESCE((lb.valeurs->>'previsions_definitives')::NUMERIC, 0) !=
      (
          COALESCE((lb.valeurs->>'budget_primitif')::NUMERIC, 0) +
          COALESCE((lb.valeurs->>'budget_additionnel')::NUMERIC, 0) +
          COALESCE((lb.valeurs->>'modifications')::NUMERIC, 0)
      )
  );

-- ============================================================================
-- FIN DES EXEMPLES
-- ============================================================================
