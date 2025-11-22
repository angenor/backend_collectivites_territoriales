-- ============================================================================
-- DONNÉES INITIALES POUR LA PLATEFORME DE SUIVI DES REVENUS MINIERS
-- ============================================================================

-- ============================================================================
-- RÔLES PAR DÉFAUT
-- ============================================================================

INSERT INTO roles (id, code, nom, description, permissions, actif) VALUES
(
    uuid_generate_v4(),
    'ADMIN',
    'Administrateur',
    'Administrateur système avec tous les droits',
    '["all"]'::jsonb,
    TRUE
),
(
    uuid_generate_v4(),
    'EDITEUR',
    'Éditeur',
    'Éditeur de contenu avec droits limités',
    '["read", "create", "update"]'::jsonb,
    TRUE
),
(
    uuid_generate_v4(),
    'LECTEUR',
    'Lecteur',
    'Utilisateur en lecture seule',
    '["read"]'::jsonb,
    TRUE
);

-- ============================================================================
-- TYPES DE DOCUMENTS
-- ============================================================================

INSERT INTO types_documents (id, code, nom, description, extensions_autorisees, taille_max_mo, actif) VALUES
(
    uuid_generate_v4(),
    'RAPPORT_ANNUEL',
    'Rapport Annuel',
    'Rapport annuel de compte administratif',
    ARRAY['.pdf', '.doc', '.docx'],
    20,
    TRUE
),
(
    uuid_generate_v4(),
    'FACTURE',
    'Facture',
    'Facture ou document comptable',
    ARRAY['.pdf', '.jpg', '.png'],
    10,
    TRUE
),
(
    uuid_generate_v4(),
    'TABLEAU_COMPTE',
    'Tableau de Compte',
    'Tableau de compte administratif',
    ARRAY['.xlsx', '.xls', '.csv'],
    15,
    TRUE
),
(
    uuid_generate_v4(),
    'JUSTIFICATIF',
    'Justificatif',
    'Document justificatif divers',
    ARRAY['.pdf', '.jpg', '.png', '.doc', '.docx'],
    10,
    TRUE
);

-- ============================================================================
-- TYPES DE MINERAIS (EXEMPLES)
-- ============================================================================

INSERT INTO types_minerais (id, code, nom, description, actif) VALUES
(
    uuid_generate_v4(),
    'NICKEL',
    'Nickel',
    'Minerai de nickel - minerai critique',
    TRUE
),
(
    uuid_generate_v4(),
    'COBALT',
    'Cobalt',
    'Minerai de cobalt - minerai critique',
    TRUE
),
(
    uuid_generate_v4(),
    'ILMENITE',
    'Ilménite',
    'Minerai d''ilménite (source de titane)',
    TRUE
),
(
    uuid_generate_v4(),
    'GRAPHITE',
    'Graphite',
    'Graphite naturel',
    TRUE
),
(
    uuid_generate_v4(),
    'OR',
    'Or',
    'Or alluvionnaire et filonien',
    TRUE
),
(
    uuid_generate_v4(),
    'PIERRES_PRECIEUSES',
    'Pierres Précieuses',
    'Pierres précieuses (saphir, émeraude, etc.)',
    TRUE
);

-- ============================================================================
-- CATÉGORIES DE RUBRIQUES
-- ============================================================================

INSERT INTO categories_rubriques (id, code, nom, description, ordre, actif) VALUES
(
    uuid_generate_v4(),
    'RECETTES',
    'Recettes',
    'Recettes de fonctionnement et d''investissement',
    1,
    TRUE
),
(
    uuid_generate_v4(),
    'DEPENSES',
    'Dépenses',
    'Dépenses de fonctionnement et d''investissement',
    2,
    TRUE
),
(
    uuid_generate_v4(),
    'SOLDES',
    'Soldes',
    'Soldes et résultats comptables',
    3,
    TRUE
);

