-- ============================================================================
-- MODÈLE DE DONNÉES - PLATEFORME DE SUIVI DES REVENUS MINIERS
-- Base de données: PostgreSQL
-- ============================================================================

-- Extension pour UUID
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- ============================================================================
-- TABLES DE RÉFÉRENCE GÉOGRAPHIQUE
-- ============================================================================

-- Table des régions
CREATE TABLE regions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    code VARCHAR(10) UNIQUE NOT NULL,
    nom VARCHAR(255) NOT NULL,
    description TEXT,
    actif BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table des départements/districts
CREATE TABLE departements (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    code VARCHAR(10) UNIQUE NOT NULL,
    nom VARCHAR(255) NOT NULL,
    region_id UUID NOT NULL REFERENCES regions(id) ON DELETE CASCADE,
    description TEXT,
    actif BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table des communes
CREATE TABLE communes (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    code VARCHAR(10) UNIQUE NOT NULL,
    nom VARCHAR(255) NOT NULL,
    departement_id UUID NOT NULL REFERENCES departements(id) ON DELETE CASCADE,
    region_id UUID NOT NULL REFERENCES regions(id) ON DELETE CASCADE,
    population INTEGER,
    superficie DECIMAL(10, 2),
    description TEXT,
    actif BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================================
-- TABLES DES PROJETS MINIERS
-- ============================================================================

-- Table des types de minerais
CREATE TABLE types_minerais (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    code VARCHAR(50) UNIQUE NOT NULL,
    nom VARCHAR(255) NOT NULL,
    description TEXT,
    actif BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table des sociétés minières
CREATE TABLE societes_minieres (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    code VARCHAR(50) UNIQUE NOT NULL,
    nom VARCHAR(255) NOT NULL,
    raison_sociale VARCHAR(255),
    nif VARCHAR(50),
    stat VARCHAR(50),
    adresse TEXT,
    telephone VARCHAR(50),
    email VARCHAR(255),
    actif BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table des projets miniers
CREATE TABLE projets_miniers (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    code VARCHAR(50) UNIQUE NOT NULL,
    nom VARCHAR(255) NOT NULL,
    societe_miniere_id UUID NOT NULL REFERENCES societes_minieres(id) ON DELETE CASCADE,
    type_minerai_id UUID NOT NULL REFERENCES types_minerais(id) ON DELETE RESTRICT,
    commune_id UUID NOT NULL REFERENCES communes(id) ON DELETE CASCADE,
    date_debut DATE,
    date_fin DATE,
    statut VARCHAR(50) DEFAULT 'actif', -- actif, suspendu, terminé
    description TEXT,
    actif BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================================
-- TABLES DE GESTION DES REVENUS
-- ============================================================================

-- Table des exercices fiscaux
CREATE TABLE exercices (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    annee INTEGER UNIQUE NOT NULL,
    date_debut DATE NOT NULL,
    date_fin DATE NOT NULL,
    statut VARCHAR(50) DEFAULT 'ouvert', -- ouvert, cloturé
    actif BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table des périodes (trimestre, semestre, etc.)
CREATE TABLE periodes (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    code VARCHAR(50) NOT NULL,
    nom VARCHAR(255) NOT NULL,
    exercice_id UUID NOT NULL REFERENCES exercices(id) ON DELETE CASCADE,
    date_debut DATE NOT NULL,
    date_fin DATE NOT NULL,
    type_periode VARCHAR(50), -- mensuel, trimestriel, semestriel, annuel
    ordre INTEGER, -- Pour l'affichage ordonné
    actif BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(exercice_id, code)
);

-- Table des catégories de rubriques
CREATE TABLE categories_rubriques (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    code VARCHAR(50) UNIQUE NOT NULL,
    nom VARCHAR(255) NOT NULL,
    description TEXT,
    ordre INTEGER,
    actif BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table des rubriques (lignes du tableau)
CREATE TABLE rubriques (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    code VARCHAR(50) UNIQUE NOT NULL,
    nom VARCHAR(255) NOT NULL,
    categorie_id UUID REFERENCES categories_rubriques(id) ON DELETE SET NULL,
    parent_id UUID REFERENCES rubriques(id) ON DELETE CASCADE, -- Pour la hiérarchie
    niveau INTEGER DEFAULT 1, -- Niveau dans la hiérarchie
    ordre INTEGER, -- Pour l'affichage ordonné
    type VARCHAR(50), -- recette, depense, solde, autre
    formule TEXT, -- Formule de calcul si applicable (JSON)
    est_calculee BOOLEAN DEFAULT FALSE,
    afficher_total BOOLEAN DEFAULT TRUE,
    description TEXT,
    actif BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table des données de revenus (cœur du système)
CREATE TABLE revenus (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    commune_id UUID NOT NULL REFERENCES communes(id) ON DELETE CASCADE,
    rubrique_id UUID NOT NULL REFERENCES rubriques(id) ON DELETE CASCADE,
    periode_id UUID NOT NULL REFERENCES periodes(id) ON DELETE CASCADE,
    projet_minier_id UUID REFERENCES projets_miniers(id) ON DELETE SET NULL,
    montant DECIMAL(15, 2) NOT NULL DEFAULT 0,
    montant_prevu DECIMAL(15, 2), -- Budget prévisionnel
    ecart DECIMAL(15, 2), -- Écart entre prévu et réalisé
    taux_realisation DECIMAL(5, 2), -- Pourcentage de réalisation
    observations TEXT,
    documents JSONB, -- Références aux documents justificatifs
    valide BOOLEAN DEFAULT FALSE,
    valide_par UUID, -- Référence à l'utilisateur
    valide_le TIMESTAMP,
    created_by UUID, -- Référence à l'utilisateur
    updated_by UUID, -- Référence à l'utilisateur
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(commune_id, rubrique_id, periode_id, projet_minier_id)
);

-- Index pour améliorer les performances
CREATE INDEX idx_revenus_commune ON revenus(commune_id);
CREATE INDEX idx_revenus_rubrique ON revenus(rubrique_id);
CREATE INDEX idx_revenus_periode ON revenus(periode_id);
CREATE INDEX idx_revenus_projet ON revenus(projet_minier_id);

-- ============================================================================
-- TABLES DE CONFIGURATION DYNAMIQUE
-- ============================================================================

-- Table des colonnes personnalisées (pour extensibilité)
CREATE TABLE colonnes_personnalisees (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    code VARCHAR(50) UNIQUE NOT NULL,
    nom VARCHAR(255) NOT NULL,
    type_donnee VARCHAR(50), -- text, number, date, boolean, json
    ordre INTEGER,
    obligatoire BOOLEAN DEFAULT FALSE,
    visible BOOLEAN DEFAULT TRUE,
    editable BOOLEAN DEFAULT TRUE,
    valeur_defaut TEXT,
    actif BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table des valeurs pour colonnes personnalisées
CREATE TABLE valeurs_colonnes_personnalisees (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    colonne_id UUID NOT NULL REFERENCES colonnes_personnalisees(id) ON DELETE CASCADE,
    revenu_id UUID NOT NULL REFERENCES revenus(id) ON DELETE CASCADE,
    valeur TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(colonne_id, revenu_id)
);

-- ============================================================================
-- TABLES DE GESTION DES UTILISATEURS
-- ============================================================================

-- Table des rôles
CREATE TABLE roles (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    code VARCHAR(50) UNIQUE NOT NULL,
    nom VARCHAR(255) NOT NULL,
    description TEXT,
    permissions JSONB, -- Liste des permissions en JSON
    actif BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table des utilisateurs
CREATE TABLE utilisateurs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email VARCHAR(255) UNIQUE NOT NULL,
    username VARCHAR(100) UNIQUE NOT NULL,
    nom VARCHAR(255) NOT NULL,
    prenom VARCHAR(255),
    password_hash VARCHAR(255) NOT NULL,
    role_id UUID NOT NULL REFERENCES roles(id) ON DELETE RESTRICT,
    commune_id UUID REFERENCES communes(id) ON DELETE SET NULL, -- Si l'utilisateur est lié à une commune
    telephone VARCHAR(50),
    dernier_login TIMESTAMP,
    actif BOOLEAN DEFAULT TRUE,
    email_verifie BOOLEAN DEFAULT FALSE,
    token_verification VARCHAR(255),
    token_reset_password VARCHAR(255),
    token_expiration TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================================
-- TABLES DE GESTION DES DOCUMENTS
-- ============================================================================

-- Table des types de documents
CREATE TABLE types_documents (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    code VARCHAR(50) UNIQUE NOT NULL,
    nom VARCHAR(255) NOT NULL,
    description TEXT,
    extensions_autorisees TEXT[], -- ['.pdf', '.xlsx', '.docx']
    taille_max_mo INTEGER DEFAULT 10,
    actif BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table des documents
CREATE TABLE documents (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    titre VARCHAR(255) NOT NULL,
    nom_fichier VARCHAR(255) NOT NULL,
    chemin_fichier TEXT NOT NULL,
    type_document_id UUID REFERENCES types_documents(id) ON DELETE SET NULL,
    taille_ko INTEGER,
    extension VARCHAR(10),
    commune_id UUID REFERENCES communes(id) ON DELETE CASCADE,
    exercice_id UUID REFERENCES exercices(id) ON DELETE CASCADE,
    revenu_id UUID REFERENCES revenus(id) ON DELETE CASCADE,
    description TEXT,
    tags TEXT[],
    indexe BOOLEAN DEFAULT FALSE, -- Pour la recherche full-text
    contenu_texte TEXT, -- Contenu extrait pour la recherche
    uploaded_by UUID REFERENCES utilisateurs(id) ON DELETE SET NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Index pour la recherche full-text
CREATE INDEX idx_documents_contenu ON documents USING gin(to_tsvector('french', contenu_texte));
CREATE INDEX idx_documents_tags ON documents USING gin(tags);

-- ============================================================================
-- TABLES DE NEWSLETTER
-- ============================================================================

-- Table des abonnés newsletter
CREATE TABLE newsletter_abonnes (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email VARCHAR(255) UNIQUE NOT NULL,
    nom VARCHAR(255),
    prenom VARCHAR(255),
    actif BOOLEAN DEFAULT TRUE,
    token_confirmation VARCHAR(255),
    confirme BOOLEAN DEFAULT FALSE,
    confirme_le TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table des campagnes newsletter
CREATE TABLE newsletter_campagnes (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    titre VARCHAR(255) NOT NULL,
    sujet VARCHAR(255) NOT NULL,
    contenu TEXT NOT NULL,
    date_envoi TIMESTAMP,
    statut VARCHAR(50) DEFAULT 'brouillon', -- brouillon, programmée, envoyée
    nb_destinataires INTEGER,
    nb_envoyes INTEGER DEFAULT 0,
    nb_ouverts INTEGER DEFAULT 0,
    nb_clics INTEGER DEFAULT 0,
    created_by UUID REFERENCES utilisateurs(id) ON DELETE SET NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================================
-- TABLES DE LOGS ET STATISTIQUES
-- ============================================================================

-- Table des logs de visites
CREATE TABLE logs_visites (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    page VARCHAR(255),
    utilisateur_id UUID REFERENCES utilisateurs(id) ON DELETE SET NULL,
    ip_adresse INET,
    user_agent TEXT,
    session_id VARCHAR(255),
    duree_secondes INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table des logs de téléchargements
CREATE TABLE logs_telechargements (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    document_id UUID REFERENCES documents(id) ON DELETE SET NULL,
    type_export VARCHAR(50), -- excel, word, pdf
    commune_id UUID REFERENCES communes(id) ON DELETE SET NULL,
    exercice_id UUID REFERENCES exercices(id) ON DELETE SET NULL,
    utilisateur_id UUID REFERENCES utilisateurs(id) ON DELETE SET NULL,
    ip_adresse INET,
    user_agent TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table des logs d'activité système
CREATE TABLE logs_activites (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    utilisateur_id UUID REFERENCES utilisateurs(id) ON DELETE SET NULL,
    action VARCHAR(100) NOT NULL, -- CREATE, UPDATE, DELETE, LOGIN, LOGOUT
    entite VARCHAR(100), -- nom de la table concernée
    entite_id UUID,
    anciennes_valeurs JSONB,
    nouvelles_valeurs JSONB,
    ip_adresse INET,
    user_agent TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_logs_activites_utilisateur ON logs_activites(utilisateur_id);
CREATE INDEX idx_logs_activites_action ON logs_activites(action);
CREATE INDEX idx_logs_activites_date ON logs_activites(created_at);

-- ============================================================================
-- TABLES POUR ÉCHANGE SÉCURISÉ D'INFORMATIONS
-- ============================================================================

-- Table des messages sécurisés
CREATE TABLE messages_securises (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    sujet VARCHAR(255) NOT NULL,
    contenu TEXT NOT NULL,
    expediteur_id UUID REFERENCES utilisateurs(id) ON DELETE SET NULL,
    destinataire_id UUID REFERENCES utilisateurs(id) ON DELETE CASCADE,
    commune_id UUID REFERENCES communes(id) ON DELETE SET NULL,
    lu BOOLEAN DEFAULT FALSE,
    lu_le TIMESTAMP,
    priorite VARCHAR(50) DEFAULT 'normale', -- basse, normale, haute, urgente
    fichiers_joints JSONB,
    archive BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================================
-- VUES UTILES
-- ============================================================================

-- Vue pour hiérarchie géographique complète
CREATE VIEW vue_hierarchie_geographique AS
SELECT
    c.id as commune_id,
    c.code as commune_code,
    c.nom as commune_nom,
    d.id as departement_id,
    d.code as departement_code,
    d.nom as departement_nom,
    r.id as region_id,
    r.code as region_code,
    r.nom as region_nom
FROM communes c
JOIN departements d ON c.departement_id = d.id
JOIN regions r ON c.region_id = r.id
WHERE c.actif = TRUE AND d.actif = TRUE AND r.actif = TRUE;

-- Vue pour revenus avec détails
CREATE VIEW vue_revenus_details AS
SELECT
    rev.id,
    rev.montant,
    rev.montant_prevu,
    rev.ecart,
    rev.taux_realisation,
    c.nom as commune_nom,
    c.code as commune_code,
    d.nom as departement_nom,
    r.nom as region_nom,
    rub.nom as rubrique_nom,
    rub.code as rubrique_code,
    cat.nom as categorie_nom,
    per.nom as periode_nom,
    ex.annee,
    pm.nom as projet_minier_nom,
    sm.nom as societe_miniere_nom,
    rev.created_at,
    rev.updated_at
FROM revenus rev
JOIN communes c ON rev.commune_id = c.id
JOIN departements d ON c.departement_id = d.id
JOIN regions r ON c.region_id = r.id
JOIN rubriques rub ON rev.rubrique_id = rub.id
LEFT JOIN categories_rubriques cat ON rub.categorie_id = cat.id
JOIN periodes per ON rev.periode_id = per.id
JOIN exercices ex ON per.exercice_id = ex.id
LEFT JOIN projets_miniers pm ON rev.projet_minier_id = pm.id
LEFT JOIN societes_minieres sm ON pm.societe_miniere_id = sm.id;

-- ============================================================================
-- FONCTIONS TRIGGERS
-- ============================================================================

-- Fonction pour mettre à jour updated_at automatiquement
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Application du trigger sur toutes les tables avec updated_at
CREATE TRIGGER update_regions_updated_at BEFORE UPDATE ON regions FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_departements_updated_at BEFORE UPDATE ON departements FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_communes_updated_at BEFORE UPDATE ON communes FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_projets_miniers_updated_at BEFORE UPDATE ON projets_miniers FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_exercices_updated_at BEFORE UPDATE ON exercices FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_periodes_updated_at BEFORE UPDATE ON periodes FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_rubriques_updated_at BEFORE UPDATE ON rubriques FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_revenus_updated_at BEFORE UPDATE ON revenus FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_utilisateurs_updated_at BEFORE UPDATE ON utilisateurs FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_documents_updated_at BEFORE UPDATE ON documents FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Fonction pour calculer l'écart et le taux de réalisation
CREATE OR REPLACE FUNCTION calculer_ecart_realisation()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.montant_prevu IS NOT NULL AND NEW.montant_prevu != 0 THEN
        NEW.ecart = NEW.montant - NEW.montant_prevu;
        NEW.taux_realisation = (NEW.montant / NEW.montant_prevu) * 100;
    END IF;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER calcul_revenus_ecart BEFORE INSERT OR UPDATE ON revenus
FOR EACH ROW EXECUTE FUNCTION calculer_ecart_realisation();

-- ============================================================================
-- COMMENTAIRES SUR LES TABLES
-- ============================================================================

COMMENT ON TABLE regions IS 'Régions administratives de Madagascar';
COMMENT ON TABLE departements IS 'Départements/Districts administratifs';
COMMENT ON TABLE communes IS 'Communes bénéficiaires des revenus miniers';
COMMENT ON TABLE projets_miniers IS 'Projets d''extraction minière sources de revenus';
COMMENT ON TABLE rubriques IS 'Rubriques (lignes) du tableau de compte administratif - structure flexible';
COMMENT ON TABLE periodes IS 'Périodes (colonnes) du tableau - structure flexible';
COMMENT ON TABLE revenus IS 'Données de revenus - cœur du système';
COMMENT ON TABLE colonnes_personnalisees IS 'Permet d''ajouter des colonnes dynamiquement sans coder';
COMMENT ON TABLE documents IS 'Documents justificatifs avec indexation full-text';
COMMENT ON TABLE logs_visites IS 'Statistiques de visites du site';
COMMENT ON TABLE logs_telechargements IS 'Statistiques de téléchargements';
