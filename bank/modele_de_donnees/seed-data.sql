-- ============================================================================
-- DONNÉES D'EXEMPLE (SEED DATA)
-- ============================================================================
-- Données de test pour la plateforme de suivi des revenus miniers
-- ============================================================================

-- ============================================================================
-- 1. COLLECTIVITÉS TERRITORIALES
-- ============================================================================

-- Régions (exemples)
INSERT INTO regions (code, nom, population, superficie, chef_lieu) VALUES
('ANA', 'Analamanga', 3618128, 16911, 'Antananarivo'),
('VAK', 'Vakinankaratra', 2074358, 16599, 'Antsirabe'),
('ATS', 'Atsinanana', 1484403, 21934, 'Toamasina'),
('ITI', 'Itasy', 897962, 6993, 'Miarinarivo'),
('ATO', 'Atsimo-Atsinanana', 1026674, 18863, 'Farafangana'),
('BOE', 'Boeny', 931171, 31046, 'Mahajanga');

-- Districts (exemples pour Analamanga et Vakinankaratra)
INSERT INTO districts (region_id, code, nom, population, superficie, chef_lieu)
SELECT
    r.id,
    d.code,
    d.nom,
    d.population,
    d.superficie,
    d.chef_lieu
FROM (VALUES
    ('ANA', 'ANTANA-R', 'Antananarivo Renivohitra', 1300000, 88, 'Antananarivo'),
    ('ANA', 'ANKAZOBE', 'Ankazobe', 215000, 6762, 'Ankazobe'),
    ('ANA', 'ANJOZOROB', 'Anjozorobe', 285000, 4922, 'Anjozorobe'),
    ('VAK', 'ANTSIR-I', 'Antsirabe I', 257500, 110, 'Antsirabe'),
    ('VAK', 'ANTSIR-II', 'Antsirabe II', 423000, 4993, 'Antsirabe'),
    ('VAK', 'BETAFO', 'Betafo', 298000, 3682, 'Betafo')
) AS d(region_code, code, nom, population, superficie, chef_lieu)
JOIN regions r ON r.code = d.region_code;

-- Communes (exemples)
INSERT INTO communes (district_id, code, nom, type, population, superficie, maire, contact_email)
SELECT
    d.id,
    c.code,
    c.nom,
    c.type,
    c.population,
    c.superficie,
    c.maire,
    c.contact_email
FROM (VALUES
    ('ANKAZOBE', 'ANKAZ-C', 'Ankazobe', 'urbaine', 35000, 45.5, 'Rakoto Jean', 'mairie.ankazobe@gov.mg'),
    ('ANKAZOBE', 'AMBATOMG', 'Ambatomanga', 'rurale', 12000, 78.2, 'Razafy Paul', 'mairie.ambatomanga@gov.mg'),
    ('ANKAZOBE', 'MIANTSO', 'Miantso', 'rurale', 8500, 92.3, 'Rabe Marie', 'mairie.miantso@gov.mg'),
    ('BETAFO', 'BETAFO-C', 'Betafo', 'urbaine', 42000, 52.1, 'Randria Joseph', 'mairie.betafo@gov.mg'),
    ('BETAFO', 'MANDROSOH', 'Mandrosohasina', 'rurale', 15000, 112.5, 'Rasolofo Claire', 'mairie.mandrosohasina@gov.mg'),
    ('ANTSIR-II', 'AMBOHIMDR', 'Ambohimandroso', 'rurale', 18000, 85.7, 'Rakotonirina Pierre', 'mairie.ambohimandroso@gov.mg')
) AS c(district_code, code, nom, type, population, superficie, maire, contact_email)
JOIN districts d ON d.code = c.district_code;

-- ============================================================================
-- 2. PROJETS MINIERS
-- ============================================================================

