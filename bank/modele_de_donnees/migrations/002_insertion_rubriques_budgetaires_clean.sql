-- ============================================================================
-- INSERTION DES RUBRIQUES BUDGÉTAIRES DEPUIS EXCEL
-- ============================================================================
-- Généré automatiquement depuis Tableaux_de_Compte_Administratif.xlsx
-- Nombre total de rubriques: 437
-- ============================================================================

-- Désactiver temporairement les triggers utilisateur pour améliorer les performances
ALTER TABLE rubriques_budgetaires DISABLE TRIGGER USER;

-- Supprimer les rubriques existantes (si nécessaire)
-- TRUNCATE TABLE rubriques_budgetaires CASCADE;

-- ========================================
-- Niveau 1
-- ========================================


-- ========================================
-- Niveau 1
-- ========================================

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '70',
    'IMPOTS SUR LES REVENUS, BENEFICES ET GAINS',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'recette',
    'fonctionnement',
    NULL,
    1,
    0,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '71',
    'IMPOTS SUR LE PATRIMOINE',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'recette',
    'fonctionnement',
    NULL,
    1,
    1,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '72',
    'IMPOTS SUR LES BIENS ET SERVICES',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'recette',
    'fonctionnement',
    NULL,
    1,
    2,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '74',
    'AUTRES RECETTES FISCALES',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'recette',
    'fonctionnement',
    NULL,
    1,
    3,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '75',
    'CONTRIBUTIONS RECUES DES TIERS',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'recette',
    'fonctionnement',
    NULL,
    1,
    4,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '76',
    'PRODUITS FINANCIERS',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'recette',
    'fonctionnement',
    NULL,
    1,
    5,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '77',
    'RECETTES NON FISCALES',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'recette',
    'fonctionnement',
    NULL,
    1,
    6,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '10',
    'FONDS, DOTATIONS ET RESERVES',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'recette',
    'investissement',
    NULL,
    1,
    7,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '13',
    'SUBVENTIONS D''EQUIPEMENT',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'recette',
    'investissement',
    NULL,
    1,
    8,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '14',
    'CESSIONS D''IMMOBILISATIONS',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'recette',
    'investissement',
    NULL,
    1,
    9,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '16',
    'EMPRUNTS ET DETTES ASSIMILEES',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'recette',
    'investissement',
    NULL,
    1,
    10,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '60',
    'CHARGES DE PERSONNEL',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'depense',
    'fonctionnement',
    NULL,
    1,
    12,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '61',
    'ACHATS DE BIENS',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'depense',
    'fonctionnement',
    NULL,
    1,
    13,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '62',
    'ACHATS DE SERVICES ET CHARGES PERMANENTES',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'depense',
    'fonctionnement',
    NULL,
    1,
    14,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '63',
    'DEPENSES D''INTERVENTION',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'depense',
    'fonctionnement',
    NULL,
    1,
    15,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '64',
    'IMPOTS ET TAXES',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'depense',
    'fonctionnement',
    NULL,
    1,
    16,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '65',
    'TRANSFERTS ET SUBVENTIONS',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'depense',
    'fonctionnement',
    NULL,
    1,
    17,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '66',
    'CHARGES FINANCIERES',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'depense',
    'fonctionnement',
    NULL,
    1,
    18,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '67',
    'CHARGES DIVERSES',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'depense',
    'fonctionnement',
    NULL,
    1,
    19,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '12',
    'EXCEDENT DE FONCTIONNEMENT',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'depense',
    'fonctionnement',
    NULL,
    1,
    20,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '20',
    'IMMOBILISATION INCORPORELLES',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'depense',
    'investissement',
    NULL,
    1,
    22,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '21',
    'IMMOBILISATION CORPORELLES',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'depense',
    'investissement',
    NULL,
    1,
    23,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

