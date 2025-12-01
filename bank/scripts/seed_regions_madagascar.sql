-- =============================================================================
-- SEED DATA: GEOGRAPHIE DE MADAGASCAR
-- 6 Provinces (Faritany) et 22 Regions
-- =============================================================================

-- Suppression des donnees existantes
TRUNCATE TABLE revenus_miniers CASCADE;
TRUNCATE TABLE projets_communes CASCADE;
TRUNCATE TABLE donnees_recettes CASCADE;
TRUNCATE TABLE donnees_depenses CASCADE;
TRUNCATE TABLE documents CASCADE;
TRUNCATE TABLE communes CASCADE;
TRUNCATE TABLE regions CASCADE;
TRUNCATE TABLE provinces CASCADE;

-- =============================================================================
-- PROVINCES DE MADAGASCAR (6 Faritany)
-- =============================================================================

INSERT INTO provinces (code, nom) VALUES
('ANT', 'Antananarivo'),
('ANS', 'Antsiranana'),
('FIA', 'Fianarantsoa'),
('MAH', 'Mahajanga'),
('TOA', 'Toamasina'),
('TOL', 'Toliara');

-- =============================================================================
-- REGIONS DE MADAGASCAR (22 Regions)
-- =============================================================================

-- Province Antananarivo (4 regions)
INSERT INTO regions (code, nom, province_id) VALUES
('ANA', 'Analamanga', (SELECT id FROM provinces WHERE code = 'ANT')),
('BON', 'Bongolava', (SELECT id FROM provinces WHERE code = 'ANT')),
('ITA', 'Itasy', (SELECT id FROM provinces WHERE code = 'ANT')),
('VAK', 'Vakinankaratra', (SELECT id FROM provinces WHERE code = 'ANT'));

-- Province Antsiranana (2 regions)
INSERT INTO regions (code, nom, province_id) VALUES
('DIA', 'Diana', (SELECT id FROM provinces WHERE code = 'ANS')),
('SAV', 'Sava', (SELECT id FROM provinces WHERE code = 'ANS'));

-- Province Fianarantsoa (6 regions)
INSERT INTO regions (code, nom, province_id) VALUES
('ALA', 'Amoron''i Mania', (SELECT id FROM provinces WHERE code = 'FIA')),
('ATS', 'Atsimo-Atsinanana', (SELECT id FROM provinces WHERE code = 'FIA')),
('HAU', 'Haute Matsiatra', (SELECT id FROM provinces WHERE code = 'FIA')),
('IMO', 'Ihorombe', (SELECT id FROM provinces WHERE code = 'FIA')),
('VAF', 'Vatovavy-Fitovinany', (SELECT id FROM provinces WHERE code = 'FIA')),
('VFI', 'Vatovavy', (SELECT id FROM provinces WHERE code = 'FIA'));

-- Province Mahajanga (4 regions)
INSERT INTO regions (code, nom, province_id) VALUES
('BET', 'Betsiboka', (SELECT id FROM provinces WHERE code = 'MAH')),
('BOE', 'Boeny', (SELECT id FROM provinces WHERE code = 'MAH')),
('MEL', 'Melaky', (SELECT id FROM provinces WHERE code = 'MAH')),
('SOF', 'Sofia', (SELECT id FROM provinces WHERE code = 'MAH'));

-- Province Toamasina (3 regions)
INSERT INTO regions (code, nom, province_id) VALUES
('ALA2', 'Alaotra-Mangoro', (SELECT id FROM provinces WHERE code = 'TOA')),
('ANA2', 'Analanjirofo', (SELECT id FROM provinces WHERE code = 'TOA')),
('ATS2', 'Atsinanana', (SELECT id FROM provinces WHERE code = 'TOA'));

-- Province Toliara (4 regions)
INSERT INTO regions (code, nom, province_id) VALUES
('AND', 'Androy', (SELECT id FROM provinces WHERE code = 'TOL')),
('ANO', 'Anosy', (SELECT id FROM provinces WHERE code = 'TOL')),
('ASA', 'Atsimo-Andrefana', (SELECT id FROM provinces WHERE code = 'TOL')),
('MEN', 'Menabe', (SELECT id FROM provinces WHERE code = 'TOL'));

