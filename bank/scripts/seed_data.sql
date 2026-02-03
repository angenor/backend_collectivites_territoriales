-- =============================================================================
-- SEED DATA: DONNEES DE DEMONSTRATION
-- Exercices, Societes Minieres, Projets, Utilisateurs, Donnees Financieres
-- =============================================================================

-- =============================================================================
-- 1. EXERCICES BUDGETAIRES
-- =============================================================================

INSERT INTO exercices (annee, libelle, date_debut, date_fin, cloture) VALUES
(2022, 'Exercice 2022', '2022-01-01', '2022-12-31', TRUE),
(2023, 'Exercice 2023', '2023-01-01', '2023-12-31', TRUE),
(2024, 'Exercice 2024', '2024-01-01', '2024-12-31', FALSE),
(2025, 'Exercice 2025', '2025-01-01', '2025-12-31', FALSE);

-- =============================================================================
-- 2. SOCIETES MINIERES
-- =============================================================================

INSERT INTO societes_minieres (nom, nif, stat, siege_social, telephone, email, site_web) VALUES
('QIT Madagascar Minerals (QMM)', '1000012345', '45678901', 'Fort-Dauphin, Region Anosy', '+261 34 00 000 01', 'contact@qmm.mg', 'https://www.riotinto.com/qmm'),
('Ambatovy', '1000012346', '45678902', 'Toamasina, Region Atsinanana', '+261 34 00 000 02', 'info@ambatovy.com', 'https://www.ambatovy.com'),
('Toliara Sands', '1000012347', '45678903', 'Toliara, Region Atsimo-Andrefana', '+261 34 00 000 03', 'contact@toliarasands.com', 'https://www.toliarasands.com'),
('KRAOMA', '1000012348', '45678904', 'Brieville, Region Sofia', '+261 34 00 000 04', 'contact@kraoma.mg', 'https://www.kraoma.mg'),
('Base Toliara', '1000012349', '45678905', 'Toliara, Region Atsimo-Andrefana', '+261 34 00 000 05', 'info@baseresources.com.au', 'https://www.baseresources.com.au');

-- =============================================================================
-- 3. PROJETS MINIERS
-- =============================================================================

INSERT INTO projets_miniers (nom, societe_id, type_minerai, statut, date_debut_exploitation, surface_ha, description) VALUES
-- QMM - Ilmenite Fort-Dauphin
('Projet QMM Fort-Dauphin',
 (SELECT id FROM societes_minieres WHERE nom LIKE 'QIT%'),
 'Ilmenite, Zircon',
 'exploitation',
 '2009-01-01',
 6000,
 'Extraction de sables mineraux (ilmenite et zircon) dans la region Anosy'),

-- Ambatovy - Nickel/Cobalt
('Projet Ambatovy',
 (SELECT id FROM societes_minieres WHERE nom = 'Ambatovy'),
 'Nickel, Cobalt',
 'exploitation',
 '2012-01-01',
 11000,
 'Mine de nickel-cobalt lateritique, une des plus grandes au monde'),

-- Toliara Sands
('Projet Toliara Sands',
 (SELECT id FROM societes_minieres WHERE nom = 'Toliara Sands'),
 'Ilmenite',
 'exploration',
 NULL,
 8000,
 'Projet de sables mineraux dans le sud-ouest de Madagascar'),

-- KRAOMA Chromite
('Mine de Chromite Bemanevika',
 (SELECT id FROM societes_minieres WHERE nom = 'KRAOMA'),
 'Chromite',
 'exploitation',
 '1968-01-01',
 2500,
 'Exploitation de chromite par la societe nationale KRAOMA'),

-- Base Toliara
('Projet Base Toliara',
 (SELECT id FROM societes_minieres WHERE nom = 'Base Toliara'),
 'Ilmenite, Zircon, Rutile',
 'exploration',
 NULL,
 9500,
 'Projet de sables mineraux lourds dans la region de Toliara');

-- =============================================================================
-- 4. LIAISON PROJETS - COMMUNES
-- =============================================================================

-- QMM Fort-Dauphin - Communes de la region Anosy
INSERT INTO projets_communes (projet_id, commune_id, pourcentage_territoire, date_debut) VALUES
((SELECT id FROM projets_miniers WHERE nom LIKE 'Projet QMM%'),
 (SELECT id FROM communes WHERE nom = 'Taolagnaro (Fort-Dauphin)'),
 15.5, '2009-01-01'),
((SELECT id FROM projets_miniers WHERE nom LIKE 'Projet QMM%'),
 (SELECT id FROM communes WHERE nom = 'Mandena'),
 45.0, '2009-01-01'),
((SELECT id FROM projets_miniers WHERE nom LIKE 'Projet QMM%'),
 (SELECT id FROM communes WHERE nom = 'Amboasary-Atsimo'),
 8.0, '2009-01-01');