-- ========================================
-- Niveau 2
-- ========================================

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '708',
    'Autres impôts sur les revenus',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'recette',
    'fonctionnement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '70' LIMIT 1),
    2,
    0,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '714',
    'Impôts fonciers sur les terrains - IFT',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'recette',
    'fonctionnement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '71' LIMIT 1),
    2,
    1,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '715',
    'Impôt foncier sur les propriétés bâties – IFPB',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'recette',
    'fonctionnement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '71' LIMIT 1),
    2,
    2,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '718',
    'Taxe annuelle sur autres patrimoines',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'recette',
    'fonctionnement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '71' LIMIT 1),
    2,
    3,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '725',
    'Taxes particulières sur les biens',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'recette',
    'fonctionnement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '72' LIMIT 1),
    2,
    4,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '726',
    'Taxes particulières sur les services',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'recette',
    'fonctionnement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '72' LIMIT 1),
    2,
    5,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '727',
    'Taxes particulières sur les activités',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'recette',
    'fonctionnement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '72' LIMIT 1),
    2,
    6,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '728',
    'Autres impôts sur les biens et services',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'recette',
    'fonctionnement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '72' LIMIT 1),
    2,
    7,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '743',
    'Amendes fiscales et pénalités',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'recette',
    'fonctionnement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '74' LIMIT 1),
    2,
    8,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '748',
    'Taxes diverses',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'recette',
    'fonctionnement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '74' LIMIT 1),
    2,
    9,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '751',
    'Subvention d''exploitation - Etat',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'recette',
    'fonctionnement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '75' LIMIT 1),
    2,
    10,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '752',
    'Subventions d''exploitation reçcues des Collectivités Publiques',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'recette',
    'fonctionnement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '75' LIMIT 1),
    2,
    11,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '755',
    'Organismes privés locaux',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'recette',
    'fonctionnement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '75' LIMIT 1),
    2,
    12,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '761',
    'Produits des prises de participation',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'recette',
    'fonctionnement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '76' LIMIT 1),
    2,
    13,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '762',
    'Produits des autres immobilisations financières',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'recette',
    'fonctionnement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '76' LIMIT 1),
    2,
    14,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '763',
    'Revenus des autres créances',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'recette',
    'fonctionnement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '76' LIMIT 1),
    2,
    15,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '764',
    'Revenus des titres de placement et des prêts à court terme',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'recette',
    'fonctionnement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '76' LIMIT 1),
    2,
    16,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '768',
    'Autres produits financiers',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'recette',
    'fonctionnement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '76' LIMIT 1),
    2,
    17,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '771',
    'Redevances',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'recette',
    'fonctionnement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '77' LIMIT 1),
    2,
    18,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '772',
    'Produits des activités des services',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'recette',
    'fonctionnement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '77' LIMIT 1),
    2,
    19,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '773',
    'Produits des activités annexes et accessoires',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'recette',
    'fonctionnement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '77' LIMIT 1),
    2,
    20,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '774',
    'Production immobilisée',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'recette',
    'fonctionnement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '77' LIMIT 1),
    2,
    21,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '101',
    'Dotations et fonds divers',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'recette',
    'investissement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '10' LIMIT 1),
    2,
    22,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '106',
    'Réserves',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'recette',
    'investissement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '10' LIMIT 1),
    2,
    23,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '131',
    'Subventions d''équipement reçues',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'recette',
    'investissement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '13' LIMIT 1),
    2,
    24,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '139',
    'Subvention d''investissement transférée au compte de résultat',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'recette',
    'investissement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '13' LIMIT 1),
    2,
    25,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '141',
    'Cession d''immobilisations incorporelles',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'recette',
    'investissement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '14' LIMIT 1),
    2,
    26,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '142',
    'Cession d''immobilisations corporelles',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'recette',
    'investissement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '14' LIMIT 1),
    2,
    27,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '147',
    'Cession d''immobilisations financières',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'recette',
    'investissement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '14' LIMIT 1),
    2,
    28,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '161',
    'Emprunts en Ariary',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'recette',
    'investissement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '16' LIMIT 1),
    2,
    29,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '162',
    'Emprunts en devises',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'recette',
    'investissement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '16' LIMIT 1),
    2,
    30,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '165',
    'Dépôts et cautionnement reçus',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'recette',
    'investissement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '16' LIMIT 1),
    2,
    31,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '167',
    'Dettes sur contrat de location-financement',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'recette',
    'investissement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '16' LIMIT 1),
    2,
    32,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '168',
    'Autres emprunts et dettes assimilés',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'recette',
    'investissement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '16' LIMIT 1),
    2,
    33,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '601',
    'Salaires et accessoires',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'depense',
    'fonctionnement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '60' LIMIT 1),
    2,
    36,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '602',
    'Indemnités liées à la solde',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'depense',
    'fonctionnement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '60' LIMIT 1),
    2,
    37,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '603',
    'Indemnités et avantages liés à la fonction',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'depense',
    'fonctionnement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '60' LIMIT 1),
    2,
    38,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '604',
    'Supplément familial de traitement',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'depense',
    'fonctionnement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '60' LIMIT 1),
    2,
    39,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '606',
    'Charges sociales patronales',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'depense',
    'fonctionnement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '60' LIMIT 1),
    2,
    40,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '611',
    'Achats de biens de fonctionnement général',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'depense',
    'fonctionnement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '61' LIMIT 1),
    2,
    41,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '612',
    'Achats de biens à usage spécifique',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'depense',
    'fonctionnement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '61' LIMIT 1),
    2,
    42,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '613',
    'Carburants, Lubrifiants et combustibles',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'depense',
    'fonctionnement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '61' LIMIT 1),
    2,
    43,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '616',
    'Variation de stocks',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'depense',
    'fonctionnement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '61' LIMIT 1),
    2,
    44,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '618',
    'Autres achats',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'depense',
    'fonctionnement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '61' LIMIT 1),
    2,
    45,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '621',
    'Entretien et maintenance',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'depense',
    'fonctionnement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '62' LIMIT 1),
    2,
    46,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '622',
    'Charges de représentation, d''information, de documentation et d''encadrement',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'depense',
    'fonctionnement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '62' LIMIT 1),
    2,
    47,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '623',
    'Charges de transport',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'depense',
    'fonctionnement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '62' LIMIT 1),
    2,
    48,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '624',
    'Indemnités de mission',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'depense',
    'fonctionnement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '62' LIMIT 1),
    2,
    49,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '625',
    'Eau et éléctricité',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'depense',
    'fonctionnement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '62' LIMIT 1),
    2,
    50,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '626',
    'Poste et télécommunications',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'depense',
    'fonctionnement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '62' LIMIT 1),
    2,
    51,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '627',
    'Charges locatives',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'depense',
    'fonctionnement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '62' LIMIT 1),
    2,
    52,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '628',
    'Services divers',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'depense',
    'fonctionnement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '62' LIMIT 1),
    2,
    53,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '631',
    'Intervention sociale',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'depense',
    'fonctionnement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '63' LIMIT 1),
    2,
    54,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '632',
    'Intervention économique',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'depense',
    'fonctionnement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '63' LIMIT 1),
    2,
    55,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '633',
    'Intervention structurelle',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'depense',
    'fonctionnement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '63' LIMIT 1),
    2,
    56,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '638',
    'Dépenses d''intervention diverses et imprévues',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'depense',
    'fonctionnement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '63' LIMIT 1),
    2,
    57,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '641',
    'Taxes et impôts directs',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'depense',
    'fonctionnement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '64' LIMIT 1),
    2,
    58,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '642',
    'Taxes et impôts indirects',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'depense',
    'fonctionnement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '64' LIMIT 1),
    2,
    59,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '643',
    'Impôts, taxes et droits d''enregistrement',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'depense',
    'fonctionnement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '64' LIMIT 1),
    2,
    60,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '644',
    'Droits à l''importation',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'depense',
    'fonctionnement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '64' LIMIT 1),
    2,
    61,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '648',
    'Impôts, taxes et droits divers',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'depense',
    'fonctionnement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '64' LIMIT 1),
    2,
    62,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '651',
    'Transferts aux collectivités publiques',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'depense',
    'fonctionnement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '65' LIMIT 1),
    2,
    63,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '653',
    'Bourses',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'depense',
    'fonctionnement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '65' LIMIT 1),
    2,
    64,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '654',
    'Contributions obligatoires',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'depense',
    'fonctionnement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '65' LIMIT 1),
    2,
    65,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '655',
    'Transferts aux organismes publics',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'depense',
    'fonctionnement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '65' LIMIT 1),
    2,
    66,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '656',
    'Transferts aux privés',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'depense',
    'fonctionnement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '65' LIMIT 1),
    2,
    67,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '661',
    'Charges d''intérêt',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'depense',
    'fonctionnement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '66' LIMIT 1),
    2,
    68,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '662',
    'Intérêts banciares et opérations de financements à court terme',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'depense',
    'fonctionnement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '66' LIMIT 1),
    2,
    69,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '663',
    'Intérêts des comptes courants et des dépôts créditeurs',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'depense',
    'fonctionnement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '66' LIMIT 1),
    2,
    70,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '666',
    'Différences de change : pertes',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'depense',
    'fonctionnement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '66' LIMIT 1),
    2,
    71,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '668',
    'Autres charges financières',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'depense',
    'fonctionnement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '66' LIMIT 1),
    2,
    72,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '671',
    'Remise gracieuse, dégrèvement et perte sur titre émis',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'depense',
    'fonctionnement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '67' LIMIT 1),
    2,
    73,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '672',
    'Reversement sur trop peçu',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'depense',
    'fonctionnement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '67' LIMIT 1),
    2,
    74,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '673',
    'Déficits budgets annexes',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'depense',
    'fonctionnement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '67' LIMIT 1),
    2,
    75,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '674',
    'Frais de justice et de contentieux',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'depense',
    'fonctionnement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '67' LIMIT 1),
    2,
    76,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '675',
    'Intérêts moratoires, Amendes et Pénalités',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'depense',
    'fonctionnement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '67' LIMIT 1),
    2,
    77,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '678',
    'Autres charges diverses',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'depense',
    'fonctionnement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '67' LIMIT 1),
    2,
    78,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '201',
    'Frais de développement, de recherche et d''études',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'depense',
    'investissement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '20' LIMIT 1),
    2,
    84,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '205',
    'Concessions et droits similaires, brevets, licences, marques',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'depense',
    'investissement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '20' LIMIT 1),
    2,
    85,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '208',
    'Autres immoblisations incorporelles',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'depense',
    'investissement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '20' LIMIT 1),
    2,
    86,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '211',
    'Terrains',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'depense',
    'investissement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '21' LIMIT 1),
    2,
    87,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '212',
    'Aménagement',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'depense',
    'investissement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '21' LIMIT 1),
    2,
    88,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '213',
    'Construction ou Réhabilitation : Bâtiments',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'depense',
    'investissement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '21' LIMIT 1),
    2,
    89,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '214',
    'Construction ou Réhabilitation : Voies',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'depense',
    'investissement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '21' LIMIT 1),
    2,
    90,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '215',
    'Construction ou Réhabilitation : Réseaux',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'depense',
    'investissement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '21' LIMIT 1),
    2,
    91,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '216',
    'Matériels et outillages',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'depense',
    'investissement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '21' LIMIT 1),
    2,
    92,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '217',
    'Matériels de transoport',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'depense',
    'investissement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '21' LIMIT 1),
    2,
    93,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '218',
    'Autres immobilisations corporelles',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'depense',
    'investissement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '21' LIMIT 1),
    2,
    94,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '7151',
    'Impôt foncier sur les propriétés bâties – IFPB',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'recette',
    'fonctionnement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '715' LIMIT 1),
    3,
    2,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

