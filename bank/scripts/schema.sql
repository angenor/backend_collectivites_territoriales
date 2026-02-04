-- =============================================================================
-- SCHEMA DE BASE DE DONNEES POSTGRESQL
-- Plateforme de Suivi des Revenus Miniers des Collectivites Territoriales
-- Version: 2.0
-- Date: 2025-12-01
-- Mise a jour: Ajout systeme CMS pour pages compte administratif
-- =============================================================================

-- Suppression des tables existantes (dans l'ordre inverse des dependances)
DROP VIEW IF EXISTS vue_tableau_equilibre CASCADE;
DROP VIEW IF EXISTS vue_tableau_depenses CASCADE;
DROP VIEW IF EXISTS vue_tableau_recettes CASCADE;

-- Tables CMS (nouvelles)
DROP TABLE IF EXISTS liens_utiles CASCADE;
DROP TABLE IF EXISTS photos_galerie CASCADE;
DROP TABLE IF EXISTS cartes_informatives CASCADE;
DROP TABLE IF EXISTS blocs_carte_fond CASCADE;
DROP TABLE IF EXISTS blocs_image_texte CASCADE;
DROP TABLE IF EXISTS contenus_editorjs CASCADE;
DROP TABLE IF EXISTS sections_cms CASCADE;
DROP TABLE IF EXISTS pages_compte_administratif CASCADE;

DROP TABLE IF EXISTS audit_log CASCADE;
DROP TABLE IF EXISTS statistiques_visites CASCADE;
DROP TABLE IF EXISTS newsletter_abonnes CASCADE;
DROP TABLE IF EXISTS documents CASCADE;
DROP TABLE IF EXISTS sessions CASCADE;
DROP TABLE IF EXISTS revenus_miniers CASCADE;
DROP TABLE IF EXISTS projets_communes CASCADE;
DROP TABLE IF EXISTS projets_miniers CASCADE;
DROP TABLE IF EXISTS societes_minieres CASCADE;
DROP TABLE IF EXISTS comptes_administratifs CASCADE;
DROP TABLE IF EXISTS donnees_depenses CASCADE;
DROP TABLE IF EXISTS donnees_recettes CASCADE;
DROP TABLE IF EXISTS exercices CASCADE;
DROP TABLE IF EXISTS plan_comptable CASCADE;
DROP TABLE IF EXISTS utilisateurs CASCADE;
DROP TABLE IF EXISTS communes CASCADE;
DROP TABLE IF EXISTS regions CASCADE;
DROP TABLE IF EXISTS provinces CASCADE;

DROP TYPE IF EXISTS type_section_cms CASCADE;
DROP TYPE IF EXISTS statut_publication CASCADE;
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

-- Statut de publication CMS
CREATE TYPE statut_publication AS ENUM ('brouillon', 'publie', 'archive');

-- Types de sections CMS pour les pages compte administratif
CREATE TYPE type_section_cms AS ENUM (
    'editorjs',              -- Texte enrichi EditorJS (obligatoire)
    'bloc_image_gauche',     -- Image a gauche + contenu a droite
    'bloc_image_droite',     -- Image a droite + contenu a gauche
    'carte_fond_image',      -- Carte avec image de fond et contenu superpose
    'grille_cartes',         -- Grille de cartes informatives
    'galerie_photos',        -- Galerie de photos
    'note_informative',      -- Note informative
    'liens_utiles',          -- Section liens utiles
    'tableau_financier',     -- Tableau financier integre (obligatoire)
    'graphiques_analytiques' -- Section graphiques analytiques
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

-- Comptes administratifs (enregistrement commune/exercice)
-- Note: la FK created_by -> utilisateurs est ajoutee apres creation de la table utilisateurs
CREATE TABLE comptes_administratifs (
    id SERIAL PRIMARY KEY,
    commune_id INTEGER NOT NULL REFERENCES communes(id) ON DELETE CASCADE,
    exercice_id INTEGER NOT NULL REFERENCES exercices(id) ON DELETE CASCADE,
    notes TEXT,
    created_by INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT uk_compte_administratif_commune_exercice UNIQUE (commune_id, exercice_id)
);

COMMENT ON TABLE comptes_administratifs IS 'Comptes administratifs enregistres (paire commune/exercice)';
COMMENT ON COLUMN comptes_administratifs.notes IS 'Notes optionnelles sur le compte administratif';
COMMENT ON COLUMN comptes_administratifs.created_by IS 'Utilisateur ayant cree le compte';

CREATE INDEX idx_compte_admin_commune ON comptes_administratifs(commune_id);
CREATE INDEX idx_compte_admin_exercice ON comptes_administratifs(exercice_id);

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

-- Ajout de la FK comptes_administratifs.created_by -> utilisateurs
-- (definie ici car utilisateurs est cree apres comptes_administratifs)
ALTER TABLE comptes_administratifs
    ADD CONSTRAINT fk_compte_admin_created_by
    FOREIGN KEY (created_by) REFERENCES utilisateurs(id) ON DELETE SET NULL;

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
-- 7. SYSTEME CMS - PAGES COMPTE ADMINISTRATIF
-- =============================================================================

-- Table principale des pages compte administratif
-- Une page par commune/exercice avec contenu editorialise
CREATE TABLE pages_compte_administratif (
    id SERIAL PRIMARY KEY,
    commune_id INTEGER NOT NULL REFERENCES communes(id) ON DELETE CASCADE,
    exercice_id INTEGER NOT NULL REFERENCES exercices(id) ON DELETE CASCADE,

    -- Metadonnees de la page
    titre VARCHAR(255),
    sous_titre VARCHAR(500),
    meta_description TEXT,
    image_hero_url VARCHAR(500),

    -- Statut et publication
    statut statut_publication NOT NULL DEFAULT 'brouillon',
    date_publication TIMESTAMP,
    date_mise_a_jour TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    -- Options d'affichage
    afficher_tableau_financier BOOLEAN DEFAULT TRUE,
    afficher_graphiques BOOLEAN DEFAULT TRUE,

    -- Audit
    cree_par INTEGER REFERENCES utilisateurs(id) ON DELETE SET NULL,
    modifie_par INTEGER REFERENCES utilisateurs(id) ON DELETE SET NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT uk_page_commune_exercice UNIQUE (commune_id, exercice_id)
);

COMMENT ON TABLE pages_compte_administratif IS 'Pages CMS pour afficher les comptes administratifs avec contenu editorialise';
COMMENT ON COLUMN pages_compte_administratif.statut IS 'brouillon, publie, ou archive';
COMMENT ON COLUMN pages_compte_administratif.image_hero_url IS 'URL de limage hero en haut de page';

CREATE INDEX idx_pages_ca_commune ON pages_compte_administratif(commune_id);
CREATE INDEX idx_pages_ca_exercice ON pages_compte_administratif(exercice_id);
CREATE INDEX idx_pages_ca_statut ON pages_compte_administratif(statut);
CREATE INDEX idx_pages_ca_publie ON pages_compte_administratif(statut, date_publication) WHERE statut = 'publie';

-- Sections CMS avec ordre et visibilite
CREATE TABLE sections_cms (
    id SERIAL PRIMARY KEY,
    page_id INTEGER NOT NULL REFERENCES pages_compte_administratif(id) ON DELETE CASCADE,

    -- Type et identification
    type_section type_section_cms NOT NULL,
    titre VARCHAR(255),

    -- Ordre et positionnement
    ordre INTEGER NOT NULL DEFAULT 0,

    -- Visibilite
    visible BOOLEAN DEFAULT TRUE,
    visible_accueil BOOLEAN DEFAULT FALSE,

    -- Configuration JSON pour options specifiques au type
    config JSONB DEFAULT '{}',

    -- Metadonnees
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

COMMENT ON TABLE sections_cms IS 'Sections de contenu pour les pages compte administratif';
COMMENT ON COLUMN sections_cms.type_section IS 'Type de section: editorjs, bloc_image_gauche, grille_cartes, etc.';
COMMENT ON COLUMN sections_cms.ordre IS 'Ordre daffichage de la section (0 = premier)';
COMMENT ON COLUMN sections_cms.visible IS 'Si true, la section est visible sur la page detail';
COMMENT ON COLUMN sections_cms.visible_accueil IS 'Si true, la section peut apparaitre sur la page daccueil';
COMMENT ON COLUMN sections_cms.config IS 'Options de configuration specifiques au type (couleurs, disposition, etc.)';

CREATE INDEX idx_sections_cms_page ON sections_cms(page_id);
CREATE INDEX idx_sections_cms_ordre ON sections_cms(page_id, ordre);
CREATE INDEX idx_sections_cms_type ON sections_cms(type_section);
CREATE INDEX idx_sections_cms_visible ON sections_cms(page_id, visible) WHERE visible = TRUE;
CREATE INDEX idx_sections_cms_accueil ON sections_cms(visible_accueil) WHERE visible_accueil = TRUE;

-- Contenu EditorJS (texte enrichi)
CREATE TABLE contenus_editorjs (
    id SERIAL PRIMARY KEY,
    section_id INTEGER NOT NULL REFERENCES sections_cms(id) ON DELETE CASCADE,

    -- Contenu EditorJS stocke en JSON
    contenu JSONB NOT NULL,

    -- Version pour historique
    version INTEGER DEFAULT 1,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT uk_editorjs_section UNIQUE (section_id)
);

COMMENT ON TABLE contenus_editorjs IS 'Contenu texte enrichi au format EditorJS';
COMMENT ON COLUMN contenus_editorjs.contenu IS 'Structure JSON EditorJS avec blocks (paragraph, header, list, image, etc.)';

CREATE INDEX idx_editorjs_section ON contenus_editorjs(section_id);

-- Blocs Image + Texte (gauche ou droite)
CREATE TABLE blocs_image_texte (
    id SERIAL PRIMARY KEY,
    section_id INTEGER NOT NULL REFERENCES sections_cms(id) ON DELETE CASCADE,

    -- Contenu
    titre VARCHAR(255),
    sous_titre VARCHAR(255),
    contenu TEXT,
    contenu_html TEXT,

    -- Image
    image_url VARCHAR(500) NOT NULL,
    image_alt VARCHAR(255),
    legende_image VARCHAR(500),

    -- Liens/Boutons (stockes en JSON array)
    boutons JSONB DEFAULT '[]',

    -- Note de bas
    note TEXT,
    note_source VARCHAR(255),

    -- Style
    couleur_fond VARCHAR(50),
    icone_titre VARCHAR(50),

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT uk_bloc_image_section UNIQUE (section_id)
);

COMMENT ON TABLE blocs_image_texte IS 'Blocs avec image (gauche ou droite) et contenu texte';
COMMENT ON COLUMN blocs_image_texte.boutons IS 'Array JSON de boutons: [{label, url, style, icon}]';
COMMENT ON COLUMN blocs_image_texte.couleur_fond IS 'Classe Tailwind ou code couleur pour le fond';

CREATE INDEX idx_blocs_image_section ON blocs_image_texte(section_id);

-- Cartes avec image de fond et contenu superpose
CREATE TABLE blocs_carte_fond (
    id SERIAL PRIMARY KEY,
    section_id INTEGER NOT NULL REFERENCES sections_cms(id) ON DELETE CASCADE,

    -- Image de fond
    image_url VARCHAR(500) NOT NULL,
    image_alt VARCHAR(255),

    -- Contenu superpose
    badge_texte VARCHAR(100),
    badge_icone VARCHAR(50),
    titre VARCHAR(255),
    contenu TEXT,

    -- Boutons (JSON array)
    boutons JSONB DEFAULT '[]',

    -- Style
    hauteur_min INTEGER DEFAULT 400,
    opacite_overlay INTEGER DEFAULT 50,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT uk_carte_fond_section UNIQUE (section_id)
);

COMMENT ON TABLE blocs_carte_fond IS 'Cartes plein ecran avec image de fond et contenu superpose';
COMMENT ON COLUMN blocs_carte_fond.opacite_overlay IS 'Opacite du gradient overlay (0-100)';

CREATE INDEX idx_carte_fond_section ON blocs_carte_fond(section_id);

-- Cartes informatives pour les grilles
CREATE TABLE cartes_informatives (
    id SERIAL PRIMARY KEY,
    section_id INTEGER NOT NULL REFERENCES sections_cms(id) ON DELETE CASCADE,

    -- Ordre dans la grille
    ordre INTEGER NOT NULL DEFAULT 0,

    -- Type de carte: image ou statistique
    type_carte VARCHAR(20) CHECK (type_carte IN ('image', 'statistique', 'icone')) DEFAULT 'image',

    -- Contenu image (si type = image)
    image_url VARCHAR(500),
    image_alt VARCHAR(255),

    -- Contenu statistique (si type = statistique)
    stat_valeur VARCHAR(50),
    stat_unite VARCHAR(50),
    stat_evolution VARCHAR(50),
    stat_icone VARCHAR(50),

    -- Badge
    badge_texte VARCHAR(100),
    badge_icone VARCHAR(50),
    badge_couleur VARCHAR(50),

    -- Texte
    titre VARCHAR(255),
    description TEXT,

    -- Lien
    lien_texte VARCHAR(100),
    lien_url VARCHAR(500),

    -- Note de bas
    note VARCHAR(255),

    -- Style
    couleur_fond VARCHAR(50),
    couleur_gradient_debut VARCHAR(50),
    couleur_gradient_fin VARCHAR(50),

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

COMMENT ON TABLE cartes_informatives IS 'Cartes pour les grilles (3 colonnes typiquement)';
COMMENT ON COLUMN cartes_informatives.type_carte IS 'image: avec photo, statistique: avec chiffre et evolution, icone: avec icone';

CREATE INDEX idx_cartes_info_section ON cartes_informatives(section_id);
CREATE INDEX idx_cartes_info_ordre ON cartes_informatives(section_id, ordre);

-- Photos pour les galeries
CREATE TABLE photos_galerie (
    id SERIAL PRIMARY KEY,
    section_id INTEGER NOT NULL REFERENCES sections_cms(id) ON DELETE CASCADE,

    -- Ordre dans la galerie
    ordre INTEGER NOT NULL DEFAULT 0,

    -- Image
    image_url VARCHAR(500) NOT NULL,
    image_alt VARCHAR(255),
    image_thumbnail_url VARCHAR(500),

    -- Texte
    titre VARCHAR(255),
    description VARCHAR(500),

    -- Metadonnees optionnelles
    date_prise DATE,
    lieu VARCHAR(255),
    credit_photo VARCHAR(255),

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

COMMENT ON TABLE photos_galerie IS 'Photos pour les galeries dimages';

CREATE INDEX idx_photos_galerie_section ON photos_galerie(section_id);
CREATE INDEX idx_photos_galerie_ordre ON photos_galerie(section_id, ordre);

-- Liens utiles
CREATE TABLE liens_utiles (
    id SERIAL PRIMARY KEY,
    section_id INTEGER NOT NULL REFERENCES sections_cms(id) ON DELETE CASCADE,

    -- Ordre
    ordre INTEGER NOT NULL DEFAULT 0,

    -- Contenu
    titre VARCHAR(255) NOT NULL,
    description VARCHAR(500),
    url VARCHAR(500) NOT NULL,

    -- Style
    icone VARCHAR(50),
    couleur VARCHAR(50),
    couleur_fond VARCHAR(50),

    -- Options
    ouvrir_nouvel_onglet BOOLEAN DEFAULT TRUE,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

COMMENT ON TABLE liens_utiles IS 'Liens utiles et documentation';

CREATE INDEX idx_liens_utiles_section ON liens_utiles(section_id);
CREATE INDEX idx_liens_utiles_ordre ON liens_utiles(section_id, ordre);

-- =============================================================================
-- 8. TABLES NEWSLETTER ET STATISTIQUES
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

CREATE TRIGGER update_comptes_administratifs_updated_at
    BEFORE UPDATE ON comptes_administratifs
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

-- Triggers CMS
CREATE TRIGGER update_pages_ca_updated_at
    BEFORE UPDATE ON pages_compte_administratif
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_sections_cms_updated_at
    BEFORE UPDATE ON sections_cms
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_contenus_editorjs_updated_at
    BEFORE UPDATE ON contenus_editorjs
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_blocs_image_texte_updated_at
    BEFORE UPDATE ON blocs_image_texte
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_blocs_carte_fond_updated_at
    BEFORE UPDATE ON blocs_carte_fond
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_cartes_informatives_updated_at
    BEFORE UPDATE ON cartes_informatives
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_photos_galerie_updated_at
    BEFORE UPDATE ON photos_galerie
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_liens_utiles_updated_at
    BEFORE UPDATE ON liens_utiles
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- =============================================================================
-- 12. VUE POUR RECUPERER LES SECTIONS CMS D'UNE PAGE
-- =============================================================================

-- Vue complete des pages compte administratif avec leurs sections
CREATE VIEW vue_page_compte_administratif AS
SELECT
    pca.id AS page_id,
    pca.commune_id,
    c.code AS commune_code,
    c.nom AS commune_nom,
    r.nom AS region_nom,
    p.nom AS province_nom,
    c.population,
    pca.exercice_id,
    e.annee AS exercice_annee,
    pca.titre AS page_titre,
    pca.sous_titre AS page_sous_titre,
    pca.image_hero_url,
    pca.statut,
    pca.date_publication,
    pca.date_mise_a_jour,
    pca.afficher_tableau_financier,
    pca.afficher_graphiques,
    (
        SELECT COUNT(*)
        FROM sections_cms s
        WHERE s.page_id = pca.id AND s.visible = TRUE
    ) AS nb_sections_visibles,
    (
        SELECT COUNT(*)
        FROM sections_cms s
        WHERE s.page_id = pca.id AND s.visible_accueil = TRUE
    ) AS nb_sections_accueil
FROM pages_compte_administratif pca
INNER JOIN communes c ON pca.commune_id = c.id
INNER JOIN regions r ON c.region_id = r.id
INNER JOIN provinces p ON r.province_id = p.id
INNER JOIN exercices e ON pca.exercice_id = e.id;

COMMENT ON VIEW vue_page_compte_administratif IS 'Vue complete des pages compte administratif avec informations geographiques';

-- Vue des sections ordonnees avec leur contenu
CREATE VIEW vue_sections_cms_detaillees AS
SELECT
    s.id AS section_id,
    s.page_id,
    pca.commune_id,
    pca.exercice_id,
    s.type_section,
    s.titre AS section_titre,
    s.ordre,
    s.visible,
    s.visible_accueil,
    s.config,
    -- Contenu EditorJS
    cej.contenu AS editorjs_contenu,
    -- Bloc Image Texte
    bit.titre AS bloc_titre,
    bit.contenu AS bloc_contenu,
    bit.image_url AS bloc_image_url,
    bit.boutons AS bloc_boutons,
    -- Carte Fond
    bcf.image_url AS carte_fond_image_url,
    bcf.titre AS carte_fond_titre,
    bcf.contenu AS carte_fond_contenu,
    -- Nombre d'elements enfants
    (SELECT COUNT(*) FROM cartes_informatives ci WHERE ci.section_id = s.id) AS nb_cartes,
    (SELECT COUNT(*) FROM photos_galerie pg WHERE pg.section_id = s.id) AS nb_photos,
    (SELECT COUNT(*) FROM liens_utiles lu WHERE lu.section_id = s.id) AS nb_liens
FROM sections_cms s
INNER JOIN pages_compte_administratif pca ON s.page_id = pca.id
LEFT JOIN contenus_editorjs cej ON cej.section_id = s.id
LEFT JOIN blocs_image_texte bit ON bit.section_id = s.id
LEFT JOIN blocs_carte_fond bcf ON bcf.section_id = s.id
ORDER BY s.page_id, s.ordre;

COMMENT ON VIEW vue_sections_cms_detaillees IS 'Vue des sections CMS avec contenu et compteurs';

-- =============================================================================
-- FIN DU SCHEMA
-- =============================================================================