-- =============================================================================
-- COMMUNES EXEMPLES (quelques communes par region pour demo)
-- =============================================================================

-- Communes de la region Analamanga (Province Antananarivo)
INSERT INTO communes (code, nom, type_commune, region_id, population) VALUES
('ANT-ANA-001', 'Antananarivo Renivohitra', 'urbaine', (SELECT id FROM regions WHERE code = 'ANA'), 1275207),
('ANT-ANA-002', 'Ambohidratrimo', 'rurale', (SELECT id FROM regions WHERE code = 'ANA'), 45000),
('ANT-ANA-003', 'Ankazobe', 'rurale', (SELECT id FROM regions WHERE code = 'ANA'), 28000),
('ANT-ANA-004', 'Anjozorobe', 'rurale', (SELECT id FROM regions WHERE code = 'ANA'), 32000),
('ANT-ANA-005', 'Manjakandriana', 'rurale', (SELECT id FROM regions WHERE code = 'ANA'), 22000);

-- Communes de la region Vakinankaratra (Province Antananarivo)
INSERT INTO communes (code, nom, type_commune, region_id, population) VALUES
('ANT-VAK-001', 'Antsirabe I', 'urbaine', (SELECT id FROM regions WHERE code = 'VAK'), 238478),
('ANT-VAK-002', 'Antsirabe II', 'rurale', (SELECT id FROM regions WHERE code = 'VAK'), 85000),
('ANT-VAK-003', 'Ambatolampy', 'urbaine', (SELECT id FROM regions WHERE code = 'VAK'), 32000),
('ANT-VAK-004', 'Betafo', 'rurale', (SELECT id FROM regions WHERE code = 'VAK'), 48000);

-- Communes de la region Diana (Province Antsiranana)
INSERT INTO communes (code, nom, type_commune, region_id, population) VALUES
('ANS-DIA-001', 'Antsiranana I', 'urbaine', (SELECT id FROM regions WHERE code = 'DIA'), 115000),
('ANS-DIA-002', 'Nosy Be', 'urbaine', (SELECT id FROM regions WHERE code = 'DIA'), 45000),
('ANS-DIA-003', 'Ambilobe', 'rurale', (SELECT id FROM regions WHERE code = 'DIA'), 38000),
('ANS-DIA-004', 'Ambanja', 'rurale', (SELECT id FROM regions WHERE code = 'DIA'), 42000);

-- Communes de la region Sava (Province Antsiranana)
INSERT INTO communes (code, nom, type_commune, region_id, population) VALUES
('ANS-SAV-001', 'Sambava', 'urbaine', (SELECT id FROM regions WHERE code = 'SAV'), 52000),
('ANS-SAV-002', 'Antalaha', 'urbaine', (SELECT id FROM regions WHERE code = 'SAV'), 48000),
('ANS-SAV-003', 'Vohemar', 'rurale', (SELECT id FROM regions WHERE code = 'SAV'), 35000),
('ANS-SAV-004', 'Andapa', 'rurale', (SELECT id FROM regions WHERE code = 'SAV'), 28000);

-- Communes de la region Haute Matsiatra (Province Fianarantsoa)
INSERT INTO communes (code, nom, type_commune, region_id, population) VALUES
('FIA-HAU-001', 'Fianarantsoa I', 'urbaine', (SELECT id FROM regions WHERE code = 'HAU'), 195000),
('FIA-HAU-002', 'Ambalavao', 'rurale', (SELECT id FROM regions WHERE code = 'HAU'), 32000),
('FIA-HAU-003', 'Ambohimahasoa', 'rurale', (SELECT id FROM regions WHERE code = 'HAU'), 25000);

