-- ============================================================================
-- POLITIQUES ROW LEVEL SECURITY (RLS) - SUPABASE
-- ============================================================================
-- Ces politiques définissent les règles d'accès aux données
-- ============================================================================

-- Activer RLS sur toutes les tables
ALTER TABLE regions ENABLE ROW LEVEL SECURITY;
ALTER TABLE districts ENABLE ROW LEVEL SECURITY;
ALTER TABLE communes ENABLE ROW LEVEL SECURITY;
ALTER TABLE projets_miniers ENABLE ROW LEVEL SECURITY;
ALTER TABLE revenus_miniers ENABLE ROW LEVEL SECURITY;
ALTER TABLE comptes_administratifs ENABLE ROW LEVEL SECURITY;
ALTER TABLE categories_rubriques ENABLE ROW LEVEL SECURITY;
ALTER TABLE rubriques_budgetaires ENABLE ROW LEVEL SECURITY;
ALTER TABLE colonnes_dynamiques ENABLE ROW LEVEL SECURITY;
ALTER TABLE lignes_budgetaires ENABLE ROW LEVEL SECURITY;
ALTER TABLE documents ENABLE ROW LEVEL SECURITY;
ALTER TABLE newsletter_subscribers ENABLE ROW LEVEL SECURITY;
ALTER TABLE analytics_visites ENABLE ROW LEVEL SECURITY;
ALTER TABLE analytics_telechargements ENABLE ROW LEVEL SECURITY;
ALTER TABLE profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE activity_logs ENABLE ROW LEVEL SECURITY;
ALTER TABLE messages_securises ENABLE ROW LEVEL SECURITY;

-- ============================================================================
-- FONCTIONS UTILITAIRES POUR LES POLITIQUES
-- ============================================================================

-- Fonction: Vérifier le rôle de l'utilisateur
CREATE OR REPLACE FUNCTION public.get_user_role(user_id UUID)
RETURNS TEXT AS $$
BEGIN
    RETURN (
        SELECT role
        FROM profiles
        WHERE id = user_id AND est_actif = TRUE
        LIMIT 1
    );
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Fonction: Vérifier si l'utilisateur est administrateur
CREATE OR REPLACE FUNCTION public.is_admin()
RETURNS BOOLEAN AS $$
BEGIN
    RETURN (
        SELECT role = 'administrateur'
        FROM profiles
        WHERE id = auth.uid() AND est_actif = TRUE
    );
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Fonction: Vérifier si l'utilisateur est éditeur ou admin
CREATE OR REPLACE FUNCTION public.can_edit()
RETURNS BOOLEAN AS $$
BEGIN
    RETURN (
        SELECT role IN ('administrateur', 'editeur')
        FROM profiles
        WHERE id = auth.uid() AND est_actif = TRUE
    );
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- ============================================================================
-- POLITIQUES: COLLECTIVITÉS TERRITORIALES (PUBLIC)
-- ============================================================================

-- REGIONS: Lecture publique
CREATE POLICY "Regions: lecture publique"
    ON regions FOR SELECT
    USING (true);

-- REGIONS: Modification admin uniquement
CREATE POLICY "Regions: modification admin"
    ON regions FOR ALL
    USING (is_admin())
    WITH CHECK (is_admin());

-- DISTRICTS: Lecture publique
CREATE POLICY "Districts: lecture publique"
    ON districts FOR SELECT
    USING (true);

-- DISTRICTS: Modification admin uniquement
CREATE POLICY "Districts: modification admin"
    ON districts FOR ALL
    USING (is_admin())
    WITH CHECK (is_admin());

-- COMMUNES: Lecture publique
CREATE POLICY "Communes: lecture publique"
    ON communes FOR SELECT
    USING (true);

-- COMMUNES: Modification admin uniquement
CREATE POLICY "Communes: modification admin"
    ON communes FOR ALL
    USING (is_admin())
    WITH CHECK (is_admin());

-- ============================================================================
-- POLITIQUES: PROJETS MINIERS ET REVENUS
-- ============================================================================

