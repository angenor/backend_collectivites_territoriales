-- ============================================================================
-- DONNÉES GÉOGRAPHIQUES DE MADAGASCAR
-- Régions, Départements et quelques Communes principales
-- ============================================================================

-- ============================================================================
-- RÉGIONS DE MADAGASCAR (22 Régions)
-- ============================================================================

INSERT INTO regions (id, code, nom, description, actif) VALUES
(uuid_generate_v4(), 'ANA', 'Analamanga', 'Région d''Analamanga - capitale Antananarivo', TRUE),
(uuid_generate_v4(), 'VAK', 'Vakinankaratra', 'Région de Vakinankaratra', TRUE),
(uuid_generate_v4(), 'ITO', 'Itasy', 'Région d''Itasy', TRUE),
(uuid_generate_v4(), 'BON', 'Bongolava', 'Région de Bongolava', TRUE),
(uuid_generate_v4(), 'MAT', 'Matsiatra Ambony', 'Région de Matsiatra Ambony (Haute Matsiatra)', TRUE),
(uuid_generate_v4(), 'AMO', 'Amoron''i Mania', 'Région d''Amoron''i Mania', TRUE),
(uuid_generate_v4(), 'VAT', 'Vatovavy Fitovinany', 'Région de Vatovavy Fitovinany', TRUE),
(uuid_generate_v4(), 'IHO', 'Ihorombe', 'Région d''Ihorombe', TRUE),
(uuid_generate_v4(), 'ATS', 'Atsimo Atsinanana', 'Région d''Atsimo Atsinanana', TRUE),
(uuid_generate_v4(), 'ATI', 'Atsinanana', 'Région d''Atsinanana', TRUE),
(uuid_generate_v4(), 'ANA2', 'Analanjirofo', 'Région d''Analanjirofo', TRUE),
(uuid_generate_v4(), 'ALO', 'Alaotra Mangoro', 'Région d''Alaotra Mangoro', TRUE),
(uuid_generate_v4(), 'BOE', 'Boeny', 'Région de Boeny', TRUE),
(uuid_generate_v4(), 'BET', 'Betsiboka', 'Région de Betsiboka', TRUE),
(uuid_generate_v4(), 'MEL', 'Melaky', 'Région de Melaky', TRUE),
(uuid_generate_v4(), 'SOF', 'Sofia', 'Région de Sofia', TRUE),
(uuid_generate_v4(), 'DIA', 'Diana', 'Région de Diana', TRUE),
(uuid_generate_v4(), 'SAV', 'Sava', 'Région de Sava', TRUE),
(uuid_generate_v4(), 'AND', 'Androy', 'Région d''Androy', TRUE),
(uuid_generate_v4(), 'ANO', 'Anosy', 'Région d''Anosy', TRUE),
(uuid_generate_v4(), 'MEN', 'Menabe', 'Région de Menabe', TRUE),
(uuid_generate_v4(), 'ATM', 'Atsimo Andrefana', 'Région d''Atsimo Andrefana', TRUE);

-- ============================================================================
-- DÉPARTEMENTS/DISTRICTS (Exemples pour les régions principales minières)
-- ============================================================================

-- Région Analamanga
INSERT INTO departements (id, code, nom, region_id, description, actif) VALUES
(uuid_generate_v4(), 'ANA-01', 'Antananarivo I', (SELECT id FROM regions WHERE code = 'ANA'), 'District d''Antananarivo I', TRUE),
(uuid_generate_v4(), 'ANA-02', 'Antananarivo II', (SELECT id FROM regions WHERE code = 'ANA'), 'District d''Antananarivo II', TRUE),
(uuid_generate_v4(), 'ANA-03', 'Anjozorobe', (SELECT id FROM regions WHERE code = 'ANA'), 'District d''Anjozorobe', TRUE),
(uuid_generate_v4(), 'ANA-04', 'Ankazobe', (SELECT id FROM regions WHERE code = 'ANA'), 'District d''Ankazobe', TRUE),
(uuid_generate_v4(), 'ANA-05', 'Andramasina', (SELECT id FROM regions WHERE code = 'ANA'), 'District d''Andramasina', TRUE),
(uuid_generate_v4(), 'ANA-06', 'Manjakandriana', (SELECT id FROM regions WHERE code = 'ANA'), 'District de Manjakandriana', TRUE);

