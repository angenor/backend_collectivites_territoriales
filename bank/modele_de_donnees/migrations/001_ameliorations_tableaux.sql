-- ============================================================================
-- MIGRATION: Améliorations pour reproduction exacte des tableaux Excel
-- ============================================================================
-- Description: Ajout de champs et fonctions pour reproduire fidèlement
--              les tableaux de compte administratif (RECETTE, DEPENSE, EQUILIBRE)
-- Date: 2025-11-16
-- ============================================================================

-- ============================================================================
-- 1. AMÉLIORATION DE LA TABLE COLONNES_DYNAMIQUES
-- ============================================================================

-- Ajouter le champ 'applicable_a' pour différencier recettes et dépenses
ALTER TABLE colonnes_dynamiques
ADD COLUMN IF NOT EXISTS applicable_a VARCHAR(50) CHECK (applicable_a IN ('recette', 'depense', 'tous', 'equilibre')) DEFAULT 'tous';

COMMENT ON COLUMN colonnes_dynamiques.applicable_a IS 'Indique si la colonne s''applique aux recettes, dépenses, les deux ou l''équilibre';

-- Mettre à jour les colonnes existantes avec leur applicabilité
UPDATE colonnes_dynamiques SET applicable_a = 'recette' WHERE code IN ('or_admis', 'recouvrement', 'reste_recouvrer');
UPDATE colonnes_dynamiques SET applicable_a = 'depense' WHERE code IN ('engagement', 'mandat_admis', 'paiement', 'reste_payer');
UPDATE colonnes_dynamiques SET applicable_a = 'tous' WHERE code IN ('compte', 'budget_primitif', 'budget_additionnel', 'modifications', 'previsions_definitives', 'taux_execution');

-- ============================================================================
-- 2. AMÉLIORATION DU TRIGGER DE CALCUL AUTOMATIQUE
-- ============================================================================

-- Remplacer la fonction de calcul avec toutes les formules
CREATE OR REPLACE FUNCTION calculer_valeurs_derivees()
RETURNS TRIGGER AS $$
DECLARE
    bp NUMERIC;
    ba NUMERIC;
    modif NUMERIC;
    prev_def NUMERIC;
    or_admis NUMERIC;
    mandat_admis NUMERIC;
    recouvrement NUMERIC;
    paiement NUMERIC;
    engagement NUMERIC;
    rubrique_type VARCHAR(50);
BEGIN
    -- Récupérer le type de rubrique (recette ou depense)
    SELECT type INTO rubrique_type
    FROM rubriques_budgetaires
    WHERE id = NEW.rubrique_id;

    -- Extraire les valeurs du JSONB (avec défaut à 0)
    bp := COALESCE((NEW.valeurs->>'budget_primitif')::NUMERIC, 0);
    ba := COALESCE((NEW.valeurs->>'budget_additionnel')::NUMERIC, 0);
    modif := COALESCE((NEW.valeurs->>'modifications')::NUMERIC, 0);
    or_admis := COALESCE((NEW.valeurs->>'or_admis')::NUMERIC, 0);
    mandat_admis := COALESCE((NEW.valeurs->>'mandat_admis')::NUMERIC, 0);
    recouvrement := COALESCE((NEW.valeurs->>'recouvrement')::NUMERIC, 0);
    paiement := COALESCE((NEW.valeurs->>'paiement')::NUMERIC, 0);
    engagement := COALESCE((NEW.valeurs->>'engagement')::NUMERIC, 0);

    -- ========================================================================
    -- CALCULS COMMUNS (Recettes ET Dépenses)
    -- ========================================================================

    -- 1. PRÉVISIONS DÉFINITIVES = Budget Primitif + Budget Additionnel + Modifications
    prev_def := bp + ba + modif;
    NEW.valeurs = jsonb_set(
        NEW.valeurs,
        ARRAY['previsions_definitives'],
        to_jsonb(prev_def)
    );

    -- ========================================================================
    -- CALCULS SPÉCIFIQUES AUX RECETTES
    -- ========================================================================

    IF rubrique_type = 'recette' THEN
        -- 2. RESTE À RECOUVRER = OR Admis - Recouvrement
        NEW.valeurs = jsonb_set(
            NEW.valeurs,
            ARRAY['reste_recouvrer'],
            to_jsonb(or_admis - recouvrement)
        );

        -- 3. TAUX D'EXÉCUTION (Recettes) = (OR Admis / Prévisions Définitives) × 100
        IF prev_def != 0 THEN
            NEW.valeurs = jsonb_set(
                NEW.valeurs,
                ARRAY['taux_execution'],
                to_jsonb(ROUND((or_admis / prev_def) * 100, 2))
            );
        ELSE
            NEW.valeurs = jsonb_set(
                NEW.valeurs,
                ARRAY['taux_execution'],
                to_jsonb(0)
            );
        END IF;
    END IF;

    -- ========================================================================
    -- CALCULS SPÉCIFIQUES AUX DÉPENSES
    -- ========================================================================

    IF rubrique_type = 'depense' THEN
        -- 4. RESTE À PAYER = Mandat Admis - Paiement
        NEW.valeurs = jsonb_set(
            NEW.valeurs,
            ARRAY['reste_payer'],
            to_jsonb(mandat_admis - paiement)
        );

        -- 5. TAUX D'EXÉCUTION (Dépenses) = (Mandat Admis / Prévisions Définitives) × 100
        IF prev_def != 0 THEN
            NEW.valeurs = jsonb_set(
                NEW.valeurs,
                ARRAY['taux_execution'],
                to_jsonb(ROUND((mandat_admis / prev_def) * 100, 2))
            );
        ELSE
            NEW.valeurs = jsonb_set(
                NEW.valeurs,
                ARRAY['taux_execution'],
                to_jsonb(0)
            );
        END IF;
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