-- Ambatovy - Communes de la region Alaotra-Mangoro
INSERT INTO projets_communes (projet_id, commune_id, pourcentage_territoire, date_debut) VALUES
((SELECT id FROM projets_miniers WHERE nom = 'Projet Ambatovy'),
 (SELECT id FROM communes WHERE nom = 'Moramanga'),
 25.0, '2012-01-01'),
((SELECT id FROM projets_miniers WHERE nom = 'Projet Ambatovy'),
 (SELECT id FROM communes WHERE nom = 'Amparafaravola'),
 12.0, '2012-01-01');

-- =============================================================================
-- 5. UTILISATEURS DE DEMONSTRATION
-- =============================================================================

-- Mot de passe: 'admin123' -> hash bcrypt genere avec passlib
INSERT INTO utilisateurs (email, mot_de_passe_hash, nom, prenom, role, actif, email_verifie) VALUES
('admin@transparency.mg', '$2b$12$XYd/1budbWgSrWbeTMO0GOTfEarX/pvQMlvejeAnZTR2FNSV1b/XS', 'Administrateur', 'TI-MG', 'admin', TRUE, TRUE),
('editeur@transparency.mg', '$2b$12$XYd/1budbWgSrWbeTMO0GOTfEarX/pvQMlvejeAnZTR2FNSV1b/XS', 'Editeur', 'TI-MG', 'editeur', TRUE, TRUE),
('lecteur@transparency.mg', '$2b$12$XYd/1budbWgSrWbeTMO0GOTfEarX/pvQMlvejeAnZTR2FNSV1b/XS', 'Visiteur', 'Public', 'lecteur', TRUE, TRUE);

-- Utilisateur lie a une commune
INSERT INTO utilisateurs (email, mot_de_passe_hash, nom, prenom, role, commune_id, actif, email_verifie) VALUES
('maire.fortdauphin@commune.mg', '$2b$12$XYd/1budbWgSrWbeTMO0GOTfEarX/pvQMlvejeAnZTR2FNSV1b/XS',
 'Razafy', 'Jean',
 'commune',
 (SELECT id FROM communes WHERE nom = 'Taolagnaro (Fort-Dauphin)'),
 TRUE, TRUE);

-- =============================================================================
-- 6. REVENUS MINIERS (Donnees de demonstration)
-- =============================================================================

-- Revenus miniers pour Fort-Dauphin (QMM)
INSERT INTO revenus_miniers (commune_id, exercice_id, projet_id, type_revenu, montant_prevu, montant_recu, date_reception, compte_code, commentaire)
SELECT
    c.id,
    e.id,
    p.id,
    'ristourne_miniere',
    CASE e.annee
        WHEN 2022 THEN 450000000
        WHEN 2023 THEN 520000000
        WHEN 2024 THEN 580000000
        ELSE 0
    END,
    CASE e.annee
        WHEN 2022 THEN 445000000
        WHEN 2023 THEN 515000000
        WHEN 2024 THEN 0
        ELSE 0
    END,
    CASE e.annee
        WHEN 2022 THEN '2022-06-15'::DATE
        WHEN 2023 THEN '2023-06-20'::DATE
        ELSE NULL
    END,
    '7717',
    'Ristournes minieres du projet QMM'
FROM communes c
CROSS JOIN exercices e
CROSS JOIN projets_miniers p
WHERE c.nom = 'Taolagnaro (Fort-Dauphin)'
  AND p.nom LIKE 'Projet QMM%'
  AND e.annee IN (2022, 2023, 2024);

-- Revenus miniers pour Moramanga (Ambatovy)
INSERT INTO revenus_miniers (commune_id, exercice_id, projet_id, type_revenu, montant_prevu, montant_recu, date_reception, compte_code, commentaire)
SELECT
    c.id,
    e.id,
    p.id,
    'ristourne_miniere',
    CASE e.annee
        WHEN 2022 THEN 380000000
        WHEN 2023 THEN 420000000
        WHEN 2024 THEN 450000000
        ELSE 0
    END,
    CASE e.annee
        WHEN 2022 THEN 375000000
        WHEN 2023 THEN 418000000
        WHEN 2024 THEN 0
        ELSE 0
    END,
    CASE e.annee
        WHEN 2022 THEN '2022-07-10'::DATE
        WHEN 2023 THEN '2023-07-15'::DATE
        ELSE NULL
    END,
    '7717',
    'Ristournes minieres du projet Ambatovy'
FROM communes c
CROSS JOIN exercices e
CROSS JOIN projets_miniers p
WHERE c.nom = 'Moramanga'
  AND p.nom = 'Projet Ambatovy'
  AND e.annee IN (2022, 2023, 2024);

-- =============================================================================
-- 7. DONNEES RECETTES DE DEMONSTRATION (Commune Fort-Dauphin, 2023)
-- =============================================================================