-- PROJETS_MINIERS: Lecture publique
CREATE POLICY "Projets miniers: lecture publique"
    ON projets_miniers FOR SELECT
    USING (true);

-- PROJETS_MINIERS: Modification admin uniquement
CREATE POLICY "Projets miniers: modification admin"
    ON projets_miniers FOR ALL
    USING (is_admin())
    WITH CHECK (is_admin());

-- REVENUS_MINIERS: Lecture publique
CREATE POLICY "Revenus miniers: lecture publique"
    ON revenus_miniers FOR SELECT
    USING (true);

-- REVENUS_MINIERS: Modification par éditeurs et admin
CREATE POLICY "Revenus miniers: modification éditeurs"
    ON revenus_miniers FOR ALL
    USING (can_edit())
    WITH CHECK (can_edit());

-- ============================================================================
-- POLITIQUES: COMPTES ADMINISTRATIFS
-- ============================================================================

-- COMPTES_ADMINISTRATIFS: Lecture des comptes publiés (public)
CREATE POLICY "Comptes: lecture publique des comptes publiés"
    ON comptes_administratifs FOR SELECT
    USING (statut = 'publie');

-- COMPTES_ADMINISTRATIFS: Lecture de tous les comptes (authentifié)
CREATE POLICY "Comptes: lecture complète authentifiés"
    ON comptes_administratifs FOR SELECT
    USING (auth.role() = 'authenticated');

-- COMPTES_ADMINISTRATIFS: Création par éditeurs
CREATE POLICY "Comptes: création par éditeurs"
    ON comptes_administratifs FOR INSERT
    WITH CHECK (can_edit());

-- COMPTES_ADMINISTRATIFS: Modification de ses propres comptes en brouillon
CREATE POLICY "Comptes: modification propres brouillons"
    ON comptes_administratifs FOR UPDATE
    USING (
        created_by = auth.uid() AND
        statut IN ('brouillon', 'valide')
    )
    WITH CHECK (
        created_by = auth.uid() AND
        statut IN ('brouillon', 'valide')
    );

-- COMPTES_ADMINISTRATIFS: Modification complète par admin
CREATE POLICY "Comptes: modification complète admin"
    ON comptes_administratifs FOR UPDATE
    USING (is_admin())
    WITH CHECK (is_admin());

-- COMPTES_ADMINISTRATIFS: Suppression par admin uniquement
CREATE POLICY "Comptes: suppression admin"
    ON comptes_administratifs FOR DELETE
    USING (is_admin());

-- ============================================================================
-- POLITIQUES: RUBRIQUES BUDGÉTAIRES (RÉFÉRENTIEL)
-- ============================================================================

-- CATEGORIES_RUBRIQUES: Lecture publique
CREATE POLICY "Catégories: lecture publique"
    ON categories_rubriques FOR SELECT
    USING (true);

-- CATEGORIES_RUBRIQUES: Modification admin
CREATE POLICY "Catégories: modification admin"
    ON categories_rubriques FOR ALL
    USING (is_admin())
    WITH CHECK (is_admin());

-- RUBRIQUES_BUDGETAIRES: Lecture publique des rubriques actives
CREATE POLICY "Rubriques: lecture publique actives"
    ON rubriques_budgetaires FOR SELECT
    USING (est_active = true);

-- RUBRIQUES_BUDGETAIRES: Lecture complète authentifié
CREATE POLICY "Rubriques: lecture complète authentifiés"
    ON rubriques_budgetaires FOR SELECT
    USING (auth.role() = 'authenticated');

-- RUBRIQUES_BUDGETAIRES: Modification admin
CREATE POLICY "Rubriques: modification admin"
    ON rubriques_budgetaires FOR ALL
    USING (is_admin())
    WITH CHECK (is_admin());

-- ============================================================================
-- POLITIQUES: COLONNES DYNAMIQUES
-- ============================================================================