-- ============================================================================
-- RUBRIQUES DE BASE (STRUCTURE TYPIQUE D'UN COMPTE ADMINISTRATIF)
-- ============================================================================

-- Rubriques de recettes
INSERT INTO rubriques (id, code, nom, categorie_id, parent_id, niveau, ordre, type, est_calculee, afficher_total, actif) VALUES
-- Niveau 1: Recettes totales
(
    uuid_generate_v4(),
    'R000',
    'RECETTES TOTALES',
    (SELECT id FROM categories_rubriques WHERE code = 'RECETTES'),
    NULL,
    1,
    1,
    'recette',
    TRUE,
    TRUE,
    TRUE
);

-- Sous-rubriques de recettes
INSERT INTO rubriques (id, code, nom, categorie_id, parent_id, niveau, ordre, type, est_calculee, afficher_total, actif) VALUES
(
    uuid_generate_v4(),
    'R100',
    'Recettes de fonctionnement',
    (SELECT id FROM categories_rubriques WHERE code = 'RECETTES'),
    (SELECT id FROM rubriques WHERE code = 'R000'),
    2,
    1,
    'recette',
    FALSE,
    TRUE,
    TRUE
),
(
    uuid_generate_v4(),
    'R110',
    'Ristournes minières',
    (SELECT id FROM categories_rubriques WHERE code = 'RECETTES'),
    (SELECT id FROM rubriques WHERE code = 'R100'),
    3,
    1,
    'recette',
    FALSE,
    TRUE,
    TRUE
),
(
    uuid_generate_v4(),
    'R120',
    'Redevances minières',
    (SELECT id FROM categories_rubriques WHERE code = 'RECETTES'),
    (SELECT id FROM rubriques WHERE code = 'R100'),
    3,
    2,
    'recette',
    FALSE,
    TRUE,
    TRUE
),
(
    uuid_generate_v4(),
    'R130',
    'Taxes et impôts locaux',
    (SELECT id FROM categories_rubriques WHERE code = 'RECETTES'),
    (SELECT id FROM rubriques WHERE code = 'R100'),
    3,
    3,
    'recette',
    FALSE,
    TRUE,
    TRUE
),
(
    uuid_generate_v4(),
    'R140',
    'Subventions de l''État',
    (SELECT id FROM categories_rubriques WHERE code = 'RECETTES'),
    (SELECT id FROM rubriques WHERE code = 'R100'),
    3,
    4,
    'recette',
    FALSE,
    TRUE,
    TRUE
),
(
    uuid_generate_v4(),
    'R200',
    'Recettes d''investissement',
    (SELECT id FROM categories_rubriques WHERE code = 'RECETTES'),
    (SELECT id FROM rubriques WHERE code = 'R000'),
    2,
    2,
    'recette',
    FALSE,
    TRUE,
    TRUE
),
(
    uuid_generate_v4(),
    'R210',
    'Emprunts',
    (SELECT id FROM categories_rubriques WHERE code = 'RECETTES'),
    (SELECT id FROM rubriques WHERE code = 'R200'),
    3,
    1,
    'recette',
    FALSE,
    TRUE,
    TRUE
),
(
    uuid_generate_v4(),
    'R220',
    'Subventions d''équipement',
    (SELECT id FROM categories_rubriques WHERE code = 'RECETTES'),
    (SELECT id FROM rubriques WHERE code = 'R200'),
    3,
    2,
    'recette',
    FALSE,
    TRUE,
    TRUE
);

-- Rubriques de dépenses
INSERT INTO rubriques (id, code, nom, categorie_id, parent_id, niveau, ordre, type, est_calculee, afficher_total, actif) VALUES
-- Niveau 1: Dépenses totales
(
    uuid_generate_v4(),
    'D000',
    'DÉPENSES TOTALES',
    (SELECT id FROM categories_rubriques WHERE code = 'DEPENSES'),
    NULL,
    1,
    1,
    'depense',
    TRUE,
    TRUE,
    TRUE
);

-- Sous-rubriques de dépenses
INSERT INTO rubriques (id, code, nom, categorie_id, parent_id, niveau, ordre, type, est_calculee, afficher_total, actif) VALUES
(
    uuid_generate_v4(),
    'D100',
    'Dépenses de fonctionnement',
    (SELECT id FROM categories_rubriques WHERE code = 'DEPENSES'),
    (SELECT id FROM rubriques WHERE code = 'D000'),
    2,
    1,
    'depense',
    FALSE,
    TRUE,
    TRUE
),
(
    uuid_generate_v4(),
    'D110',
    'Charges de personnel',
    (SELECT id FROM categories_rubriques WHERE code = 'DEPENSES'),
    (SELECT id FROM rubriques WHERE code = 'D100'),
    3,
    1,
    'depense',
    FALSE,
    TRUE,
    TRUE
),
(
    uuid_generate_v4(),
    'D120',
    'Charges de fonctionnement courant',
    (SELECT id FROM categories_rubriques WHERE code = 'DEPENSES'),
    (SELECT id FROM rubriques WHERE code = 'D100'),
    3,
    2,
    'depense',
    FALSE,
    TRUE,
    TRUE
),
(
    uuid_generate_v4(),
    'D130',
    'Charges financières',
    (SELECT id FROM categories_rubriques WHERE code = 'DEPENSES'),
    (SELECT id FROM rubriques WHERE code = 'D100'),
    3,
    3,
    'depense',
    FALSE,
    TRUE,
    TRUE
),
(
    uuid_generate_v4(),
    'D200',
    'Dépenses d''investissement',
    (SELECT id FROM categories_rubriques WHERE code = 'DEPENSES'),
    (SELECT id FROM rubriques WHERE code = 'D000'),
    2,
    2,
    'depense',
    FALSE,
    TRUE,
    TRUE
),
(
    uuid_generate_v4(),
    'D210',
    'Équipements et infrastructures',
    (SELECT id FROM categories_rubriques WHERE code = 'DEPENSES'),
    (SELECT id FROM rubriques WHERE code = 'D200'),
    3,
    1,
    'depense',
    FALSE,
    TRUE,
    TRUE
),
(
    uuid_generate_v4(),
    'D220',
    'Remboursement d''emprunts',
    (SELECT id FROM categories_rubriques WHERE code = 'DEPENSES'),
    (SELECT id FROM rubriques WHERE code = 'D200'),
    3,
    2,
    'depense',
    FALSE,
    TRUE,
    TRUE
);

-- Rubriques de soldes
INSERT INTO rubriques (id, code, nom, categorie_id, parent_id, niveau, ordre, type, est_calculee, afficher_total, actif) VALUES
(
    uuid_generate_v4(),
    'S100',
    'Solde de fonctionnement',
    (SELECT id FROM categories_rubriques WHERE code = 'SOLDES'),
    NULL,
    1,
    1,
    'solde',
    TRUE,
    TRUE,
    TRUE
),
(
    uuid_generate_v4(),
    'S200',
    'Solde d''investissement',
    (SELECT id FROM categories_rubriques WHERE code = 'SOLDES'),
    NULL,
    1,
    2,
    'solde',
    TRUE,
    TRUE,
    TRUE
),
(
    uuid_generate_v4(),
    'S300',
    'Solde global',
    (SELECT id FROM categories_rubriques WHERE code = 'SOLDES'),
    NULL,
    1,
    3,
    'solde',
    TRUE,
    TRUE,
    TRUE
);

-- ============================================================================
-- COMMENTAIRES
-- ============================================================================

COMMENT ON TABLE roles IS 'Les données de cette table sont les rôles de base pour le système';
COMMENT ON TABLE types_documents IS 'Types de documents autorisés dans le système';
COMMENT ON TABLE types_minerais IS 'Types de minerais exploités à Madagascar - liste indicative';
COMMENT ON TABLE categories_rubriques IS 'Catégories principales pour organiser les rubriques du compte administratif';
COMMENT ON TABLE rubriques IS 'Structure hiérarchique des rubriques du compte administratif - peut être étendue selon les besoins';