-- Quelques lignes de recettes pour Fort-Dauphin exercice 2023
INSERT INTO donnees_recettes (commune_id, exercice_id, compte_code, budget_primitif, budget_additionnel, modifications, previsions_definitives, or_admis, recouvrement, reste_a_recouvrer)
SELECT
    c.id,
    e.id,
    pc.code,
    CASE pc.code
        WHEN '7140' THEN 85000000
        WHEN '7151' THEN 120000000
        WHEN '7251' THEN 45000000
        WHEN '7261' THEN 12000000
        WHEN '7713' THEN 25000000
        WHEN '7717' THEN 520000000  -- Ristournes minieres
        WHEN '7721' THEN 35000000
        WHEN '7732' THEN 18000000
        ELSE 0
    END,
    CASE pc.code
        WHEN '7140' THEN 5000000
        WHEN '7151' THEN 10000000
        WHEN '7717' THEN 0
        ELSE 0
    END,
    0,
    CASE pc.code
        WHEN '7140' THEN 90000000
        WHEN '7151' THEN 130000000
        WHEN '7251' THEN 45000000
        WHEN '7261' THEN 12000000
        WHEN '7713' THEN 25000000
        WHEN '7717' THEN 520000000
        WHEN '7721' THEN 35000000
        WHEN '7732' THEN 18000000
        ELSE 0
    END,
    CASE pc.code
        WHEN '7140' THEN 88000000
        WHEN '7151' THEN 125000000
        WHEN '7251' THEN 42000000
        WHEN '7261' THEN 11500000
        WHEN '7713' THEN 24000000
        WHEN '7717' THEN 515000000
        WHEN '7721' THEN 33000000
        WHEN '7732' THEN 17500000
        ELSE 0
    END,
    CASE pc.code
        WHEN '7140' THEN 86000000
        WHEN '7151' THEN 122000000
        WHEN '7251' THEN 40000000
        WHEN '7261' THEN 11000000
        WHEN '7713' THEN 23500000
        WHEN '7717' THEN 515000000
        WHEN '7721' THEN 32000000
        WHEN '7732' THEN 17000000
        ELSE 0
    END,
    CASE pc.code
        WHEN '7140' THEN 2000000
        WHEN '7151' THEN 3000000
        WHEN '7251' THEN 2000000
        WHEN '7261' THEN 500000
        WHEN '7713' THEN 500000
        WHEN '7717' THEN 0
        WHEN '7721' THEN 1000000
        WHEN '7732' THEN 500000
        ELSE 0
    END
FROM communes c
CROSS JOIN exercices e
CROSS JOIN plan_comptable pc
WHERE c.nom = 'Taolagnaro (Fort-Dauphin)'
  AND e.annee = 2023
  AND pc.code IN ('7140', '7151', '7251', '7261', '7713', '7717', '7721', '7732')
  AND pc.niveau = 3;

-- =============================================================================
-- 8. DONNEES DEPENSES DE DEMONSTRATION (Commune Fort-Dauphin, 2023)
-- =============================================================================

INSERT INTO donnees_depenses (commune_id, exercice_id, compte_code, programme, budget_primitif, budget_additionnel, modifications, previsions_definitives, engagement, mandat_admis, paiement, reste_a_payer)
SELECT
    c.id,
    e.id,
    pc.code,
    'Programme General',
    CASE pc.code
        WHEN '6011' THEN 180000000
        WHEN '6012' THEN 45000000
        WHEN '6111' THEN 12000000
        WHEN '6131' THEN 25000000
        WHEN '6211' THEN 35000000
        WHEN '6250' THEN 18000000
        WHEN '6264' THEN 8000000
        WHEN '2132' THEN 150000000  -- Batiments scolaires
        WHEN '2141' THEN 200000000  -- Routes
        WHEN '2151' THEN 80000000   -- Reseau eau
        ELSE 0
    END,
    CASE pc.code
        WHEN '6011' THEN 10000000
        WHEN '2132' THEN 20000000
        WHEN '2141' THEN 30000000
        ELSE 0
    END,
    0,
    CASE pc.code
        WHEN '6011' THEN 190000000
        WHEN '6012' THEN 45000000
        WHEN '6111' THEN 12000000
        WHEN '6131' THEN 25000000
        WHEN '6211' THEN 35000000
        WHEN '6250' THEN 18000000
        WHEN '6264' THEN 8000000
        WHEN '2132' THEN 170000000
        WHEN '2141' THEN 230000000
        WHEN '2151' THEN 80000000
        ELSE 0
    END,
    CASE pc.code
        WHEN '6011' THEN 185000000
        WHEN '6012' THEN 44000000
        WHEN '6111' THEN 11500000
        WHEN '6131' THEN 24000000
        WHEN '6211' THEN 34000000
        WHEN '6250' THEN 17500000
        WHEN '6264' THEN 7800000
        WHEN '2132' THEN 165000000
        WHEN '2141' THEN 220000000
        WHEN '2151' THEN 75000000
        ELSE 0
    END,
    CASE pc.code
        WHEN '6011' THEN 185000000
        WHEN '6012' THEN 44000000
        WHEN '6111' THEN 11500000
        WHEN '6131' THEN 24000000
        WHEN '6211' THEN 34000000
        WHEN '6250' THEN 17500000
        WHEN '6264' THEN 7800000
        WHEN '2132' THEN 165000000
        WHEN '2141' THEN 220000000
        WHEN '2151' THEN 75000000
        ELSE 0
    END,
    CASE pc.code
        WHEN '6011' THEN 182000000
        WHEN '6012' THEN 43000000
        WHEN '6111' THEN 11000000
        WHEN '6131' THEN 23500000
        WHEN '6211' THEN 33000000
        WHEN '6250' THEN 17000000
        WHEN '6264' THEN 7500000
        WHEN '2132' THEN 160000000
        WHEN '2141' THEN 215000000
        WHEN '2151' THEN 72000000
        ELSE 0
    END,
    CASE pc.code
        WHEN '6011' THEN 3000000
        WHEN '6012' THEN 1000000
        WHEN '6111' THEN 500000
        WHEN '6131' THEN 500000
        WHEN '6211' THEN 1000000
        WHEN '6250' THEN 500000
        WHEN '6264' THEN 300000
        WHEN '2132' THEN 5000000
        WHEN '2141' THEN 5000000
        WHEN '2151' THEN 3000000
        ELSE 0
    END