-- COLONNES_DYNAMIQUES: Lecture publique des colonnes actives
CREATE POLICY "Colonnes: lecture publique actives"
    ON colonnes_dynamiques FOR SELECT
    USING (est_active = true);

-- COLONNES_DYNAMIQUES: Lecture complète authentifié
CREATE POLICY "Colonnes: lecture complète authentifiés"
    ON colonnes_dynamiques FOR SELECT
    USING (auth.role() = 'authenticated');

-- COLONNES_DYNAMIQUES: Modification admin
CREATE POLICY "Colonnes: modification admin"
    ON colonnes_dynamiques FOR ALL
    USING (is_admin())
    WITH CHECK (is_admin());

-- ============================================================================
-- POLITIQUES: LIGNES BUDGÉTAIRES
-- ============================================================================

-- LIGNES_BUDGETAIRES: Lecture selon statut du compte
CREATE POLICY "Lignes: lecture publique (comptes publiés)"
    ON lignes_budgetaires FOR SELECT
    USING (
        EXISTS (
            SELECT 1 FROM comptes_administratifs ca
            WHERE ca.id = compte_administratif_id
            AND ca.statut = 'publie'
        )
    );

-- LIGNES_BUDGETAIRES: Lecture complète authentifié
CREATE POLICY "Lignes: lecture complète authentifiés"
    ON lignes_budgetaires FOR SELECT
    USING (auth.role() = 'authenticated');

-- LIGNES_BUDGETAIRES: Modification de ses propres lignes
CREATE POLICY "Lignes: modification propres comptes"
    ON lignes_budgetaires FOR ALL
    USING (
        EXISTS (
            SELECT 1 FROM comptes_administratifs ca
            WHERE ca.id = compte_administratif_id
            AND ca.created_by = auth.uid()
            AND ca.statut IN ('brouillon', 'valide')
        )
    )
    WITH CHECK (
        EXISTS (
            SELECT 1 FROM comptes_administratifs ca
            WHERE ca.id = compte_administratif_id
            AND ca.created_by = auth.uid()
            AND ca.statut IN ('brouillon', 'valide')
        )
    );

-- LIGNES_BUDGETAIRES: Modification complète admin
CREATE POLICY "Lignes: modification complète admin"
    ON lignes_budgetaires FOR ALL
    USING (is_admin())
    WITH CHECK (is_admin());

-- ============================================================================
-- POLITIQUES: DOCUMENTS
-- ============================================================================

-- DOCUMENTS: Lecture des documents publics
CREATE POLICY "Documents: lecture publique"
    ON documents FOR SELECT
    USING (est_public = true);

-- DOCUMENTS: Lecture complète authentifié
CREATE POLICY "Documents: lecture complète authentifiés"
    ON documents FOR SELECT
    USING (auth.role() = 'authenticated');

-- DOCUMENTS: Upload par éditeurs
CREATE POLICY "Documents: upload par éditeurs"
    ON documents FOR INSERT
    WITH CHECK (can_edit());

-- DOCUMENTS: Modification de ses propres uploads
CREATE POLICY "Documents: modification propres uploads"
    ON documents FOR UPDATE
    USING (uploaded_by = auth.uid())
    WITH CHECK (uploaded_by = auth.uid());

-- DOCUMENTS: Modification complète admin
CREATE POLICY "Documents: modification complète admin"
    ON documents FOR UPDATE
    USING (is_admin())
    WITH CHECK (is_admin());

-- DOCUMENTS: Suppression admin ou propriétaire
CREATE POLICY "Documents: suppression admin ou propriétaire"
    ON documents FOR DELETE
    USING (is_admin() OR uploaded_by = auth.uid());

-- ============================================================================
-- POLITIQUES: NEWSLETTER
-- ============================================================================

-- NEWSLETTER_SUBSCRIBERS: Insertion publique (auto-inscription)
CREATE POLICY "Newsletter: inscription publique"
    ON newsletter_subscribers FOR INSERT
    WITH CHECK (true);