-- ========================================
-- Autres niveaux
-- ========================================

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '7080',
    'Autres impôts sur les revenus - Impôt synthétique',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'recette',
    'fonctionnement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '708' LIMIT 1),
    3,
    0,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '7140',
    'Impôts fonciers sur les terrains - IFT',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'recette',
    'fonctionnement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '714' LIMIT 1),
    3,
    1,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '7158',
    'Autres impôts locaux sur les propriétés baties',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'recette',
    'fonctionnement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '715' LIMIT 1),
    3,
    3,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '7181',
    'Taxes sur les appareils automatiques ou électroniques',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'recette',
    'fonctionnement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '718' LIMIT 1),
    3,
    4,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '7182',
    'Taxes sur les appareils mecaniques',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'recette',
    'fonctionnement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '718' LIMIT 1),
    3,
    5,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '7188',
    'Autres taxes et impots annuels',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'recette',
    'fonctionnement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '718' LIMIT 1),
    3,
    6,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '7251',
    'Taxes sur l''électricité',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'recette',
    'fonctionnement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '725' LIMIT 1),
    3,
    7,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '7252',
    'Taxes sur l''eau',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'recette',
    'fonctionnement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '725' LIMIT 1),
    3,
    8,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '7253',
    'Surtaxe sur l''eau et l''électricité',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'recette',
    'fonctionnement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '725' LIMIT 1),
    3,
    9,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '7254',
    'Taxes sur les eaux minérales',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'recette',
    'fonctionnement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '725' LIMIT 1),
    3,
    10,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '7258',
    'Autres taxes particulières sur les biens',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'recette',
    'fonctionnement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '725' LIMIT 1),
    3,
    11,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '7261',
    'taxes sur la publicité',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'recette',
    'fonctionnement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '726' LIMIT 1),
    3,
    12,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '7262',
    'Taxe d’abattage',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'recette',
    'fonctionnement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '726' LIMIT 1),
    3,
    13,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '7263',
    'Taxe de visite et de poinçonnage des viandes',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'recette',
    'fonctionnement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '726' LIMIT 1),
    3,
    14,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '7268',
    'Autres taxes locales sur les services',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'recette',
    'fonctionnement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '726' LIMIT 1),
    3,
    15,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '7273',
    'Impôt de licence',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'recette',
    'fonctionnement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '727' LIMIT 1),
    3,
    16,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '7274',
    'Prélèvement sur les produits de jeux - PPJ',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'recette',
    'fonctionnement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '727' LIMIT 1),
    3,
    17,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '7276',
    'Taxes sur les fêtes, spectacles et manifestations…',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'recette',
    'fonctionnement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '727' LIMIT 1),
    3,
    18,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '7277',
    'Taxes sur les établissements exerçant des activités à but lucratif',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'recette',
    'fonctionnement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '727' LIMIT 1),
    3,
    19,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '7278',
    'Autres taxes locales sur les activités',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'recette',
    'fonctionnement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '727' LIMIT 1),
    3,
    20,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '7280',
    'Autres impôts sur les biens et services',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'recette',
    'fonctionnement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '728' LIMIT 1),
    3,
    21,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '7431',
    'Amendes fiscales',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'recette',
    'fonctionnement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '743' LIMIT 1),
    3,
    22,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '7432',
    'Pénalité',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'recette',
    'fonctionnement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '743' LIMIT 1),
    3,
    23,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '7433',
    'Intérêt moratoire',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'recette',
    'fonctionnement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '743' LIMIT 1),
    3,
    24,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '7482',
    'Droits et taxes diverses : Activités agricoles',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'recette',
    'fonctionnement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '748' LIMIT 1),
    3,
    25,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '7511',
    'Dotation globale -EPP',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'recette',
    'fonctionnement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '751' LIMIT 1),
    3,
    26,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '7512',
    'Dotation globale -CSB',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'recette',
    'fonctionnement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '751' LIMIT 1),
    3,
    27,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '7513',
    'Dotation globale -Etat civil',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'recette',
    'fonctionnement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '751' LIMIT 1),
    3,
    28,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '7518',
    'Dotation globale -Autres',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'recette',
    'fonctionnement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '751' LIMIT 1),
    3,
    29,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '7522',
    'Collectivités Territoriales Décentralisées',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'recette',
    'fonctionnement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '752' LIMIT 1),
    3,
    30,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '7523',
    'Etablissements Publics à caractère Industriel et Commercial (EPIC)',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'recette',
    'fonctionnement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '752' LIMIT 1),
    3,
    31,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '7524',
    'Etablissements Publics à caractère Administratifs (EPA)',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'recette',
    'fonctionnement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '752' LIMIT 1),
    3,
    32,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '7528',
    'Autres Collectivités Publiques',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'recette',
    'fonctionnement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '752' LIMIT 1),
    3,
    33,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '7550',
    'organisme privée locaux',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'recette',
    'fonctionnement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '755' LIMIT 1),
    3,
    34,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '7610',
    'Produits des prises de participation',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'recette',
    'fonctionnement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '761' LIMIT 1),
    3,
    35,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '7621',
    'Revenus des obligations et bons à plus d''un an',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'recette',
    'fonctionnement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '762' LIMIT 1),
    3,
    36,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '7622',
    'Revenus des prêts à long et moyen terme',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'recette',
    'fonctionnement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '762' LIMIT 1),
    3,
    37,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '7630',
    'Revenus des autres créances',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'recette',
    'fonctionnement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '763' LIMIT 1),
    3,
    38,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '7641',
    'Revenus des obligations et bons à court terme',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'recette',
    'fonctionnement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '764' LIMIT 1),
    3,
    39,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '7642',
    'Revenus des prêts à court terme',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'recette',
    'fonctionnement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '764' LIMIT 1),
    3,
    40,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '7680',
    'Autres produits financiers',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'recette',
    'fonctionnement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '768' LIMIT 1),
    3,
    41,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '7711',
    'Redevances de collecte et de traitement des ordures ménagères - ROM',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'recette',
    'fonctionnement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '771' LIMIT 1),
    3,
    42,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '7712',
    'Redevances de rejet des eaux usées - RREU',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'recette',
    'fonctionnement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '771' LIMIT 1),
    3,
    43,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '7713',
    'Redevance et frais d''administration minière',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'recette',
    'fonctionnement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '771' LIMIT 1),
    3,
    44,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '7714',
    'Redevances sur autorisations administratives',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'recette',
    'fonctionnement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '771' LIMIT 1),
    3,
    45,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '7715',
    'Redevance fixe d''abonnement pour branchement',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'recette',
    'fonctionnement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '771' LIMIT 1),
    3,
    46,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '7716',
    'Redevance versées par les fermiers et concessionnaires',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'recette',
    'fonctionnement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '771' LIMIT 1),
    3,
    47,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '7717',
    'Produits des ristournes',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'recette',
    'fonctionnement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '771' LIMIT 1),
    3,
    48,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '7718',
    'Autres redevances locales',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'recette',
    'fonctionnement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '771' LIMIT 1),
    3,
    49,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '7721',
    'Prestation de service',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'recette',
    'fonctionnement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '772' LIMIT 1),
    3,
    50,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '7722',
    'Produits finis',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'recette',
    'fonctionnement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '772' LIMIT 1),
    3,
    51,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '7723',
    'Produits intermédiaires',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'recette',
    'fonctionnement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '772' LIMIT 1),
    3,
    52,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '7724',
    'Produits résiduels',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'recette',
    'fonctionnement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '772' LIMIT 1),
    3,
    53,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '7725',
    'Travaux',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'recette',
    'fonctionnement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '772' LIMIT 1),
    3,
    54,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '7726',
    'Marchandises',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'recette',
    'fonctionnement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '772' LIMIT 1),
    3,
    55,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '7727',
    'revenus des domaines',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'recette',
    'fonctionnement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '772' LIMIT 1),
    3,
    56,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '7728',
    'Autres produits des activités des services',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'recette',
    'fonctionnement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '772' LIMIT 1),
    3,
    57,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '7731',
    'Commissions et courtages',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'recette',
    'fonctionnement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '773' LIMIT 1),
    3,
    58,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '7732',
    'Locations diverses',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'recette',
    'fonctionnement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '773' LIMIT 1),
    3,
    59,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '7733',
    'Confiscations',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'recette',
    'fonctionnement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '773' LIMIT 1),
    3,
    60,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '7734',
    'Droit de fourrières',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'recette',
    'fonctionnement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '773' LIMIT 1),
    3,
    61,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '7735',
    'Droit de stationnement',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'recette',
    'fonctionnement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '773' LIMIT 1),
    3,
    62,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '7738',
    'Autres',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'recette',
    'fonctionnement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '773' LIMIT 1),
    3,
    63,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '7741',
    'Immobilisation incorporelle',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'recette',
    'fonctionnement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '774' LIMIT 1),
    3,
    64,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '7742',
    'Immobilisations corporelle',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'recette',
    'fonctionnement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '774' LIMIT 1),
    3,
    65,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '1011',
    'Contreparties d''intégrations pratimoniales',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'recette',
    'investissement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '101' LIMIT 1),
    3,
    66,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '1012',
    'Dotations de l’État',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'recette',
    'investissement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '101' LIMIT 1),
    3,
    67,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '1013',
    'Dotations : autres collectivités ou organismes publics',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'recette',
    'investissement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '101' LIMIT 1),
    3,
    68,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '1014',
    'Fonds de travaux électricité',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'recette',
    'investissement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '101' LIMIT 1),
    3,
    69,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '1015',
    'Fonds de travaux réseau eau',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'recette',
    'investissement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '101' LIMIT 1),
    3,
    70,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '1016',
    'Dons et legs en capital',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'recette',
    'investissement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '101' LIMIT 1),
    3,
    71,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '1017',
    'Mises à disposition',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'recette',
    'investissement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '101' LIMIT 1),
    3,
    72,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '1018',
    'Autres',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'recette',
    'investissement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '101' LIMIT 1),
    3,
    73,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '1061',
    'Réserves des budgets annexes',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'recette',
    'investissement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '106' LIMIT 1),
    3,
    74,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '1064',
    'Excédent de fonctionnement capitalisé',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'recette',
    'investissement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '106' LIMIT 1),
    3,
    75,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '1068',
    'Autres réserves',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'recette',
    'investissement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '106' LIMIT 1),
    3,
    76,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '1311',
    'Subventions reçues de l''Etat',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'recette',
    'investissement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '131' LIMIT 1),
    3,
    77,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '1312',
    'Subventions reçues des Collectivités Territoriales Décentralisées',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'recette',
    'investissement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '131' LIMIT 1),
    3,
    78,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '1313',
    'Subventions reçues des Organismes nationaux et internationaux',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'recette',
    'investissement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '131' LIMIT 1),
    3,
    79,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '1314',
    'Aides bilatérales',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'recette',
    'investissement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '131' LIMIT 1),
    3,
    80,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '1315',
    'Aides multilatérales',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'recette',
    'investissement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '131' LIMIT 1),
    3,
    81,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '1318',
    'Autres subventions d''équipement reçues',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'recette',
    'investissement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '131' LIMIT 1),
    3,
    82,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '1390',
    'Subvention d''investissement transférée au compte de résultat',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'recette',
    'investissement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '139' LIMIT 1),
    3,
    83,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '1411',
    'Frais de développement, de recherche et d''études',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'recette',
    'investissement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '141' LIMIT 1),
    3,
    84,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '1415',
    'Concessions et droits similaires, brevets, licence, marques',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'recette',
    'investissement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '141' LIMIT 1),
    3,
    85,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '1418',
    'Autres immobilisations incorporelles',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'recette',
    'investissement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '141' LIMIT 1),
    3,
    86,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '1421',
    'Terrains',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'recette',
    'investissement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '142' LIMIT 1),
    3,
    87,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '1423',
    'Bâtiments',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'recette',
    'investissement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '142' LIMIT 1),
    3,
    88,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '1424',
    'Voies',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'recette',
    'investissement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '142' LIMIT 1),
    3,
    89,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '1425',
    'Réseaux',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'recette',
    'investissement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '142' LIMIT 1),
    3,
    90,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '1426',
    'Matériel et ouillage',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'recette',
    'investissement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '142' LIMIT 1),
    3,
    91,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '1427',
    'Matériels de transport',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'recette',
    'investissement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '142' LIMIT 1),
    3,
    92,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '1428',
    'Autres immobilisations corporelles',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'recette',
    'investissement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '142' LIMIT 1),
    3,
    93,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '1471',
    'Ventes de titres de participations',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'recette',
    'investissement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '147' LIMIT 1),
    3,
    94,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '1472',
    'Remboursements de prêts accordés à long terme et moyen terme',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'recette',
    'investissement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '147' LIMIT 1),
    3,
    95,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '1473',
    'Remboursements de prêts accordés à court terme',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'recette',
    'investissement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '147' LIMIT 1),
    3,
    96,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '1474',
    'Remboursements d''avances accordées',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'recette',
    'investissement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '147' LIMIT 1),
    3,
    97,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '1478',
    'Autres immobilisations financières',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'recette',
    'investissement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '147' LIMIT 1),
    3,
    98,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '1611',
    'Emprunts à long et moyen terme : part à plus d''un an',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'recette',
    'investissement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '161' LIMIT 1),
    3,
    99,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '1612',
    'Emprunts à long et moyen terme : part à moins d''un an',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'recette',
    'investissement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '161' LIMIT 1),
    3,
    100,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '1621',
    'Emprunts à long et moyen terme : part à plus d''un an',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'recette',
    'investissement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '162' LIMIT 1),
    3,
    101,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '1622',
    'Emprunts à long et moyen terme : part à moins d''un an',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'recette',
    'investissement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '162' LIMIT 1),
    3,
    102,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '1650',
    'Dépôts et cautionnement reçus',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'recette',
    'investissement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '165' LIMIT 1),
    3,
    103,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '1670',
    'Dettes sur contrat de location-financement',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'recette',
    'investissement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '167' LIMIT 1),
    3,
    104,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '1680',
    'Autres emprunts et dettes assimilés',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'recette',
    'investissement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '168' LIMIT 1),
    3,
    105,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '1688',
    'Intérêts courus sur emprunts et dettes assimilés',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'recette',
    'investissement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '168' LIMIT 1),
    3,
    106,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '6011',
    'Personnel permanent',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'depense',
    'fonctionnement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '601' LIMIT 1),
    3,
    118,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '6012',
    'Personnel non permanent',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'depense',
    'fonctionnement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '601' LIMIT 1),
    3,
    119,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '6021',
    'Personnel permanent',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'depense',
    'fonctionnement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '602' LIMIT 1),
    3,
    120,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '6022',
    'Personnel non permanent',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'depense',
    'fonctionnement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '602' LIMIT 1),
    3,
    121,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '6031',
    'Personnel permanent',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'depense',
    'fonctionnement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '603' LIMIT 1),
    3,
    122,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '6032',
    'Personnel non permanent',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'depense',
    'fonctionnement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '603' LIMIT 1),
    3,
    123,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '6041',
    'Personnel permanent',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'depense',
    'fonctionnement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '604' LIMIT 1),
    3,
    124,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '6042',
    'Personnel non permanent',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'depense',
    'fonctionnement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '604' LIMIT 1),
    3,
    125,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '6061',
    'Cotisations à la CNAPS',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'depense',
    'fonctionnement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '606' LIMIT 1),
    3,
    126,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '6062',
    'Cotisations caisse de retraites civiles et militaires',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'depense',
    'fonctionnement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '606' LIMIT 1),
    3,
    127,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '6063',
    'CPR',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'depense',
    'fonctionnement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '606' LIMIT 1),
    3,
    128,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '6064',
    'Cotisations aux OSIE',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'depense',
    'fonctionnement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '606' LIMIT 1),
    3,
    129,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '6068',
    'Autres charges sociales patronales',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'depense',
    'fonctionnement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '606' LIMIT 1),
    3,
    130,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '6111',
    'Fournitures et articles de bureau',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'depense',
    'fonctionnement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '611' LIMIT 1),
    3,
    131,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '6112',
    'Imprimés, cachets et docuements administratifs',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'depense',
    'fonctionnement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '611' LIMIT 1),
    3,
    132,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '6113',
    'Consomptibles informatiques',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'depense',
    'fonctionnement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '611' LIMIT 1),
    3,
    133,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '6114',
    'Produits, petits matériels et menues dépenses d''entretien',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'depense',
    'fonctionnement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '611' LIMIT 1),
    3,
    134,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '6115',
    'Petits outillages et fournitures d''atelier',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'depense',
    'fonctionnement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '611' LIMIT 1),
    3,
    135,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '6116',
    'Instruments spécialisés',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'depense',
    'fonctionnement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '611' LIMIT 1),
    3,
    136,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '6117',
    'Habillement',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'depense',
    'fonctionnement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '611' LIMIT 1),
    3,
    137,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '6121',
    'Fornitures scolaires',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'depense',
    'fonctionnement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '612' LIMIT 1),
    3,
    138,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '6122',
    'Consommables médicaux',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'depense',
    'fonctionnement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '612' LIMIT 1),
    3,
    139,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '6123',
    'Produits pahrmaceutiques',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'depense',
    'fonctionnement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '612' LIMIT 1),
    3,
    140,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '6124',
    'Produits vétérianaires',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'depense',
    'fonctionnement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '612' LIMIT 1),
    3,
    141,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '6125',
    'Produits alimentaires',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'depense',
    'fonctionnement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '612' LIMIT 1),
    3,
    142,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '6126',
    'Intrants agricoles',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'depense',
    'fonctionnement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '612' LIMIT 1),
    3,
    143,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '6127',
    'Fournitures sportives',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'depense',
    'fonctionnement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '612' LIMIT 1),
    3,
    144,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '6128',
    'Fournitures ménagères',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'depense',
    'fonctionnement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '612' LIMIT 1),
    3,
    145,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '6131',
    'Carburants et Lubrifiants',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'depense',
    'fonctionnement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '613' LIMIT 1),
    3,
    146,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '6132',
    'Gaz',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'depense',
    'fonctionnement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '613' LIMIT 1),
    3,
    147,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '6138',
    'Autres combustibles',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'depense',
    'fonctionnement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '613' LIMIT 1),
    3,
    148,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '6161',
    'Variation des stocks de biens de fonctionnement général',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'depense',
    'fonctionnement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '616' LIMIT 1),
    3,
    149,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '6162',
    'Variation des stoccks de biens à usage spécifique',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'depense',
    'fonctionnement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '616' LIMIT 1),
    3,
    150,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '6163',
    'Variation des stocks de carburants, Lubrifiants et combustibles',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'depense',
    'fonctionnement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '616' LIMIT 1),
    3,
    151,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '6168',
    'Variation des staock d''autres achats',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'depense',
    'fonctionnement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '616' LIMIT 1),
    3,
    152,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '6181',
    'Achats de matières premières',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'depense',
    'fonctionnement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '618' LIMIT 1),
    3,
    153,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '6182',
    'Achats de marchandises destinées à être revendues',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'depense',
    'fonctionnement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '618' LIMIT 1),
    3,
    154,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '6183',
    'Emballages',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'depense',
    'fonctionnement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '618' LIMIT 1),
    3,
    155,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '6211',
    'Entretien de bâtiments',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'depense',
    'fonctionnement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '621' LIMIT 1),
    3,
    156,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '6212',
    'Entretien des autres infrastructures',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'depense',
    'fonctionnement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '621' LIMIT 1),
    3,
    157,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '6213',
    'Entretien de véhicules',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'depense',
    'fonctionnement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '621' LIMIT 1),
    3,
    158,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '6214',
    'Entretien de matériels techniques',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'depense',
    'fonctionnement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '621' LIMIT 1),
    3,
    159,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '6215',
    'Entretien et réparation des matériels et mobiliers de bureau',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'depense',
    'fonctionnement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '621' LIMIT 1),
    3,
    160,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '6216',
    'Entretien et réparation des matériels et mobiliers de logement',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'depense',
    'fonctionnement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '621' LIMIT 1),
    3,
    161,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '6217',
    'Entretien et réparation des matériels et mobiliers scolaires',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'depense',
    'fonctionnement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '621' LIMIT 1),
    3,
    162,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '6218',
    'Maintenance du matériel informatique',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'depense',
    'fonctionnement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '621' LIMIT 1),
    3,
    163,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '6221',
    'Fêtes et cérémonies officielles',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'depense',
    'fonctionnement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '622' LIMIT 1),
    3,
    164,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '6222',
    'Charges de représentation : visites officielles',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'depense',
    'fonctionnement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '622' LIMIT 1),
    3,
    165,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '6223',
    'Docuementation et abonnement',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'depense',
    'fonctionnement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '622' LIMIT 1),
    3,
    166,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '6224',
    'Impression, reliures, insertions, publicité et promotion',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'depense',
    'fonctionnement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '622' LIMIT 1),
    3,
    167,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '6225',
    'Frais de Colloques, séminaires, conférences',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'depense',
    'fonctionnement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '622' LIMIT 1),
    3,
    168,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '6226',
    'Foires, exposition',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'depense',
    'fonctionnement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '622' LIMIT 1),
    3,
    169,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '6231',
    'Frais de déplacement intérieur',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'depense',
    'fonctionnement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '623' LIMIT 1),
    3,
    170,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '6232',
    'Frais de déplacement extérieur',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'depense',
    'fonctionnement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '623' LIMIT 1),
    3,
    171,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '6233',
    'Locations de voitures',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'depense',
    'fonctionnement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '623' LIMIT 1),
    3,
    172,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '6234',
    'Transport administratif',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'depense',
    'fonctionnement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '623' LIMIT 1),
    3,
    173,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '6235',
    'Transport de bien',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'depense',
    'fonctionnement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '623' LIMIT 1),
    3,
    174,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '6241',
    'Indemnité de mission intérieure',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'depense',
    'fonctionnement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '624' LIMIT 1),
    3,
    175,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '6242',
    'Indemnité de mission extérieure',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'depense',
    'fonctionnement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '624' LIMIT 1),
    3,
    176,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '6243',
    'Viatique',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'depense',
    'fonctionnement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '624' LIMIT 1),
    3,
    177,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '6250',
    'Eau et électricité',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'depense',
    'fonctionnement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '625' LIMIT 1),
    3,
    178,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '6261',
    'Frais postaux',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'depense',
    'fonctionnement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '626' LIMIT 1),
    3,
    179,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '6262',
    'Redevances téléphoniques',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'depense',
    'fonctionnement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '626' LIMIT 1),
    3,
    180,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '6263',
    'Redevances téléphoniques mobiles',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'depense',
    'fonctionnement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '626' LIMIT 1),
    3,
    181,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '6264',
    'Internet',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'depense',
    'fonctionnement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '626' LIMIT 1),
    3,
    182,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '6265',
    'Télex',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'depense',
    'fonctionnement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '626' LIMIT 1),
    3,
    183,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '6268',
    'Autres',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'depense',
    'fonctionnement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '626' LIMIT 1),
    3,
    184,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '6271',
    'Location d''immeuble de bureau',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'depense',
    'fonctionnement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '627' LIMIT 1),
    3,
    185,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '6272',
    'Location d''immeuble de logement',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'depense',
    'fonctionnement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '627' LIMIT 1),
    3,
    186,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '6273',
    'Location d''immeuble de bureau-loggement',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'depense',
    'fonctionnement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '627' LIMIT 1),
    3,
    187,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '6274',
    'Location de terrain',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'depense',
    'fonctionnement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '627' LIMIT 1),
    3,
    188,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '6275',
    'Location de matériels',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'depense',
    'fonctionnement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '627' LIMIT 1),
    3,
    189,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '6278',
    'Autres charges locatives',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'depense',
    'fonctionnement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '627' LIMIT 1),
    3,
    190,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '6281',
    'Rémunérations d''intermédiaires et honoraires',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'depense',
    'fonctionnement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '628' LIMIT 1),
    3,
    191,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '6282',
    'Frais d''études et de recherche',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'depense',
    'fonctionnement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '628' LIMIT 1),
    3,
    192,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '6283',
    'Frais de stage et de formation',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'depense',
    'fonctionnement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '628' LIMIT 1),
    3,
    193,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '6284',
    'Assurances',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'depense',
    'fonctionnement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '628' LIMIT 1),
    3,
    194,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '6285',
    'Services banciares et assimilés',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'depense',
    'fonctionnement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '628' LIMIT 1),
    3,
    195,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '6286',
    'Cotisations et divers',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'depense',
    'fonctionnement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '628' LIMIT 1),
    3,
    196,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '6287',
    'Personnels extérieurs au service',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'depense',
    'fonctionnement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '628' LIMIT 1),
    3,
    197,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '6288',
    'Contrat de prestation de service',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'depense',
    'fonctionnement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '628' LIMIT 1),
    3,
    198,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '6310',
    'Intervention sociale',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'depense',
    'fonctionnement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '631' LIMIT 1),
    3,
    199,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '6320',
    'Intervention économique',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'depense',
    'fonctionnement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '632' LIMIT 1),
    3,
    200,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '6330',
    'Intervention structurelle',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'depense',
    'fonctionnement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '633' LIMIT 1),
    3,
    201,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '6380',
    'Dépenses d''intervention diverses et imprévues',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'depense',
    'fonctionnement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '638' LIMIT 1),
    3,
    202,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '6418',
    'Autres taxes et impôts directs',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'depense',
    'fonctionnement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '641' LIMIT 1),
    3,
    203,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '6420',
    'Taxes et impôts indirects',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'depense',
    'fonctionnement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '642' LIMIT 1),
    3,
    204,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '6430',
    'Impôts, taxes et droits d''enregistrement',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'depense',
    'fonctionnement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '643' LIMIT 1),
    3,
    205,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '6440',
    'Droits à l''importation',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'depense',
    'fonctionnement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '644' LIMIT 1),
    3,
    206,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '6480',
    'Impôts, taxes et droits divers',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'depense',
    'fonctionnement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '648' LIMIT 1),
    3,
    207,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '6510',
    'Transferts aux collectivités publiques',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'depense',
    'fonctionnement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '651' LIMIT 1),
    3,
    208,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '6531',
    'Bourses à Madagascar',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'depense',
    'fonctionnement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '653' LIMIT 1),
    3,
    209,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '6532',
    'Bourses à l''extérieur',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'depense',
    'fonctionnement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '653' LIMIT 1),
    3,
    210,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '6533',
    'Présalaire, Prêt d''honneur',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'depense',
    'fonctionnement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '653' LIMIT 1),
    3,
    211,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '6534',
    'Prix et récompenses officiels',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'depense',
    'fonctionnement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '653' LIMIT 1),
    3,
    212,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '6540',
    'Contributions obligatoires',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'depense',
    'fonctionnement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '654' LIMIT 1),
    3,
    213,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '6550',
    'Transferts aux organismes publics',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'depense',
    'fonctionnement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '655' LIMIT 1),
    3,
    214,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '6561',
    'Hospitalisation, traitement et soins',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'depense',
    'fonctionnement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '656' LIMIT 1),
    3,
    215,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '6562',
    'Secours',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'depense',
    'fonctionnement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '656' LIMIT 1),
    3,
    216,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '6563',
    'Indemnisation',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'depense',
    'fonctionnement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '656' LIMIT 1),
    3,
    217,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '6564',
    'Régularisation des droits acquis',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'depense',
    'fonctionnement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '656' LIMIT 1),
    3,
    218,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '6565',
    'Subvention au secteur privé',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'depense',
    'fonctionnement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '656' LIMIT 1),
    3,
    219,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '6611',
    'Intérêts des emprunts',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'depense',
    'fonctionnement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '661' LIMIT 1),
    3,
    220,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '6618',
    'Autres charges d''intérêt',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'depense',
    'fonctionnement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '661' LIMIT 1),
    3,
    221,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '6621',
    'Intérêts banciares et opérations de financements à court terme',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'depense',
    'fonctionnement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '662' LIMIT 1),
    3,
    222,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '6622',
    'Intérêts des opérations de financements à court terme',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'depense',
    'fonctionnement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '662' LIMIT 1),
    3,
    223,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '6631',
    'Intérêts des comptes courants',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'depense',
    'fonctionnement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '663' LIMIT 1),
    3,
    224,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '6632',
    'Intérêts des dépôts créditerus',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'depense',
    'fonctionnement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '663' LIMIT 1),
    3,
    225,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '6660',
    'Pertes de changes',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'depense',
    'fonctionnement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '666' LIMIT 1),
    3,
    226,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '6681',
    'Intérêts des autres dettes',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'depense',
    'fonctionnement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '668' LIMIT 1),
    3,
    227,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '6688',
    'Autres charges financières',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'depense',
    'fonctionnement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '668' LIMIT 1),
    3,
    228,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '6711',
    'Remises gracieuses',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'depense',
    'fonctionnement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '671' LIMIT 1),
    3,
    229,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '6712',
    'Dégrèvement sur titres émis',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'depense',
    'fonctionnement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '671' LIMIT 1),
    3,
    230,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '6713',
    'Pertes sur créances irrecouvrables',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'depense',
    'fonctionnement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '671' LIMIT 1),
    3,
    231,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '6714',
    'Perte sur dons extérieurs',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'depense',
    'fonctionnement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '671' LIMIT 1),
    3,
    232,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '6718',
    'Autres',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'depense',
    'fonctionnement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '671' LIMIT 1),
    3,
    233,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '6720',
    'Reversement sur trop perçu',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'depense',
    'fonctionnement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '672' LIMIT 1),
    3,
    234,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '6730',
    'Déficits budgets annexes',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'depense',
    'fonctionnement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '673' LIMIT 1),
    3,
    235,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '6741',
    'Frais de justice',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'depense',
    'fonctionnement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '674' LIMIT 1),
    3,
    236,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '6742',
    'Frais de contentieux',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'depense',
    'fonctionnement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '674' LIMIT 1),
    3,
    237,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '6751',
    'Intérêts moratoires, Amendes et Pénalités',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'depense',
    'fonctionnement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '675' LIMIT 1),
    3,
    238,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '6752',
    'Amendes',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'depense',
    'fonctionnement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '675' LIMIT 1),
    3,
    239,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '6753',
    'Pénalités',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'depense',
    'fonctionnement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '675' LIMIT 1),
    3,
    240,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '6781',
    'Moins-values sur cessions d''immobilisations',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'depense',
    'fonctionnement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '678' LIMIT 1),
    3,
    241,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '6782',
    'Quotes-part de résultat sur opérations faites en commun',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'depense',
    'fonctionnement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '678' LIMIT 1),
    3,
    242,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '6788',
    'Autres',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'depense',
    'fonctionnement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '678' LIMIT 1),
    3,
    243,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '2011',
    'Formation',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'depense',
    'investissement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '201' LIMIT 1),
    3,
    252,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '2012',
    'Animation et encadrement',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'depense',
    'investissement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '201' LIMIT 1),
    3,
    253,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '2013',
    'Assistance technique',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'depense',
    'investissement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '201' LIMIT 1),
    3,
    254,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '2014',
    'Logiciels informatiques et assimilés',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'depense',
    'investissement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '201' LIMIT 1),
    3,
    255,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '2015',
    'Etudes et recherches',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'depense',
    'investissement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '201' LIMIT 1),
    3,
    256,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '2016',
    'Suivi - Contrôle - Evaluations',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'depense',
    'investissement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '201' LIMIT 1),
    3,
    257,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '2017',
    'Frais de pré-exploitation',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'depense',
    'investissement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '201' LIMIT 1),
    3,
    258,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '2018',
    'Autres',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'depense',
    'investissement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '201' LIMIT 1),
    3,
    259,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '2051',
    'Concessions et droits similaires',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'depense',
    'investissement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '205' LIMIT 1),
    3,
    260,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '2052',
    'Brevets, licences, marques',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'depense',
    'investissement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '205' LIMIT 1),
    3,
    261,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '2080',
    'Autres immoblisations incorporelles',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'depense',
    'investissement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '208' LIMIT 1),
    3,
    262,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '2111',
    'Terrains nus',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'depense',
    'investissement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '211' LIMIT 1),
    3,
    263,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '2112',
    'Terrains bâtis',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'depense',
    'investissement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '211' LIMIT 1),
    3,
    264,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '2113',
    'Terrains de gisement',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'depense',
    'investissement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '211' LIMIT 1),
    3,
    265,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '2114',
    'Terrains de chantiers',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'depense',
    'investissement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '211' LIMIT 1),
    3,
    266,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '2115',
    'Terrains de voiries',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'depense',
    'investissement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '211' LIMIT 1),
    3,
    267,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '2116',
    'Cimetières',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'depense',
    'investissement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '211' LIMIT 1),
    3,
    268,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '2117',
    'Bois et forêts',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'depense',
    'investissement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '211' LIMIT 1),
    3,
    269,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '2118',
    'Autres',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'depense',
    'investissement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '211' LIMIT 1),
    3,
    270,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '2121',
    'Aménagement de terrain',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'depense',
    'investissement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '212' LIMIT 1),
    3,
    271,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '2122',
    'Aménagement des aérodromes',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'depense',
    'investissement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '212' LIMIT 1),
    3,
    272,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '2123',
    'Aménagement des ports',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'depense',
    'investissement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '212' LIMIT 1),
    3,
    273,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '2124',
    'Travaux d''irrigation',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'depense',
    'investissement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '212' LIMIT 1),
    3,
    274,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '2125',
    'Travaus d''urbanisme',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'depense',
    'investissement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '212' LIMIT 1),
    3,
    275,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '2128',
    'Autres aménagements',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'depense',
    'investissement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '212' LIMIT 1),
    3,
    276,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '2131',
    'Batiments administratifs',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'depense',
    'investissement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '213' LIMIT 1),
    3,
    277,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '2132',
    'Bâtiments scolaires',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'depense',
    'investissement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '213' LIMIT 1),
    3,
    278,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '2133',
    'Batiments de cnetres de soins de santé',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'depense',
    'investissement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '213' LIMIT 1),
    3,
    279,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '2134',
    'Autres bâtiments techniques',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'depense',
    'investissement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '213' LIMIT 1),
    3,
    280,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '2137',
    'Installations, agencemetns et aménagements - Bâtiments',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'depense',
    'investissement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '213' LIMIT 1),
    3,
    281,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '2138',
    'Autres constructions ou réhabilitations - Bâtiments',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'depense',
    'investissement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '213' LIMIT 1),
    3,
    282,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '2141',
    'Routes',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'depense',
    'investissement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '214' LIMIT 1),
    3,
    283,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '2142',
    'Voies ferrées',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'depense',
    'investissement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '214' LIMIT 1),
    3,
    284,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '2143',
    'Voies d''eau',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'depense',
    'investissement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '214' LIMIT 1),
    3,
    285,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '2144',
    'Pistes d''aérodrome',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'depense',
    'investissement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '214' LIMIT 1),
    3,
    286,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '2147',
    'Installations, agencements et aménagements - Voies',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'depense',
    'investissement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '214' LIMIT 1),
    3,
    287,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '2148',
    'Autres constructions ou réhabilitations - Voies',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'depense',
    'investissement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '214' LIMIT 1),
    3,
    288,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '2151',
    'Réseau d''aduction d''eau',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'depense',
    'investissement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '215' LIMIT 1),
    3,
    289,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '2152',
    'Réseau d''assainissement',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'depense',
    'investissement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '215' LIMIT 1),
    3,
    290,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '2153',
    'Réseau téléphonique',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'depense',
    'investissement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '215' LIMIT 1),
    3,
    291,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '2154',
    'Réseau de communication',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'depense',
    'investissement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '215' LIMIT 1),
    3,
    292,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '2155',
    'Réseau d''électricité',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'depense',
    'investissement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '215' LIMIT 1),
    3,
    293,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '2156',
    'Réseau d''irrigation',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'depense',
    'investissement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '215' LIMIT 1),
    3,
    294,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '2157',
    'Installations, agencements et aménagements - Réseaux',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'depense',
    'investissement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '215' LIMIT 1),
    3,
    295,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '2158',
    'Autres constructions ou réhabilitations - Réseaux',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'depense',
    'investissement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '215' LIMIT 1),
    3,
    296,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '2161',
    'Matériels techniques',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'depense',
    'investissement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '216' LIMIT 1),
    3,
    297,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '2162',
    'Matériels agricoles',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'depense',
    'investissement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '216' LIMIT 1),
    3,
    298,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '2163',
    'Matériels informatiques',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'depense',
    'investissement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '216' LIMIT 1),
    3,
    299,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '2164',
    'Matériels et mobiliers de bureau',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'depense',
    'investissement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '216' LIMIT 1),
    3,
    300,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '2165',
    'Matériels et mobiliers de logement',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'depense',
    'investissement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '216' LIMIT 1),
    3,
    301,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '2166',
    'Matériels et mobiliers scolaires',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'depense',
    'investissement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '216' LIMIT 1),
    3,
    302,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '2167',
    'Outillages',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'depense',
    'investissement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '216' LIMIT 1),
    3,
    303,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '2168',
    'Autres matériels et outillages',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'depense',
    'investissement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '216' LIMIT 1),
    3,
    304,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '2171',
    'Renouvellement des vehicules du parc administratif',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'depense',
    'investissement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '217' LIMIT 1),
    3,
    305,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '2172',
    'Matériel automobile',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'depense',
    'investissement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '217' LIMIT 1),
    3,
    306,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '2173',
    'Matériel fluvial',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'depense',
    'investissement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '217' LIMIT 1),
    3,
    307,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '2174',
    'Matériel ferroviaire',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'depense',
    'investissement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '217' LIMIT 1),
    3,
    308,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '2175',
    'Matériel naval',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'depense',
    'investissement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '217' LIMIT 1),
    3,
    309,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '2176',
    'Matériel aérien',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'depense',
    'investissement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '217' LIMIT 1),
    3,
    310,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '2178',
    'Autres moyens de locomotion',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'depense',
    'investissement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '217' LIMIT 1),
    3,
    311,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '2181',
    'Cheptel',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'depense',
    'investissement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '218' LIMIT 1),
    3,
    312,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '2182',
    'Emballages récupérables',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'depense',
    'investissement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '218' LIMIT 1),
    3,
    313,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '2183',
    'Installations complexes spécialisées',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'depense',
    'investissement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '218' LIMIT 1),
    3,
    314,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

INSERT INTO rubriques_budgetaires (
    code, intitule, categorie_id, type, section,
    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description
) VALUES (
    '2188',
    'Autres immobilisations corporelles',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    'depense',
    'investissement',
    (SELECT id FROM rubriques_budgetaires WHERE code = '218' LIMIT 1),
    3,
    315,
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
);

-- Réactiver les triggers
ALTER TABLE rubriques_budgetaires ENABLE TRIGGER USER;