FROM communes c
CROSS JOIN exercices e
CROSS JOIN plan_comptable pc
WHERE c.nom = 'Taolagnaro (Fort-Dauphin)'
  AND e.annee = 2023
  AND pc.code IN ('6011', '6012', '6111', '6131', '6211', '6250', '6264', '2132', '2141', '2151')
  AND pc.niveau = 3;

-- =============================================================================
-- 9. ABONNES NEWSLETTER
-- =============================================================================

INSERT INTO newsletter_abonnes (email, nom, actif) VALUES
('citoyen1@example.com', 'Rakoto Jean', TRUE),
('citoyen2@example.com', 'Rasoa Marie', TRUE),
('ong@example.org', 'ONG Locale', TRUE),
('journaliste@media.mg', 'Journaliste Local', TRUE);

-- =============================================================================
-- 10. STATISTIQUES DE VISITES (Exemple)
-- =============================================================================

INSERT INTO statistiques_visites (date_visite, page, commune_id, nb_visites, nb_telechargements)
SELECT
    CURRENT_DATE - (n || ' days')::INTERVAL,
    '/commune/' || c.id,
    c.id,
    floor(random() * 50 + 10)::INTEGER,
    floor(random() * 5)::INTEGER
FROM communes c
CROSS JOIN generate_series(0, 30) AS n
WHERE c.nom IN ('Taolagnaro (Fort-Dauphin)', 'Moramanga', 'Antananarivo Renivohitra')
LIMIT 50;

-- =============================================================================
-- VERIFICATION FINALE
-- =============================================================================

SELECT '=== RESUME DES DONNEES INSEREES ===' AS info;

SELECT 'Exercices' AS table_name, COUNT(*) AS count FROM exercices
UNION ALL
SELECT 'Societes minieres', COUNT(*) FROM societes_minieres
UNION ALL
SELECT 'Projets miniers', COUNT(*) FROM projets_miniers
UNION ALL
SELECT 'Projets-Communes', COUNT(*) FROM projets_communes
UNION ALL
SELECT 'Utilisateurs', COUNT(*) FROM utilisateurs
UNION ALL
SELECT 'Revenus miniers', COUNT(*) FROM revenus_miniers
UNION ALL
SELECT 'Donnees recettes', COUNT(*) FROM donnees_recettes
UNION ALL
SELECT 'Donnees depenses', COUNT(*) FROM donnees_depenses
UNION ALL
SELECT 'Newsletter abonnes', COUNT(*) FROM newsletter_abonnes
UNION ALL
SELECT 'Statistiques visites', COUNT(*) FROM statistiques_visites;

-- Test de la vue recettes
SELECT '=== TEST VUE RECETTES (Fort-Dauphin 2023) ===' AS info;
SELECT
    commune_nom,
    exercice,
    compte,
    intitule,
    budget_primitif,
    or_admis,
    recouvrement,
    taux_execution
FROM vue_tableau_recettes
WHERE commune_nom = 'Taolagnaro (Fort-Dauphin)'
  AND exercice = 2023
  AND budget_primitif > 0
ORDER BY ordre_affichage
LIMIT 10;