COMMENT ON FUNCTION calculer_valeurs_derivees() IS 'Calcule automatiquement les valeurs dérivées (prévisions définitives, restes, taux) pour recettes et dépenses';

-- ============================================================================
-- 3. VUE POUR LE TABLEAU D'ÉQUILIBRE
-- ============================================================================

CREATE OR REPLACE VIEW v_equilibre_compte_administratif AS
WITH
-- Agrégation des dépenses de fonctionnement
depenses_fonctionnement AS (
    SELECT
        lb.compte_administratif_id,
        rb.code,
        rb.intitule,
        SUM(COALESCE((lb.valeurs->>'mandat_admis')::NUMERIC, 0)) as mandat_admis,
        SUM(COALESCE((lb.valeurs->>'paiement')::NUMERIC, 0)) as paiement,
        SUM(COALESCE((lb.valeurs->>'reste_payer')::NUMERIC, 0)) as reste_payer
    FROM lignes_budgetaires lb
    JOIN rubriques_budgetaires rb ON lb.rubrique_id = rb.id
    WHERE rb.type = 'depense'
      AND rb.section = 'fonctionnement'
      AND rb.niveau = 1  -- Seulement les comptes principaux (60, 61, 62, etc.)
      AND rb.code ~ '^[0-9]+$'  -- Seulement les codes numériques
    GROUP BY lb.compte_administratif_id, rb.code, rb.intitule
),
-- Agrégation des recettes de fonctionnement
recettes_fonctionnement AS (
    SELECT
        lb.compte_administratif_id,
        rb.code,
        rb.intitule,
        SUM(COALESCE((lb.valeurs->>'or_admis')::NUMERIC, 0)) as or_admis,
        SUM(COALESCE((lb.valeurs->>'recouvrement')::NUMERIC, 0)) as recouvrement,
        SUM(COALESCE((lb.valeurs->>'reste_recouvrer')::NUMERIC, 0)) as reste_recouvrer
    FROM lignes_budgetaires lb
    JOIN rubriques_budgetaires rb ON lb.rubrique_id = rb.id
    WHERE rb.type = 'recette'
      AND rb.section = 'fonctionnement'
      AND rb.niveau = 1
      AND rb.code ~ '^[0-9]+$'
    GROUP BY lb.compte_administratif_id, rb.code, rb.intitule
),
-- Agrégation des dépenses d'investissement
depenses_investissement AS (
    SELECT
        lb.compte_administratif_id,
        rb.code,
        rb.intitule,
        SUM(COALESCE((lb.valeurs->>'mandat_admis')::NUMERIC, 0)) as mandat_admis,
        SUM(COALESCE((lb.valeurs->>'paiement')::NUMERIC, 0)) as paiement,
        SUM(COALESCE((lb.valeurs->>'reste_payer')::NUMERIC, 0)) as reste_payer
    FROM lignes_budgetaires lb
    JOIN rubriques_budgetaires rb ON lb.rubrique_id = rb.id
    WHERE rb.type = 'depense'
      AND rb.section = 'investissement'
      AND rb.niveau = 1
      AND rb.code ~ '^[0-9]+$'
    GROUP BY lb.compte_administratif_id, rb.code, rb.intitule
),
-- Agrégation des recettes d'investissement
recettes_investissement AS (
    SELECT
        lb.compte_administratif_id,
        rb.code,
        rb.intitule,
        SUM(COALESCE((lb.valeurs->>'or_admis')::NUMERIC, 0)) as or_admis,
        SUM(COALESCE((lb.valeurs->>'recouvrement')::NUMERIC, 0)) as recouvrement,
        SUM(COALESCE((lb.valeurs->>'reste_recouvrer')::NUMERIC, 0)) as reste_recouvrer
    FROM lignes_budgetaires lb
    JOIN rubriques_budgetaires rb ON lb.rubrique_id = rb.id
    WHERE rb.type = 'recette'
      AND rb.section = 'investissement'
      AND rb.niveau = 1
      AND rb.code ~ '^[0-9]+$'
    GROUP BY lb.compte_administratif_id, rb.code, rb.intitule
),
-- Totaux de fonctionnement
totaux_fonctionnement AS (
    SELECT
        compte_administratif_id,
        SUM(mandat_admis) as total_depenses_fonct,
        SUM(paiement) as total_paiement_fonct
    FROM depenses_fonctionnement
    GROUP BY compte_administratif_id
),
totaux_recettes_fonct AS (
    SELECT
        compte_administratif_id,
        SUM(or_admis) as total_recettes_fonct,
        SUM(recouvrement) as total_recouvrement_fonct
    FROM recettes_fonctionnement
    GROUP BY compte_administratif_id
)