INSERT INTO projets_miniers (
    nom, code, type_minerai, societe_exploitante,
    region_id, district_id, commune_id,
    date_debut, statut, description
)
SELECT
    'Projet Graphite Molo',
    'GRAPH-MOLO-001',
    'Graphite',
    'NextSource Materials',
    r.id,
    d.id,
    c.id,
    '2019-01-15'::DATE,
    'en_cours',
    'Extraction de graphite de haute pureté pour batteries lithium-ion'
FROM regions r
JOIN districts d ON d.region_id = r.id
JOIN communes c ON c.district_id = d.id
WHERE r.code = 'ANA' AND d.code = 'ANKAZOBE' AND c.code = 'ANKAZ-C'

UNION ALL

SELECT
    'Projet Ilménite QIT Madagascar Minerals',
    'ILM-QMM-001',
    'Ilménite',
    'QIT Madagascar Minerals (Rio Tinto)',
    r.id,
    NULL,
    NULL,
    '2009-03-01'::DATE,
    'en_cours',
    'Extraction d''ilménite pour production de dioxyde de titane'
FROM regions r
WHERE r.code = 'ATO'

UNION ALL

SELECT
    'Projet Nickel et Cobalt Ambatovy',
    'NI-AMB-001',
    'Nickel',
    'Ambatovy Joint Venture',
    r.id,
    d.id,
    NULL,
    '2012-06-15'::DATE,
    'en_cours',
    'Extraction et raffinage de nickel et cobalt'
FROM regions r
JOIN districts d ON d.region_id = r.id
WHERE r.code = 'ATS' AND d.code LIKE 'MORAMANGA%'
LIMIT 1;

-- ============================================================================
-- 3. REVENUS MINIERS
-- ============================================================================

-- Revenus pour la commune d'Ankazobe (2023 et 2024)
INSERT INTO revenus_miniers (
    projet_minier_id, commune_id, annee, trimestre,
    type_revenu, montant, date_versement
)
SELECT
    pm.id,
    c.id,
    annee,
    trimestre,
    type_revenu,
    montant,
    date_versement
FROM (VALUES
    (2023, 1, 'ristourne', 45000000, '2023-04-15'::DATE),
    (2023, 2, 'ristourne', 52000000, '2023-07-20'::DATE),
    (2023, 3, 'ristourne', 48000000, '2023-10-18'::DATE),
    (2023, 4, 'ristourne', 55000000, '2024-01-22'::DATE),
    (2024, 1, 'ristourne', 58000000, '2024-04-16'::DATE),
    (2024, 2, 'ristourne', 61000000, '2024-07-21'::DATE),
    (2024, 1, 'redevance', 12000000, '2024-04-16'::DATE),
    (2024, 2, 'redevance', 13500000, '2024-07-21'::DATE)
) AS rev(annee, trimestre, type_revenu, montant, date_versement)
CROSS JOIN projets_miniers pm
CROSS JOIN communes c
WHERE pm.code = 'GRAPH-MOLO-001' AND c.code = 'ANKAZ-C';

-- ============================================================================
-- 4. RUBRIQUES BUDGÉTAIRES (Catalogue)
-- ============================================================================

-- Catégories principales
INSERT INTO categories_rubriques (code, nom, type, section, ordre) VALUES
('REC-FONC', 'Recettes de Fonctionnement', 'recette', 'fonctionnement', 1),
('REC-INV', 'Recettes d''Investissement', 'recette', 'investissement', 2),
('DEP-FONC', 'Dépenses de Fonctionnement', 'depense', 'fonctionnement', 3),
('DEP-INV', 'Dépenses d''Investissement', 'depense', 'investissement', 4),
('EQUI', 'Équilibre', 'equilibre', 'equilibre', 5);

-- Rubriques de recettes de fonctionnement (sélection)
INSERT INTO rubriques_budgetaires (code, intitule, categorie_id, type, section, niveau, ordre)
SELECT
    code, intitule,
    (SELECT id FROM categories_rubriques WHERE code = 'REC-FONC'),
    'recette', 'fonctionnement', niveau, ordre