-- Région Atsinanana (importante pour les mines)
INSERT INTO departements (id, code, nom, region_id, description, actif) VALUES
(uuid_generate_v4(), 'ATI-01', 'Toamasina I', (SELECT id FROM regions WHERE code = 'ATI'), 'District de Toamasina I', TRUE),
(uuid_generate_v4(), 'ATI-02', 'Toamasina II', (SELECT id FROM regions WHERE code = 'ATI'), 'District de Toamasina II', TRUE),
(uuid_generate_v4(), 'ATI-03', 'Vatomandry', (SELECT id FROM regions WHERE code = 'ATI'), 'District de Vatomandry', TRUE),
(uuid_generate_v4(), 'ATI-04', 'Mahanoro', (SELECT id FROM regions WHERE code = 'ATI'), 'District de Mahanoro', TRUE),
(uuid_generate_v4(), 'ATI-05', 'Brickaville', (SELECT id FROM regions WHERE code = 'ATI'), 'District de Brickaville', TRUE);

-- Région Anosy (Fort-Dauphin - mines importantes)
INSERT INTO departements (id, code, nom, region_id, description, actif) VALUES
(uuid_generate_v4(), 'ANO-01', 'Tôlagnaro', (SELECT id FROM regions WHERE code = 'ANO'), 'District de Tôlagnaro (Fort-Dauphin)', TRUE),
(uuid_generate_v4(), 'ANO-02', 'Amboasary-Sud', (SELECT id FROM regions WHERE code = 'ANO'), 'District d''Amboasary-Sud', TRUE),
(uuid_generate_v4(), 'ANO-03', 'Betroka', (SELECT id FROM regions WHERE code = 'ANO'), 'District de Betroka', TRUE),
(uuid_generate_v4(), 'ANO-04', 'Bekily', (SELECT id FROM regions WHERE code = 'ANO'), 'District de Bekily', TRUE);

-- Région Boeny (Mahajanga)
INSERT INTO departements (id, code, nom, region_id, description, actif) VALUES
(uuid_generate_v4(), 'BOE-01', 'Mahajanga I', (SELECT id FROM regions WHERE code = 'BOE'), 'District de Mahajanga I', TRUE),
(uuid_generate_v4(), 'BOE-02', 'Mahajanga II', (SELECT id FROM regions WHERE code = 'BOE'), 'District de Mahajanga II', TRUE),
(uuid_generate_v4(), 'BOE-03', 'Marovoay', (SELECT id FROM regions WHERE code = 'BOE'), 'District de Marovoay', TRUE),
(uuid_generate_v4(), 'BOE-04', 'Ambato-Boeny', (SELECT id FROM regions WHERE code = 'BOE'), 'District d''Ambato-Boeny', TRUE),
(uuid_generate_v4(), 'BOE-05', 'Soalala', (SELECT id FROM regions WHERE code = 'BOE'), 'District de Soalala', TRUE),
(uuid_generate_v4(), 'BOE-06', 'Mitsinjo', (SELECT id FROM regions WHERE code = 'BOE'), 'District de Mitsinjo', TRUE);

