-- =============================================================================
-- SCHEMA DE BASE DE DONNEES POSTGRESQL
-- Plateforme de Suivi des Revenus Miniers des Collectivites Territoriales
-- Version: 1.0
-- Date: 2025-12-01
-- =============================================================================

-- Suppression des tables existantes (dans l'ordre inverse des dependances)
DROP VIEW IF EXISTS vue_tableau_equilibre CASCADE;
DROP VIEW IF EXISTS vue_tableau_depenses CASCADE;
DROP VIEW IF EXISTS vue_tableau_recettes CASCADE;

DROP TABLE IF EXISTS audit_log CASCADE;
DROP TABLE IF EXISTS statistiques_visites CASCADE;
DROP TABLE IF EXISTS newsletter_abonnes CASCADE;
DROP TABLE IF EXISTS documents CASCADE;
DROP TABLE IF EXISTS sessions CASCADE;
DROP TABLE IF EXISTS revenus_miniers CASCADE;
DROP TABLE IF EXISTS projets_communes CASCADE;
DROP TABLE IF EXISTS projets_miniers CASCADE;
DROP TABLE IF EXISTS societes_minieres CASCADE;
DROP TABLE IF EXISTS donnees_depenses CASCADE;
DROP TABLE IF EXISTS donnees_recettes CASCADE;
DROP TABLE IF EXISTS exercices CASCADE;
DROP TABLE IF EXISTS plan_comptable CASCADE;
DROP TABLE IF EXISTS utilisateurs CASCADE;
DROP TABLE IF EXISTS communes CASCADE;
DROP TABLE IF EXISTS regions CASCADE;
DROP TABLE IF EXISTS provinces CASCADE;

DROP TYPE IF EXISTS type_document CASCADE;
DROP TYPE IF EXISTS role_utilisateur CASCADE;
DROP TYPE IF EXISTS section_budgetaire CASCADE;
DROP TYPE IF EXISTS type_mouvement CASCADE;

-- =============================================================================
-- TYPES ENUMERES
-- =============================================================================

-- Types de mouvement financier
CREATE TYPE type_mouvement AS ENUM ('recette', 'depense');

-- Sections budgetaires
CREATE TYPE section_budgetaire AS ENUM ('fonctionnement', 'investissement');

-- Roles utilisateurs
CREATE TYPE role_utilisateur AS ENUM ('admin', 'editeur', 'lecteur', 'commune');

-- Types de documents
CREATE TYPE type_document AS ENUM (
    'compte_administratif',
    'budget_primitif',
    'budget_additionnel',
    'piece_justificative',
    'rapport',
    'autre'
);

-- =============================================================================
-- 1. TABLES GEOGRAPHIQUES
-- =============================================================================

-- Provinces de Madagascar (6 provinces)
CREATE TABLE provinces (
    id SERIAL PRIMARY KEY,
    code VARCHAR(10) UNIQUE NOT NULL,
    nom VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

COMMENT ON TABLE provinces IS 'Les 6 provinces de Madagascar';
COMMENT ON COLUMN provinces.code IS 'Code unique de la province (ex: ANT pour Antananarivo)';

-- Regions de Madagascar (22 regions)
CREATE TABLE regions (
    id SERIAL PRIMARY KEY,
    code VARCHAR(10) UNIQUE NOT NULL,
    nom VARCHAR(100) NOT NULL,
    province_id INTEGER NOT NULL REFERENCES provinces(id) ON DELETE CASCADE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

COMMENT ON TABLE regions IS 'Les 22 regions de Madagascar';
COMMENT ON COLUMN regions.province_id IS 'Reference vers la province parente';

CREATE INDEX idx_regions_province ON regions(province_id);

-- Communes de Madagascar
CREATE TABLE communes (
    id SERIAL PRIMARY KEY,
    code VARCHAR(20) UNIQUE NOT NULL,
    nom VARCHAR(150) NOT NULL,
    type_commune VARCHAR(20) CHECK (type_commune IN ('urbaine', 'rurale')),
    region_id INTEGER NOT NULL REFERENCES regions(id) ON DELETE CASCADE,
    population INTEGER,
    superficie_km2 DECIMAL(10, 2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

COMMENT ON TABLE communes IS 'Communes de Madagascar (collectivites territoriales)';
COMMENT ON COLUMN communes.type_commune IS 'Type: urbaine ou rurale';

CREATE INDEX idx_communes_region ON communes(region_id);
CREATE INDEX idx_communes_nom ON communes(nom);

-- =============================================================================
-- 2. TABLE PLAN COMPTABLE
-- =============================================================================

-- Plan comptable hierarchique (base sur le modele du compte administratif)
CREATE TABLE plan_comptable (
    id SERIAL PRIMARY KEY,
    code VARCHAR(10) UNIQUE NOT NULL,
    intitule VARCHAR(255) NOT NULL,
    niveau INTEGER NOT NULL CHECK (niveau BETWEEN 1 AND 3),
    type_mouvement type_mouvement NOT NULL,
    section section_budgetaire NOT NULL,
    parent_code VARCHAR(10),
    est_sommable BOOLEAN DEFAULT TRUE,
    ordre_affichage INTEGER,
    actif BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_plan_comptable_parent
        FOREIGN KEY (parent_code) REFERENCES plan_comptable(code)
        ON DELETE SET NULL
);

COMMENT ON TABLE plan_comptable IS 'Plan comptable hierarchique des collectivites territoriales';
COMMENT ON COLUMN plan_comptable.code IS 'Code comptable (2, 3 ou 4 chiffres)';
COMMENT ON COLUMN plan_comptable.niveau IS '1=categorie principale, 2=sous-categorie, 3=ligne detail';
COMMENT ON COLUMN plan_comptable.type_mouvement IS 'recette ou depense';
COMMENT ON COLUMN plan_comptable.section IS 'fonctionnement ou investissement';
COMMENT ON COLUMN plan_comptable.parent_code IS 'Code du compte parent pour la hierarchie';
COMMENT ON COLUMN plan_comptable.est_sommable IS 'Si true, les valeurs enfants sont sommees';
COMMENT ON COLUMN plan_comptable.ordre_affichage IS 'Ordre pour reproduire la structure Excel';

CREATE INDEX idx_plan_comptable_parent ON plan_comptable(parent_code);
CREATE INDEX idx_plan_comptable_type ON plan_comptable(type_mouvement, section);
CREATE INDEX idx_plan_comptable_niveau ON plan_comptable(niveau);
CREATE INDEX idx_plan_comptable_ordre ON plan_comptable(type_mouvement, section, ordre_affichage);

-- =============================================================================
-- 3. TABLES EXERCICES ET DONNEES FINANCIERES
-- =============================================================================

-- Exercices budgetaires (annees fiscales)
CREATE TABLE exercices (
    id SERIAL PRIMARY KEY,
    annee INTEGER UNIQUE NOT NULL,
    libelle VARCHAR(50),
    date_debut DATE NOT NULL,
    date_fin DATE NOT NULL,
    cloture BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT chk_exercice_dates CHECK (date_fin > date_debut)
);

COMMENT ON TABLE exercices IS 'Exercices budgetaires annuels';
COMMENT ON COLUMN exercices.annee IS 'Annee fiscale (ex: 2024)';
COMMENT ON COLUMN exercices.cloture IS 'True si lexercice est cloture et non modifiable';

CREATE INDEX idx_exercices_annee ON exercices(annee);

-- Donnees RECETTES par commune/exercice/compte
CREATE TABLE donnees_recettes (
    id SERIAL PRIMARY KEY,
    commune_id INTEGER NOT NULL REFERENCES communes(id) ON DELETE CASCADE,
    exercice_id INTEGER NOT NULL REFERENCES exercices(id) ON DELETE CASCADE,
    compte_code VARCHAR(10) NOT NULL REFERENCES plan_comptable(code) ON DELETE CASCADE,

    -- Colonnes financieres (en Ariary - MGA)
    budget_primitif DECIMAL(18, 2) DEFAULT 0,
    budget_additionnel DECIMAL(18, 2) DEFAULT 0,
    modifications DECIMAL(18, 2) DEFAULT 0,
    previsions_definitives DECIMAL(18, 2) DEFAULT 0,
    or_admis DECIMAL(18, 2) DEFAULT 0,
    recouvrement DECIMAL(18, 2) DEFAULT 0,
    reste_a_recouvrer DECIMAL(18, 2) DEFAULT 0,

    -- Metadonnees
    commentaire TEXT,
    valide BOOLEAN DEFAULT FALSE,
    valide_par INTEGER,
    valide_le TIMESTAMP,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT uk_recettes_commune_exercice_compte
        UNIQUE (commune_id, exercice_id, compte_code)
);

COMMENT ON TABLE donnees_recettes IS 'Donnees financieres des recettes par commune/exercice/compte';
COMMENT ON COLUMN donnees_recettes.budget_primitif IS 'Budget Primitif en Ariary';
COMMENT ON COLUMN donnees_recettes.budget_additionnel IS 'Budget Additionnel en Ariary';
COMMENT ON COLUMN donnees_recettes.modifications IS 'Modifications +/- en Ariary';
COMMENT ON COLUMN donnees_recettes.previsions_definitives IS 'Previsions Definitives (calcule ou saisi)';
COMMENT ON COLUMN donnees_recettes.or_admis IS 'Ordre de Recette Admis';
COMMENT ON COLUMN donnees_recettes.recouvrement IS 'Montant recouvre';
COMMENT ON COLUMN donnees_recettes.reste_a_recouvrer IS 'Reste a Recouvrer (OR Admis - Recouvrement)';

CREATE INDEX idx_recettes_commune ON donnees_recettes(commune_id);
CREATE INDEX idx_recettes_exercice ON donnees_recettes(exercice_id);
CREATE INDEX idx_recettes_compte ON donnees_recettes(compte_code);
CREATE INDEX idx_recettes_commune_exercice ON donnees_recettes(commune_id, exercice_id);

-- Donnees DEPENSES par commune/exercice/compte
CREATE TABLE donnees_depenses (
    id SERIAL PRIMARY KEY,
    commune_id INTEGER NOT NULL REFERENCES communes(id) ON DELETE CASCADE,
    exercice_id INTEGER NOT NULL REFERENCES exercices(id) ON DELETE CASCADE,
    compte_code VARCHAR(10) NOT NULL REFERENCES plan_comptable(code) ON DELETE CASCADE,

    -- Colonnes financieres (en Ariary - MGA)
    budget_primitif DECIMAL(18, 2) DEFAULT 0,
    budget_additionnel DECIMAL(18, 2) DEFAULT 0,
    modifications DECIMAL(18, 2) DEFAULT 0,
    previsions_definitives DECIMAL(18, 2) DEFAULT 0,
    engagement DECIMAL(18, 2) DEFAULT 0,
    mandat_admis DECIMAL(18, 2) DEFAULT 0,
    paiement DECIMAL(18, 2) DEFAULT 0,
    reste_a_payer DECIMAL(18, 2) DEFAULT 0,

    -- Metadonnees
    programme VARCHAR(100),
    commentaire TEXT,
    valide BOOLEAN DEFAULT FALSE,
    valide_par INTEGER,
    valide_le TIMESTAMP,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT uk_depenses_commune_exercice_compte
        UNIQUE (commune_id, exercice_id, compte_code)
);

COMMENT ON TABLE donnees_depenses IS 'Donnees financieres des depenses par commune/exercice/compte';
COMMENT ON COLUMN donnees_depenses.budget_primitif IS 'Budget Primitif en Ariary';
COMMENT ON COLUMN donnees_depenses.budget_additionnel IS 'Budget Additionnel en Ariary';
COMMENT ON COLUMN donnees_depenses.modifications IS 'Modifications +/- en Ariary';
COMMENT ON COLUMN donnees_depenses.previsions_definitives IS 'Previsions Definitives';
COMMENT ON COLUMN donnees_depenses.engagement IS 'Montant engage';
COMMENT ON COLUMN donnees_depenses.mandat_admis IS 'Mandat Admis';
COMMENT ON COLUMN donnees_depenses.paiement IS 'Montant paye';
COMMENT ON COLUMN donnees_depenses.reste_a_payer IS 'Reste a Payer (Mandat - Paiement)';
COMMENT ON COLUMN donnees_depenses.programme IS 'Programme budgetaire associe';

CREATE INDEX idx_depenses_commune ON donnees_depenses(commune_id);
CREATE INDEX idx_depenses_exercice ON donnees_depenses(exercice_id);
CREATE INDEX idx_depenses_compte ON donnees_depenses(compte_code);
CREATE INDEX idx_depenses_commune_exercice ON donnees_depenses(commune_id, exercice_id);

-- =============================================================================
-- 4. TABLES PROJETS MINIERS
-- =============================================================================

-- Societes minieres
CREATE TABLE societes_minieres (
    id SERIAL PRIMARY KEY,
    nom VARCHAR(200) NOT NULL,
    nif VARCHAR(50),
    stat VARCHAR(50),
    siege_social VARCHAR(255),
    telephone VARCHAR(50),
    email VARCHAR(100),
    site_web VARCHAR(200),
    actif BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

COMMENT ON TABLE societes_minieres IS 'Societes minieres operant a Madagascar';
COMMENT ON COLUMN societes_minieres.nif IS 'Numero dIdentification Fiscale';
COMMENT ON COLUMN societes_minieres.stat IS 'Numero STAT (statistique)';

CREATE INDEX idx_societes_minieres_nom ON societes_minieres(nom);

-- Projets miniers
CREATE TABLE projets_miniers (
    id SERIAL PRIMARY KEY,
    nom VARCHAR(200) NOT NULL,
    societe_id INTEGER REFERENCES societes_minieres(id) ON DELETE SET NULL,
    type_minerai VARCHAR(100),
    statut VARCHAR(50) CHECK (statut IN ('exploration', 'exploitation', 'rehabilitation', 'ferme')),
    date_debut_exploitation DATE,
    surface_ha DECIMAL(12, 2),
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

COMMENT ON TABLE projets_miniers IS 'Projets dexploitation miniere';
COMMENT ON COLUMN projets_miniers.type_minerai IS 'Type de minerai exploite (Nickel, Cobalt, Ilmenite, etc.)';
COMMENT ON COLUMN projets_miniers.statut IS 'Statut du projet: exploration, exploitation, rehabilitation, ferme';
COMMENT ON COLUMN projets_miniers.surface_ha IS 'Surface du permis en hectares';

CREATE INDEX idx_projets_miniers_societe ON projets_miniers(societe_id);
CREATE INDEX idx_projets_miniers_statut ON projets_miniers(statut);

-- Relation N-N entre projets et communes
CREATE TABLE projets_communes (
    id SERIAL PRIMARY KEY,
    projet_id INTEGER NOT NULL REFERENCES projets_miniers(id) ON DELETE CASCADE,
    commune_id INTEGER NOT NULL REFERENCES communes(id) ON DELETE CASCADE,
    pourcentage_territoire DECIMAL(5, 2),
    date_debut DATE,
    date_fin DATE,
    CONSTRAINT uk_projet_commune UNIQUE (projet_id, commune_id)
);

COMMENT ON TABLE projets_communes IS 'Communes impactees par les projets miniers';
COMMENT ON COLUMN projets_communes.pourcentage_territoire IS 'Pourcentage du territoire communal concerne';

CREATE INDEX idx_projets_communes_projet ON projets_communes(projet_id);
CREATE INDEX idx_projets_communes_commune ON projets_communes(commune_id);

-- Revenus miniers specifiques
CREATE TABLE revenus_miniers (
    id SERIAL PRIMARY KEY,
    commune_id INTEGER NOT NULL REFERENCES communes(id) ON DELETE CASCADE,
    exercice_id INTEGER NOT NULL REFERENCES exercices(id) ON DELETE CASCADE,
    projet_id INTEGER REFERENCES projets_miniers(id) ON DELETE SET NULL,

    type_revenu VARCHAR(50) NOT NULL CHECK (type_revenu IN (
        'ristourne_miniere',
        'redevance_miniere',
        'frais_administration_miniere',
        'quote_part_ristourne',
        'autre'
    )),

    montant_prevu DECIMAL(18, 2) DEFAULT 0,
    montant_recu DECIMAL(18, 2) DEFAULT 0,
    date_reception DATE,
    reference_paiement VARCHAR(100),
    compte_code VARCHAR(10) REFERENCES plan_comptable(code),
    commentaire TEXT,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

COMMENT ON TABLE revenus_miniers IS 'Revenus miniers specifiques (ristournes, redevances)';
COMMENT ON COLUMN revenus_miniers.type_revenu IS 'Type de revenu minier';
COMMENT ON COLUMN revenus_miniers.compte_code IS 'Lien vers le plan comptable (7713 ou 7717 generalement)';

CREATE INDEX idx_revenus_miniers_commune ON revenus_miniers(commune_id);
CREATE INDEX idx_revenus_miniers_exercice ON revenus_miniers(exercice_id);
CREATE INDEX idx_revenus_miniers_projet ON revenus_miniers(projet_id);
CREATE INDEX idx_revenus_miniers_type ON revenus_miniers(type_revenu);

-- =============================================================================
-- 5. TABLES UTILISATEURS ET AUTHENTIFICATION
-- =============================================================================

-- Utilisateurs
CREATE TABLE utilisateurs (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    mot_de_passe_hash VARCHAR(255) NOT NULL,
    nom VARCHAR(100) NOT NULL,
    prenom VARCHAR(100),
    role role_utilisateur NOT NULL DEFAULT 'lecteur',
    commune_id INTEGER REFERENCES communes(id) ON DELETE SET NULL,
    actif BOOLEAN DEFAULT TRUE,
    email_verifie BOOLEAN DEFAULT FALSE,
    derniere_connexion TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

COMMENT ON TABLE utilisateurs IS 'Utilisateurs de la plateforme';
COMMENT ON COLUMN utilisateurs.role IS 'Role: admin, editeur, lecteur, commune';
COMMENT ON COLUMN utilisateurs.commune_id IS 'Si role=commune, utilisateur limite a cette commune';

CREATE INDEX idx_utilisateurs_email ON utilisateurs(email);
CREATE INDEX idx_utilisateurs_commune ON utilisateurs(commune_id);
CREATE INDEX idx_utilisateurs_role ON utilisateurs(role);

-- Ajout des references de validation
ALTER TABLE donnees_recettes
    ADD CONSTRAINT fk_recettes_valide_par
    FOREIGN KEY (valide_par) REFERENCES utilisateurs(id) ON DELETE SET NULL;

ALTER TABLE donnees_depenses
    ADD CONSTRAINT fk_depenses_valide_par
    FOREIGN KEY (valide_par) REFERENCES utilisateurs(id) ON DELETE SET NULL;

-- Sessions (pour JWT refresh tokens)
CREATE TABLE sessions (
    id SERIAL PRIMARY KEY,
    utilisateur_id INTEGER NOT NULL REFERENCES utilisateurs(id) ON DELETE CASCADE,
    refresh_token VARCHAR(500) NOT NULL,
    expires_at TIMESTAMP NOT NULL,
    ip_address VARCHAR(45),
    user_agent TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

COMMENT ON TABLE sessions IS 'Sessions utilisateurs et refresh tokens JWT';

CREATE INDEX idx_sessions_utilisateur ON sessions(utilisateur_id);
CREATE INDEX idx_sessions_token ON sessions(refresh_token);
CREATE INDEX idx_sessions_expires ON sessions(expires_at);

-- =============================================================================
-- 6. TABLES DOCUMENTS
-- =============================================================================

-- Documents attaches
CREATE TABLE documents (
    id SERIAL PRIMARY KEY,
    commune_id INTEGER REFERENCES communes(id) ON DELETE CASCADE,
    exercice_id INTEGER REFERENCES exercices(id) ON DELETE SET NULL,
    type_document type_document NOT NULL,
    titre VARCHAR(255) NOT NULL,
    description TEXT,
    nom_fichier VARCHAR(255) NOT NULL,
    chemin_fichier VARCHAR(500) NOT NULL,
    taille_octets BIGINT,
    mime_type VARCHAR(100),
    uploade_par INTEGER REFERENCES utilisateurs(id) ON DELETE SET NULL,
    nb_telechargements INTEGER DEFAULT 0,
    public BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

COMMENT ON TABLE documents IS 'Documents et pieces justificatives';
COMMENT ON COLUMN documents.type_document IS 'Type: compte_administratif, budget, piece_justificative, etc.';
COMMENT ON COLUMN documents.public IS 'Si true, visible par tous les visiteurs';

CREATE INDEX idx_documents_commune ON documents(commune_id);
CREATE INDEX idx_documents_exercice ON documents(exercice_id);
CREATE INDEX idx_documents_type ON documents(type_document);
CREATE INDEX idx_documents_public ON documents(public) WHERE public = TRUE;

-- =============================================================================
-- 7. TABLES NEWSLETTER ET STATISTIQUES
-- =============================================================================

-- Abonnes newsletter
CREATE TABLE newsletter_abonnes (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    nom VARCHAR(100),
    actif BOOLEAN DEFAULT TRUE,
    date_inscription TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    date_desinscription TIMESTAMP,
    token_desinscription VARCHAR(100) UNIQUE
);

COMMENT ON TABLE newsletter_abonnes IS 'Abonnes a la newsletter';

CREATE INDEX idx_newsletter_email ON newsletter_abonnes(email);
CREATE INDEX idx_newsletter_actif ON newsletter_abonnes(actif) WHERE actif = TRUE;

-- Statistiques de visites
CREATE TABLE statistiques_visites (
    id SERIAL PRIMARY KEY,
    date_visite DATE NOT NULL,
    page VARCHAR(255),
    commune_id INTEGER REFERENCES communes(id) ON DELETE SET NULL,
    nb_visites INTEGER DEFAULT 1,
    nb_telechargements INTEGER DEFAULT 0,
    ip_address VARCHAR(45),
    user_agent TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

COMMENT ON TABLE statistiques_visites IS 'Statistiques de visites pour le back-office';

CREATE INDEX idx_stats_date ON statistiques_visites(date_visite);
CREATE INDEX idx_stats_commune ON statistiques_visites(commune_id);
CREATE INDEX idx_stats_page ON statistiques_visites(page);

-- =============================================================================
-- 8. TABLE AUDIT LOG
-- =============================================================================

-- Historique des modifications (audit trail)
CREATE TABLE audit_log (
    id SERIAL PRIMARY KEY,
    table_name VARCHAR(100) NOT NULL,
    record_id INTEGER NOT NULL,
    action VARCHAR(20) NOT NULL CHECK (action IN ('INSERT', 'UPDATE', 'DELETE')),
    old_values JSONB,
    new_values JSONB,
    utilisateur_id INTEGER REFERENCES utilisateurs(id) ON DELETE SET NULL,
    ip_address VARCHAR(45),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

COMMENT ON TABLE audit_log IS 'Journal daudit des modifications';
COMMENT ON COLUMN audit_log.old_values IS 'Anciennes valeurs en JSON';
COMMENT ON COLUMN audit_log.new_values IS 'Nouvelles valeurs en JSON';

CREATE INDEX idx_audit_table ON audit_log(table_name);
CREATE INDEX idx_audit_record ON audit_log(table_name, record_id);
CREATE INDEX idx_audit_date ON audit_log(created_at);
CREATE INDEX idx_audit_utilisateur ON audit_log(utilisateur_id);

-- =============================================================================
-- 9. VUES POUR GENERATION DES TABLEAUX EXCEL
-- =============================================================================

-- Vue pour le tableau des RECETTES (reproduit la structure Excel)
CREATE VIEW vue_tableau_recettes AS
SELECT
    c.id AS commune_id,
    c.code AS commune_code,
    c.nom AS commune_nom,
    r.nom AS region_nom,
    e.id AS exercice_id,
    e.annee AS exercice,
    pc.code AS compte,
    pc.intitule,
    pc.niveau,
    pc.section,
    pc.parent_code,
    pc.ordre_affichage,
    COALESCE(dr.budget_primitif, 0) AS budget_primitif,
    COALESCE(dr.budget_additionnel, 0) AS budget_additionnel,
    COALESCE(dr.modifications, 0) AS modifications,
    COALESCE(
        dr.previsions_definitives,
        dr.budget_primitif + dr.budget_additionnel + dr.modifications
    ) AS previsions_definitives,
    COALESCE(dr.or_admis, 0) AS or_admis,
    COALESCE(dr.recouvrement, 0) AS recouvrement,
    COALESCE(dr.or_admis, 0) - COALESCE(dr.recouvrement, 0) AS reste_a_recouvrer,
    CASE
        WHEN COALESCE(dr.previsions_definitives, dr.budget_primitif + dr.budget_additionnel + dr.modifications) > 0
        THEN ROUND(
            COALESCE(dr.or_admis, 0)::NUMERIC /
            COALESCE(dr.previsions_definitives, dr.budget_primitif + dr.budget_additionnel + dr.modifications)::NUMERIC * 100,
            2
        )
        ELSE 0
    END AS taux_execution
FROM plan_comptable pc
CROSS JOIN communes c
INNER JOIN regions r ON c.region_id = r.id
CROSS JOIN exercices e
LEFT JOIN donnees_recettes dr
    ON dr.commune_id = c.id
    AND dr.exercice_id = e.id
    AND dr.compte_code = pc.code
WHERE pc.type_mouvement = 'recette'
  AND pc.actif = TRUE;

COMMENT ON VIEW vue_tableau_recettes IS 'Vue pour generer le tableau des recettes (feuille RECETTE Excel)';

-- Vue pour le tableau des DEPENSES (reproduit la structure Excel)
CREATE VIEW vue_tableau_depenses AS
SELECT
    c.id AS commune_id,
    c.code AS commune_code,
    c.nom AS commune_nom,
    r.nom AS region_nom,
    e.id AS exercice_id,
    e.annee AS exercice,
    pc.code AS compte,
    pc.intitule,
    pc.niveau,
    pc.section,
    pc.parent_code,
    pc.ordre_affichage,
    dd.programme,
    COALESCE(dd.budget_primitif, 0) AS budget_primitif,
    COALESCE(dd.budget_additionnel, 0) AS budget_additionnel,
    COALESCE(dd.modifications, 0) AS modifications,
    COALESCE(
        dd.previsions_definitives,
        dd.budget_primitif + dd.budget_additionnel + dd.modifications
    ) AS previsions_definitives,
    COALESCE(dd.engagement, 0) AS engagement,
    COALESCE(dd.mandat_admis, 0) AS mandat_admis,
    COALESCE(dd.paiement, 0) AS paiement,
    COALESCE(dd.mandat_admis, 0) - COALESCE(dd.paiement, 0) AS reste_a_payer,
    CASE
        WHEN COALESCE(dd.previsions_definitives, dd.budget_primitif + dd.budget_additionnel + dd.modifications) > 0
        THEN ROUND(
            COALESCE(dd.mandat_admis, 0)::NUMERIC /
            COALESCE(dd.previsions_definitives, dd.budget_primitif + dd.budget_additionnel + dd.modifications)::NUMERIC * 100,
            2
        )
        ELSE 0
    END AS taux_execution
FROM plan_comptable pc
CROSS JOIN communes c
INNER JOIN regions r ON c.region_id = r.id
CROSS JOIN exercices e
LEFT JOIN donnees_depenses dd
    ON dd.commune_id = c.id
    AND dd.exercice_id = e.id
    AND dd.compte_code = pc.code
WHERE pc.type_mouvement = 'depense'
  AND pc.actif = TRUE;

COMMENT ON VIEW vue_tableau_depenses IS 'Vue pour generer le tableau des depenses (feuille DEPENSES Excel)';

-- Vue pour le tableau d'EQUILIBRE (synthese)
CREATE VIEW vue_tableau_equilibre AS
SELECT
    c.id AS commune_id,
    c.code AS commune_code,
    c.nom AS commune_nom,
    r.nom AS region_nom,
    e.id AS exercice_id,
    e.annee AS exercice,

    -- DEPENSES FONCTIONNEMENT
    COALESCE(SUM(CASE
        WHEN pc.type_mouvement = 'depense' AND pc.section = 'fonctionnement' AND pc.niveau = 1
        THEN dd.mandat_admis ELSE 0
    END), 0) AS depenses_fonct_mandat,
    COALESCE(SUM(CASE
        WHEN pc.type_mouvement = 'depense' AND pc.section = 'fonctionnement' AND pc.niveau = 1
        THEN dd.paiement ELSE 0
    END), 0) AS depenses_fonct_paiement,

    -- DEPENSES INVESTISSEMENT
    COALESCE(SUM(CASE
        WHEN pc.type_mouvement = 'depense' AND pc.section = 'investissement' AND pc.niveau = 1
        THEN dd.mandat_admis ELSE 0
    END), 0) AS depenses_invest_mandat,
    COALESCE(SUM(CASE
        WHEN pc.type_mouvement = 'depense' AND pc.section = 'investissement' AND pc.niveau = 1
        THEN dd.paiement ELSE 0
    END), 0) AS depenses_invest_paiement,

    -- RECETTES FONCTIONNEMENT
    COALESCE(SUM(CASE
        WHEN pc.type_mouvement = 'recette' AND pc.section = 'fonctionnement' AND pc.niveau = 1
        THEN dr.or_admis ELSE 0
    END), 0) AS recettes_fonct_or,
    COALESCE(SUM(CASE
        WHEN pc.type_mouvement = 'recette' AND pc.section = 'fonctionnement' AND pc.niveau = 1
        THEN dr.recouvrement ELSE 0
    END), 0) AS recettes_fonct_recouvrement,

    -- RECETTES INVESTISSEMENT
    COALESCE(SUM(CASE
        WHEN pc.type_mouvement = 'recette' AND pc.section = 'investissement' AND pc.niveau = 1
        THEN dr.or_admis ELSE 0
    END), 0) AS recettes_invest_or,
    COALESCE(SUM(CASE
        WHEN pc.type_mouvement = 'recette' AND pc.section = 'investissement' AND pc.niveau = 1
        THEN dr.recouvrement ELSE 0
    END), 0) AS recettes_invest_recouvrement

FROM communes c
INNER JOIN regions r ON c.region_id = r.id
CROSS JOIN exercices e
LEFT JOIN plan_comptable pc ON pc.niveau = 1 AND pc.actif = TRUE
LEFT JOIN donnees_depenses dd
    ON dd.commune_id = c.id AND dd.exercice_id = e.id AND dd.compte_code = pc.code
LEFT JOIN donnees_recettes dr
    ON dr.commune_id = c.id AND dr.exercice_id = e.id AND dr.compte_code = pc.code
GROUP BY c.id, c.code, c.nom, r.nom, e.id, e.annee;

COMMENT ON VIEW vue_tableau_equilibre IS 'Vue pour generer le tableau dequilibre (feuille EQUILIBRE Excel)';

-- =============================================================================
-- 10. FONCTIONS UTILITAIRES
-- =============================================================================

-- Fonction pour mettre a jour le timestamp updated_at
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Application des triggers de mise a jour automatique
CREATE TRIGGER update_provinces_updated_at
    BEFORE UPDATE ON provinces
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_regions_updated_at
    BEFORE UPDATE ON regions
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_communes_updated_at
    BEFORE UPDATE ON communes
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_plan_comptable_updated_at
    BEFORE UPDATE ON plan_comptable
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_exercices_updated_at
    BEFORE UPDATE ON exercices
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_donnees_recettes_updated_at
    BEFORE UPDATE ON donnees_recettes
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_donnees_depenses_updated_at
    BEFORE UPDATE ON donnees_depenses
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_societes_minieres_updated_at
    BEFORE UPDATE ON societes_minieres
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_projets_miniers_updated_at
    BEFORE UPDATE ON projets_miniers
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_revenus_miniers_updated_at
    BEFORE UPDATE ON revenus_miniers
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_utilisateurs_updated_at
    BEFORE UPDATE ON utilisateurs
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_documents_updated_at
    BEFORE UPDATE ON documents
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- =============================================================================
-- FIN DU SCHEMA
-- =============================================================================