FROM (VALUES
    ('R-1', 'RECETTES FISCALES', 1, 1),
    ('R-1-1', 'IMPOTS SUR LES REVENUS, BENEFICES ET GAINS', 2, 2),
    ('R-1-1-1', 'Autres impôts sur les revenus - Impôt synthétique', 3, 3),
    ('R-1-2', 'IMPOTS SUR LE PATRIMOINE', 2, 4),
    ('R-1-2-1', 'Impôts fonciers sur les terrains - IFT', 3, 5),
    ('R-1-2-2', 'Impôt foncier sur les propriétés bâties – IFPB', 3, 6),
    ('R-1-3', 'IMPOTS SUR LES BIENS ET SERVICES', 2, 7),
    ('R-1-3-1', 'Taxes sur la publicité', 3, 8),
    ('R-1-3-2', 'Taxe d''abattage', 3, 9),
    ('R-1-3-3', 'Taxe de visite et de poinçonnage des viandes', 3, 10),
    ('R-2', 'RECETTES NON FISCALES', 1, 20),
    ('R-2-1', 'CONTRIBUTIONS RECUES DES TIERS', 2, 21),
    ('R-2-1-1', 'Dotation globale - EPP', 3, 22),
    ('R-2-1-2', 'Dotation globale - CSB', 3, 23),
    ('R-2-1-3', 'Dotation globale - État civil', 3, 24),
    ('R-2-2', 'Produits des ristournes', 2, 30),
    ('R-2-3', 'Redevances', 2, 31),
    ('R-2-3-1', 'Redevances de collecte et de traitement des ordures ménagères - ROM', 3, 32),
    ('R-2-3-2', 'Redevance et frais d''administration minière', 3, 33)
) AS r(code, intitule, niveau, ordre);

-- Rubriques de dépenses de fonctionnement (sélection)
INSERT INTO rubriques_budgetaires (code, intitule, categorie_id, type, section, niveau, ordre)
SELECT
    code, intitule,
    (SELECT id FROM categories_rubriques WHERE code = 'DEP-FONC'),
    'depense', 'fonctionnement', niveau, ordre
FROM (VALUES
    ('D-1', 'CHARGES DE PERSONNEL', 1, 100),
    ('D-1-1', 'Salaires et accessoires', 2, 101),
    ('D-1-1-1', 'Personnel permanent', 3, 102),
    ('D-1-1-2', 'Personnel non permanent', 3, 103),
    ('D-1-2', 'Charges sociales patronales', 2, 110),
    ('D-1-2-1', 'Cotisations à la CNAPS', 3, 111),
    ('D-2', 'ACHATS DE BIENS', 1, 200),
    ('D-2-1', 'Achats de biens de fonctionnement général', 2, 201),
    ('D-2-1-1', 'Fournitures et articles de bureau', 3, 202),
    ('D-2-1-2', 'Imprimés, cachets et documents administratifs', 3, 203),
    ('D-2-2', 'Carburants, Lubrifiants et combustibles', 2, 210),
    ('D-3', 'ACHATS DE SERVICES ET CHARGES PERMANENTES', 1, 300),
    ('D-3-1', 'Entretien et maintenance', 2, 301),
    ('D-3-1-1', 'Entretien de bâtiments', 3, 302),
    ('D-3-1-2', 'Entretien de véhicules', 3, 303),
    ('D-3-2', 'Eau et électricité', 2, 310),
    ('D-3-3', 'Poste et télécommunications', 2, 320),
    ('D-4', 'DEPENSES D''INTERVENTION', 1, 400),
    ('D-5', 'TRANSFERTS ET SUBVENTIONS', 1, 500)
) AS d(code, intitule, niveau, ordre);