-- NEWSLETTER_SUBSCRIBERS: Modification de son propre profil
CREATE POLICY "Newsletter: modification propre profil"
    ON newsletter_subscribers FOR UPDATE
    USING (email = (SELECT email FROM auth.users WHERE id = auth.uid()))
    WITH CHECK (email = (SELECT email FROM auth.users WHERE id = auth.uid()));

-- NEWSLETTER_SUBSCRIBERS: Lecture admin uniquement
CREATE POLICY "Newsletter: lecture admin"
    ON newsletter_subscribers FOR SELECT
    USING (is_admin());

-- NEWSLETTER_SUBSCRIBERS: Suppression admin ou soi-même
CREATE POLICY "Newsletter: désabonnement"
    ON newsletter_subscribers FOR DELETE
    USING (
        is_admin() OR
        email = (SELECT email FROM auth.users WHERE id = auth.uid())
    );

-- ============================================================================
-- POLITIQUES: ANALYTICS
-- ============================================================================

-- ANALYTICS_VISITES: Insertion publique (tracking)
CREATE POLICY "Analytics visites: insertion publique"
    ON analytics_visites FOR INSERT
    WITH CHECK (true);

-- ANALYTICS_VISITES: Lecture admin uniquement
CREATE POLICY "Analytics visites: lecture admin"
    ON analytics_visites FOR SELECT
    USING (is_admin());

-- ANALYTICS_TELECHARGEMENTS: Insertion publique (tracking)
CREATE POLICY "Analytics téléchargements: insertion publique"
    ON analytics_telechargements FOR INSERT
    WITH CHECK (true);

-- ANALYTICS_TELECHARGEMENTS: Lecture admin uniquement
CREATE POLICY "Analytics téléchargements: lecture admin"
    ON analytics_telechargements FOR SELECT
    USING (is_admin());

-- ============================================================================
-- POLITIQUES: PROFILS UTILISATEURS
-- ============================================================================

-- PROFILES: Lecture de son propre profil
CREATE POLICY "Profils: lecture propre profil"
    ON profiles FOR SELECT
    USING (id = auth.uid());

-- PROFILES: Lecture de tous les profils (admin)
CREATE POLICY "Profils: lecture complète admin"
    ON profiles FOR SELECT
    USING (is_admin());

-- PROFILES: Modification de son propre profil (champs limités)
CREATE POLICY "Profils: modification propre profil"
    ON profiles FOR UPDATE
    USING (id = auth.uid())
    WITH CHECK (
        id = auth.uid() AND
        -- L'utilisateur ne peut pas changer son propre rôle
        role = (SELECT role FROM profiles WHERE id = auth.uid())
    );

-- PROFILES: Modification complète admin
CREATE POLICY "Profils: modification complète admin"
    ON profiles FOR UPDATE
    USING (is_admin())
    WITH CHECK (is_admin());

-- PROFILES: Création automatique lors de l'inscription
CREATE POLICY "Profils: création auto"
    ON profiles FOR INSERT
    WITH CHECK (id = auth.uid());

-- ============================================================================
-- POLITIQUES: JOURNAL D'ACTIVITÉ
-- ============================================================================

-- ACTIVITY_LOGS: Insertion par utilisateurs authentifiés
CREATE POLICY "Logs: insertion authentifiés"
    ON activity_logs FOR INSERT
    WITH CHECK (auth.role() = 'authenticated');

-- ACTIVITY_LOGS: Lecture de ses propres logs
CREATE POLICY "Logs: lecture propres logs"
    ON activity_logs FOR SELECT
    USING (user_id = auth.uid());

-- ACTIVITY_LOGS: Lecture complète admin
CREATE POLICY "Logs: lecture complète admin"
    ON activity_logs FOR SELECT
    USING (is_admin());

-- ============================================================================
-- POLITIQUES: MESSAGES SÉCURISÉS
-- ============================================================================

-- MESSAGES_SECURISES: Lecture de ses messages (expéditeur ou destinataire)
CREATE POLICY "Messages: lecture propres messages"
    ON messages_securises FOR SELECT
    USING (
        expediteur_id = auth.uid() OR
        destinataire_id = auth.uid()
    );