-- Communes de la region Anosy (Province Toliara) - Zone miniere importante
INSERT INTO communes (code, nom, type_commune, region_id, population) VALUES
('TOL-ANO-001', 'Taolagnaro (Fort-Dauphin)', 'urbaine', (SELECT id FROM regions WHERE code = 'ANO'), 85000),
('TOL-ANO-002', 'Amboasary-Atsimo', 'rurale', (SELECT id FROM regions WHERE code = 'ANO'), 28000),
('TOL-ANO-003', 'Betroka', 'rurale', (SELECT id FROM regions WHERE code = 'ANO'), 22000),
('TOL-ANO-004', 'Mandena', 'rurale', (SELECT id FROM regions WHERE code = 'ANO'), 12000);

-- Communes de la region Alaotra-Mangoro (Province Toamasina) - Zone miniere
INSERT INTO communes (code, nom, type_commune, region_id, population) VALUES
('TOA-ALA-001', 'Ambatondrazaka', 'urbaine', (SELECT id FROM regions WHERE code = 'ALA2'), 42000),
('TOA-ALA-002', 'Moramanga', 'urbaine', (SELECT id FROM regions WHERE code = 'ALA2'), 38000),
('TOA-ALA-003', 'Amparafaravola', 'rurale', (SELECT id FROM regions WHERE code = 'ALA2'), 28000);

-- Communes de la region Atsinanana (Province Toamasina)
INSERT INTO communes (code, nom, type_commune, region_id, population) VALUES
('TOA-ATS-001', 'Toamasina I', 'urbaine', (SELECT id FROM regions WHERE code = 'ATS2'), 274667),
('TOA-ATS-002', 'Toamasina II', 'rurale', (SELECT id FROM regions WHERE code = 'ATS2'), 85000),
('TOA-ATS-003', 'Brickaville', 'rurale', (SELECT id FROM regions WHERE code = 'ATS2'), 32000);

-- Communes de la region Boeny (Province Mahajanga)
INSERT INTO communes (code, nom, type_commune, region_id, population) VALUES
('MAH-BOE-001', 'Mahajanga I', 'urbaine', (SELECT id FROM regions WHERE code = 'BOE'), 226578),
('MAH-BOE-002', 'Mahajanga II', 'rurale', (SELECT id FROM regions WHERE code = 'BOE'), 65000),
('MAH-BOE-003', 'Marovoay', 'rurale', (SELECT id FROM regions WHERE code = 'BOE'), 42000);

-- Communes de la region Atsimo-Andrefana (Province Toliara)
INSERT INTO communes (code, nom, type_commune, region_id, population) VALUES
('TOL-ASA-001', 'Toliara I', 'urbaine', (SELECT id FROM regions WHERE code = 'ASA'), 168756),
('TOL-ASA-002', 'Toliara II', 'rurale', (SELECT id FROM regions WHERE code = 'ASA'), 75000),
('TOL-ASA-003', 'Sakaraha', 'rurale', (SELECT id FROM regions WHERE code = 'ASA'), 28000);

-- Communes de la region Menabe (Province Toliara)
INSERT INTO communes (code, nom, type_commune, region_id, population) VALUES
('TOL-MEN-001', 'Morondava', 'urbaine', (SELECT id FROM regions WHERE code = 'MEN'), 42000),
('TOL-MEN-002', 'Belo sur Tsiribihina', 'rurale', (SELECT id FROM regions WHERE code = 'MEN'), 22000);

-- =============================================================================
-- VERIFICATION
-- =============================================================================

-- Compte des entites geographiques
SELECT 'Provinces' as entite, COUNT(*) as nombre FROM provinces
UNION ALL
SELECT 'Regions' as entite, COUNT(*) as nombre FROM regions
UNION ALL
SELECT 'Communes' as entite, COUNT(*) as nombre FROM communes;

-- Liste des regions par province
SELECT
    p.nom AS province,
    r.code AS code_region,
    r.nom AS region,
    COUNT(c.id) AS nb_communes
FROM provinces p
JOIN regions r ON r.province_id = p.id
LEFT JOIN communes c ON c.region_id = r.id
GROUP BY p.nom, r.code, r.nom
ORDER BY p.nom, r.nom;