-- Rubriques d'investissement
INSERT INTO rubriques_budgetaires (code, intitule, categorie_id, type, section, niveau, ordre)
SELECT
    code, intitule,
    (SELECT id FROM categories_rubriques WHERE code = 'REC-INV'),
    'recette', 'investissement', niveau, ordre
FROM (VALUES
    ('RI-1', 'SUBVENTIONS D''EQUIPEMENT', 1, 1),
    ('RI-1-1', 'Subventions reçues de l''État', 2, 2),
    ('RI-1-2', 'Subventions reçues des Collectivités Territoriales Décentralisées', 2, 3),
    ('RI-1-3', 'Subventions reçues des Organismes nationaux et internationaux', 2, 4),
    ('RI-2', 'CESSIONS D''IMMOBILISATIONS', 1, 10)
) AS ri(code, intitule, niveau, ordre);

INSERT INTO rubriques_budgetaires (code, intitule, categorie_id, type, section, niveau, ordre)
SELECT
    code, intitule,
    (SELECT id FROM categories_rubriques WHERE code = 'DEP-INV'),
    'depense', 'investissement', niveau, ordre
FROM (VALUES
    ('DI-1', 'IMMOBILISATION INCORPORELLES', 1, 100),
    ('DI-1-1', 'Logiciels informatiques et assimilés', 2, 101),
    ('DI-1-2', 'Études et recherches', 2, 102),
    ('DI-2', 'IMMOBILISATION CORPORELLES', 1, 200),
    ('DI-2-1', 'Terrains', 2, 201),
    ('DI-2-2', 'Construction ou Réhabilitation : Bâtiments', 2, 210),
    ('DI-2-2-1', 'Bâtiments administratifs', 3, 211),
    ('DI-2-2-2', 'Bâtiments scolaires', 3, 212),
    ('DI-2-2-3', 'Bâtiments de centres de soins de santé', 3, 213),
    ('DI-2-3', 'Construction ou Réhabilitation : Voies', 2, 220),
    ('DI-2-3-1', 'Routes', 3, 221),
    ('DI-2-4', 'Construction ou Réhabilitation : Réseaux', 2, 230),
    ('DI-2-4-1', 'Réseau d''adduction d''eau', 3, 231),
    ('DI-2-4-2', 'Réseau d''assainissement', 3, 232),
    ('DI-2-4-3', 'Réseau d''électricité', 3, 233),
    ('DI-2-5', 'Matériels et outillages', 2, 240),
    ('DI-2-6', 'Matériels de transport', 2, 250)
) AS di(code, intitule, niveau, ordre);

-- ============================================================================
-- 5. COMPTE ADMINISTRATIF (Exemple pour Ankazobe 2024)
-- ============================================================================

-- Créer un compte administratif
INSERT INTO comptes_administratifs (commune_id, annee, statut, created_by)
SELECT
    c.id,
    2024,
    'publie',
    NULL -- Sera défini par l'utilisateur lors de l'utilisation réelle
FROM communes c
WHERE c.code = 'ANKAZ-C';

-- Ajouter des lignes budgétaires d'exemple
INSERT INTO lignes_budgetaires (compte_administratif_id, rubrique_id, valeurs)
SELECT
    ca.id,
    rb.id,
    valeurs::JSONB