-- Région Sofia (Antsohihy)
INSERT INTO departements (id, code, nom, region_id, description, actif) VALUES
(uuid_generate_v4(), 'SOF-01', 'Antsohihy', (SELECT id FROM regions WHERE code = 'SOF'), 'District d''Antsohihy', TRUE),
(uuid_generate_v4(), 'SOF-02', 'Mandritsara', (SELECT id FROM regions WHERE code = 'SOF'), 'District de Mandritsara', TRUE),
(uuid_generate_v4(), 'SOF-03', 'Bealanana', (SELECT id FROM regions WHERE code = 'SOF'), 'District de Bealanana', TRUE),
(uuid_generate_v4(), 'SOF-04', 'Befandriana-Nord', (SELECT id FROM regions WHERE code = 'SOF'), 'District de Befandriana-Nord', TRUE),
(uuid_generate_v4(), 'SOF-05', 'Port-Bergé', (SELECT id FROM regions WHERE code = 'SOF'), 'District de Port-Bergé', TRUE),
(uuid_generate_v4(), 'SOF-06', 'Mampikony', (SELECT id FROM regions WHERE code = 'SOF'), 'District de Mampikony', TRUE),
(uuid_generate_v4(), 'SOF-07', 'Analalava', (SELECT id FROM regions WHERE code = 'SOF'), 'District d''Analalava', TRUE);

-- Région Melaky (région minière importante)
INSERT INTO departements (id, code, nom, region_id, description, actif) VALUES
(uuid_generate_v4(), 'MEL-01', 'Maintirano', (SELECT id FROM regions WHERE code = 'MEL'), 'District de Maintirano', TRUE),
(uuid_generate_v4(), 'MEL-02', 'Morafenobe', (SELECT id FROM regions WHERE code = 'MEL'), 'District de Morafenobe', TRUE),
(uuid_generate_v4(), 'MEL-03', 'Besalampy', (SELECT id FROM regions WHERE code = 'MEL'), 'District de Besalampy', TRUE),
(uuid_generate_v4(), 'MEL-04', 'Antsalova', (SELECT id FROM regions WHERE code = 'MEL'), 'District d''Antsalova', TRUE);

-- Région Vakinankaratra
INSERT INTO departements (id, code, nom, region_id, description, actif) VALUES
(uuid_generate_v4(), 'VAK-01', 'Antsirabe I', (SELECT id FROM regions WHERE code = 'VAK'), 'District d''Antsirabe I', TRUE),
(uuid_generate_v4(), 'VAK-02', 'Antsirabe II', (SELECT id FROM regions WHERE code = 'VAK'), 'District d''Antsirabe II', TRUE),
(uuid_generate_v4(), 'VAK-03', 'Ambatolampy', (SELECT id FROM regions WHERE code = 'VAK'), 'District d''Ambatolampy', TRUE),
(uuid_generate_v4(), 'VAK-04', 'Betafo', (SELECT id FROM regions WHERE code = 'VAK'), 'District de Betafo', TRUE),
(uuid_generate_v4(), 'VAK-05', 'Antanifotsy', (SELECT id FROM regions WHERE code = 'VAK'), 'District d''Antanifotsy', TRUE),
(uuid_generate_v4(), 'VAK-06', 'Faratsiho', (SELECT id FROM regions WHERE code = 'VAK'), 'District de Faratsiho', TRUE),
(uuid_generate_v4(), 'VAK-07', 'Mandoto', (SELECT id FROM regions WHERE code = 'VAK'), 'District de Mandoto', TRUE);

-- ============================================================================
-- COMMUNES (Exemples de communes avec projets miniers importants)
-- ============================================================================

-- Communes de la région Anosy (QMM - Rio Tinto)
INSERT INTO communes (id, code, nom, departement_id, region_id, population, description, actif) VALUES
(uuid_generate_v4(), 'ANO-01-001', 'Tôlagnaro (Fort-Dauphin)',
    (SELECT id FROM departements WHERE code = 'ANO-01'),
    (SELECT id FROM regions WHERE code = 'ANO'),
    60000,
    'Chef-lieu de région - Zone d''exploitation QMM',
    TRUE),
(uuid_generate_v4(), 'ANO-01-002', 'Mandena',
    (SELECT id FROM departements WHERE code = 'ANO-01'),
    (SELECT id FROM regions WHERE code = 'ANO'),
    5000,
    'Zone d''exploitation ilménite QMM',
    TRUE),