-- MESSAGES_SECURISES: Envoi de messages
CREATE POLICY "Messages: envoi par authentifiés"
    ON messages_securises FOR INSERT
    WITH CHECK (
        auth.role() = 'authenticated' AND
        expediteur_id = auth.uid()
    );

-- MESSAGES_SECURISES: Modification de ses messages envoyés
CREATE POLICY "Messages: modification propres messages"
    ON messages_securises FOR UPDATE
    USING (expediteur_id = auth.uid())
    WITH CHECK (expediteur_id = auth.uid());

-- MESSAGES_SECURISES: Suppression admin ou expéditeur
CREATE POLICY "Messages: suppression admin ou expéditeur"
    ON messages_securises FOR DELETE
    USING (is_admin() OR expediteur_id = auth.uid());

-- ============================================================================
-- TRIGGER: Création automatique du profil utilisateur
-- ============================================================================

-- Fonction: Créer un profil lors de l'inscription
CREATE OR REPLACE FUNCTION public.handle_new_user()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO public.profiles (id, email, role, est_actif)
    VALUES (
        NEW.id,
        NEW.email,
        'lecteur', -- Rôle par défaut
        TRUE
    );
    RETURN NEW;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Trigger: Créer le profil après création d'un utilisateur
DROP TRIGGER IF EXISTS on_auth_user_created ON auth.users;
CREATE TRIGGER on_auth_user_created
    AFTER INSERT ON auth.users
    FOR EACH ROW EXECUTE FUNCTION public.handle_new_user();

-- ============================================================================
-- TRIGGER: Journalisation automatique des modifications
-- ============================================================================

-- Fonction: Enregistrer les modifications dans activity_logs
CREATE OR REPLACE FUNCTION public.log_activity()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO public.activity_logs (
        user_id,
        action,
        table_name,
        record_id,
        old_values,
        new_values
    ) VALUES (
        auth.uid(),
        TG_OP,
        TG_TABLE_NAME,
        COALESCE(NEW.id, OLD.id),
        CASE WHEN TG_OP = 'DELETE' THEN to_jsonb(OLD) ELSE NULL END,
        CASE WHEN TG_OP IN ('INSERT', 'UPDATE') THEN to_jsonb(NEW) ELSE NULL END
    );
    RETURN COALESCE(NEW, OLD);
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Appliquer le logging aux tables critiques
CREATE TRIGGER log_comptes_administratifs_changes
    AFTER INSERT OR UPDATE OR DELETE ON comptes_administratifs
    FOR EACH ROW EXECUTE FUNCTION log_activity();

CREATE TRIGGER log_lignes_budgetaires_changes
    AFTER INSERT OR UPDATE OR DELETE ON lignes_budgetaires
    FOR EACH ROW EXECUTE FUNCTION log_activity();

CREATE TRIGGER log_documents_changes
    AFTER INSERT OR UPDATE OR DELETE ON documents
    FOR EACH ROW EXECUTE FUNCTION log_activity();

CREATE TRIGGER log_profiles_changes
    AFTER UPDATE ON profiles
    FOR EACH ROW EXECUTE FUNCTION log_activity();

-- ============================================================================
-- GRANTS: Permissions pour l'utilisateur Supabase
-- ============================================================================

-- Accorder les permissions nécessaires
GRANT USAGE ON SCHEMA public TO anon, authenticated;

-- Tables accessibles publiquement (lecture)
GRANT SELECT ON regions, districts, communes TO anon;
GRANT SELECT ON projets_miniers, revenus_miniers TO anon;
GRANT SELECT ON categories_rubriques, rubriques_budgetaires, colonnes_dynamiques TO anon;

-- Tables accessibles aux utilisateurs authentifiés
GRANT ALL ON ALL TABLES IN SCHEMA public TO authenticated;
GRANT ALL ON ALL SEQUENCES IN SCHEMA public TO authenticated;

-- ============================================================================
-- FIN DES POLITIQUES
-- ============================================================================