FROM comptes_administratifs ca
CROSS JOIN (VALUES
    ('R-1-1-1', '{"budget_primitif": 5000000, "budget_additionnel": 0, "modifications": 0, "or_admis": 4200000, "recouvrement": 3800000}'::TEXT),
    ('R-1-2-1', '{"budget_primitif": 12000000, "budget_additionnel": 2000000, "modifications": 0, "or_admis": 11500000, "recouvrement": 10200000}'::TEXT),
    ('R-1-2-2', '{"budget_primitif": 8000000, "budget_additionnel": 0, "modifications": 500000, "or_admis": 7800000, "recouvrement": 7500000}'::TEXT),
    ('R-1-3-1', '{"budget_primitif": 3000000, "budget_additionnel": 0, "modifications": 0, "or_admis": 2500000, "recouvrement": 2300000}'::TEXT),
    ('R-2-1-1', '{"budget_primitif": 25000000, "budget_additionnel": 0, "modifications": 0, "or_admis": 25000000, "recouvrement": 25000000}'::TEXT),
    ('R-2-1-2', '{"budget_primitif": 18000000, "budget_additionnel": 0, "modifications": 0, "or_admis": 18000000, "recouvrement": 18000000}'::TEXT),
    ('R-2-2', '{"budget_primitif": 200000000, "budget_additionnel": 0, "modifications": 0, "or_admis": 215000000, "recouvrement": 215000000}'::TEXT),
    ('R-2-3-1', '{"budget_primitif": 15000000, "budget_additionnel": 0, "modifications": 0, "or_admis": 12000000, "recouvrement": 11500000}'::TEXT),
    ('D-1-1-1', '{"budget_primitif": 45000000, "engagement": 45000000, "mandat_admis": 45000000, "paiement": 43500000}'::TEXT),
    ('D-1-2-1', '{"budget_primitif": 6500000, "engagement": 6500000, "mandat_admis": 6500000, "paiement": 6200000}'::TEXT),
    ('D-2-1-1', '{"budget_primitif": 8000000, "engagement": 7200000, "mandat_admis": 7200000, "paiement": 6800000}'::TEXT),
    ('D-2-2', '{"budget_primitif": 12000000, "engagement": 10500000, "mandat_admis": 10500000, "paiement": 9800000}'::TEXT),
    ('D-3-1-1', '{"budget_primitif": 15000000, "engagement": 12000000, "mandat_admis": 12000000, "paiement": 10500000}'::TEXT),
    ('D-3-2', '{"budget_primitif": 5000000, "engagement": 4500000, "mandat_admis": 4500000, "paiement": 4200000}'::TEXT),
    ('D-3-3', '{"budget_primitif": 3000000, "engagement": 2800000, "mandat_admis": 2800000, "paiement": 2600000}'::TEXT),
    ('DI-2-2-2', '{"budget_primitif": 150000000, "engagement": 120000000, "mandat_admis": 100000000, "paiement": 85000000}'::TEXT),
    ('DI-2-3-1', '{"budget_primitif": 80000000, "engagement": 75000000, "mandat_admis": 70000000, "paiement": 55000000}'::TEXT),
    ('DI-2-4-1', '{"budget_primitif": 60000000, "engagement": 55000000, "mandat_admis": 50000000, "paiement": 42000000}'::TEXT)
) AS data(rubrique_code, valeurs)
JOIN rubriques_budgetaires rb ON rb.code = data.rubrique_code
WHERE ca.annee = 2024 AND EXISTS (
    SELECT 1 FROM communes c
    WHERE c.id = ca.commune_id AND c.code = 'ANKAZ-C'
);

-- ============================================================================
-- 6. NEWSLETTER (Exemples d'abonnés)
-- ============================================================================

INSERT INTO newsletter_subscribers (email, nom, prenom, organisation, statut, date_confirmation) VALUES
('jean.rakoto@example.mg', 'Rakoto', 'Jean', 'TI Madagascar', 'actif', NOW()),
('marie.rabe@example.mg', 'Rabe', 'Marie', 'PCQVP Madagascar', 'actif', NOW()),
('paul.razafy@example.mg', 'Razafy', 'Paul', 'Société Civile', 'actif', NOW());

-- ============================================================================
-- FIN DES DONNÉES D'EXEMPLE
-- ============================================================================

-- Remarques :
-- 1. Les UUID seront générés automatiquement
-- 2. Les données de profils utilisateurs seront créées lors de l'inscription via Supabase Auth
-- 3. Les analytics seront collectés automatiquement lors de l'utilisation
-- 4. Adaptez les montants et données selon vos besoins réels