(uuid_generate_v4(), 'ANO-01-003', 'Sainte-Luce',
    (SELECT id FROM departements WHERE code = 'ANO-01'),
    (SELECT id FROM regions WHERE code = 'ANO'),
    8000,
    'Zone côtière - projet QMM',
    TRUE);

-- Communes de la région Atsinanana (Ambatovy - Nickel-Cobalt)
INSERT INTO communes (id, code, nom, departement_id, region_id, population, description, actif) VALUES
(uuid_generate_v4(), 'ATI-01-001', 'Toamasina',
    (SELECT id FROM departements WHERE code = 'ATI-01'),
    (SELECT id FROM regions WHERE code = 'ATI'),
    320000,
    'Capitale économique - Port d''exportation minière',
    TRUE),
(uuid_generate_v4(), 'ATI-02-001', 'Moramanga',
    (SELECT id FROM departements WHERE code = 'ATI-02'),
    (SELECT id FROM regions WHERE code = 'ATI'),
    50000,
    'Zone du projet Ambatovy (Nickel-Cobalt)',
    TRUE);

-- Communes de la région Analamanga
INSERT INTO communes (id, code, nom, departement_id, region_id, population, description, actif) VALUES
(uuid_generate_v4(), 'ANA-01-001', 'Antananarivo',
    (SELECT id FROM departements WHERE code = 'ANA-01'),
    (SELECT id FROM regions WHERE code = 'ANA'),
    1300000,
    'Capitale nationale',
    TRUE),
(uuid_generate_v4(), 'ANA-03-001', 'Anjozorobe',
    (SELECT id FROM departements WHERE code = 'ANA-03'),
    (SELECT id FROM regions WHERE code = 'ANA'),
    15000,
    'Zone d''exploration minière',
    TRUE);

-- Communes de la région Sofia (graphite et pierres précieuses)
INSERT INTO communes (id, code, nom, departement_id, region_id, population, description, actif) VALUES
(uuid_generate_v4(), 'SOF-01-001', 'Antsohihy',
    (SELECT id FROM departements WHERE code = 'SOF-01'),
    (SELECT id FROM regions WHERE code = 'SOF'),
    35000,
    'Chef-lieu de région - Zone minière',
    TRUE),
(uuid_generate_v4(), 'SOF-02-001', 'Mandritsara',
    (SELECT id FROM departements WHERE code = 'SOF-02'),
    (SELECT id FROM regions WHERE code = 'SOF'),
    25000,
    'Zone d''exploitation de graphite',
    TRUE);

-- Communes de la région Boeny
INSERT INTO communes (id, code, nom, departement_id, region_id, population, description, actif) VALUES
(uuid_generate_v4(), 'BOE-01-001', 'Mahajanga',
    (SELECT id FROM departements WHERE code = 'BOE-01'),
    (SELECT id FROM regions WHERE code = 'BOE'),
    220000,
    'Chef-lieu de région - Port important',
    TRUE);

-- Communes de la région Vakinankaratra (mines artisanales)
INSERT INTO communes (id, code, nom, departement_id, region_id, population, description, actif) VALUES
(uuid_generate_v4(), 'VAK-01-001', 'Antsirabe',
    (SELECT id FROM departements WHERE code = 'VAK-01'),
    (SELECT id FROM regions WHERE code = 'VAK'),
    250000,
    'Troisième ville de Madagascar',
    TRUE),
(uuid_generate_v4(), 'VAK-03-001', 'Ambatolampy',
    (SELECT id FROM departements WHERE code = 'VAK-03'),
    (SELECT id FROM regions WHERE code = 'VAK'),
    30000,
    'Zone d''exploitation minière artisanale',
    TRUE);

-- ============================================================================
-- COMMENTAIRES
-- ============================================================================

COMMENT ON TABLE regions IS 'Les 22 régions administratives de Madagascar';
COMMENT ON TABLE departements IS 'Districts des régions - focus sur les zones minières importantes';
COMMENT ON TABLE communes IS 'Communes principales - notamment celles avec des projets miniers actifs ou potentiels';