-- Vue finale avec structure du tableau d'équilibre
SELECT
    ca.id as compte_administratif_id,
    ca.annee,
    ca.commune_id,
    ca.district_id,
    ca.region_id,

    -- Section Fonctionnement - Dépenses
    jsonb_agg(DISTINCT jsonb_build_object(
        'section', 'fonctionnement_depenses',
        'compte', df.code,
        'intitule', df.intitule,
        'mandat_admis', df.mandat_admis,
        'paiement', df.paiement,
        'reste_payer', df.reste_payer
    )) FILTER (WHERE df.code IS NOT NULL) as depenses_fonctionnement,

    -- Section Fonctionnement - Recettes
    jsonb_agg(DISTINCT jsonb_build_object(
        'section', 'fonctionnement_recettes',
        'compte', rf.code,
        'intitule', rf.intitule,
        'or_admis', rf.or_admis,
        'recouvrement', rf.recouvrement,
        'reste_recouvrer', rf.reste_recouvrer
    )) FILTER (WHERE rf.code IS NOT NULL) as recettes_fonctionnement,

    -- Section Investissement - Dépenses
    jsonb_agg(DISTINCT jsonb_build_object(
        'section', 'investissement_depenses',
        'compte', di.code,
        'intitule', di.intitule,
        'mandat_admis', di.mandat_admis,
        'paiement', di.paiement,
        'reste_payer', di.reste_payer
    )) FILTER (WHERE di.code IS NOT NULL) as depenses_investissement,

    -- Section Investissement - Recettes
    jsonb_agg(DISTINCT jsonb_build_object(
        'section', 'investissement_recettes',
        'compte', ri.code,
        'intitule', ri.intitule,
        'or_admis', ri.or_admis,
        'recouvrement', ri.recouvrement,
        'reste_recouvrer', ri.reste_recouvrer
    )) FILTER (WHERE ri.code IS NOT NULL) as recettes_investissement,

    -- Totaux et soldes
    tf.total_depenses_fonct,
    trf.total_recettes_fonct,
    (trf.total_recettes_fonct - tf.total_depenses_fonct) as solde_fonctionnement

FROM comptes_administratifs ca
LEFT JOIN depenses_fonctionnement df ON ca.id = df.compte_administratif_id
LEFT JOIN recettes_fonctionnement rf ON ca.id = rf.compte_administratif_id
LEFT JOIN depenses_investissement di ON ca.id = di.compte_administratif_id
LEFT JOIN recettes_investissement ri ON ca.id = ri.compte_administratif_id
LEFT JOIN totaux_fonctionnement tf ON ca.id = tf.compte_administratif_id
LEFT JOIN totaux_recettes_fonct trf ON ca.id = trf.compte_administratif_id
GROUP BY
    ca.id,
    ca.annee,
    ca.commune_id,
    ca.district_id,
    ca.region_id,
    tf.total_depenses_fonct,
    trf.total_recettes_fonct;

COMMENT ON VIEW v_equilibre_compte_administratif IS 'Vue pour générer le tableau d''équilibre du compte administratif (comme dans l''Excel)';

-- ============================================================================
-- FIN DE LA MIGRATION
-- ============================================================================
