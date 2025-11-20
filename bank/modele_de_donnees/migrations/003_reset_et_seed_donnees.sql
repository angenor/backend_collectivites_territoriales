-- ============================================================================
-- Script de réinitialisation et seed de la base de données (VERSION CORRIGÉE)
-- Basé sur le fichier Excel: Tableaux_de_Compte_Administratif.xlsx
-- ⚠️ CORRECTION: Doublons supprimés (16 doublons éliminés)
-- ============================================================================

-- ============================================================================
-- ÉTAPE 1: NETTOYAGE DES DONNÉES EXISTANTES
-- ============================================================================

-- Désactiver temporairement les triggers pour éviter les erreurs
SET session_replication_role = 'replica';

-- Supprimer les données dans l'ordre inverse des dépendances
DELETE FROM lignes_budgetaires;
DELETE FROM comptes_administratifs;
DELETE FROM colonnes_dynamiques;
DELETE FROM rubriques_budgetaires;
DELETE FROM categories_rubriques;

-- Réactiver les triggers
SET session_replication_role = 'origin';

-- ============================================================================
-- ÉTAPE 2: INSERTION DES COLONNES DYNAMIQUES
-- ============================================================================

-- Colonnes communes (applicables aux recettes ET dépenses)
INSERT INTO colonnes_dynamiques (code, nom, type_donnee, ordre, est_calculee, formule_calcul, est_active, applicable_a, description) VALUES
('budget_primitif', 'Budget primitif', 'montant', 1, false, NULL, true, 'tous', 'Budget voté initial'),
('budget_additionnel', 'Budget additionnel', 'montant', 2, false, NULL, true, 'tous', 'Ajustements budgétaires en cours d''année'),
('modifications', 'Modifications +/-', 'montant', 3, false, NULL, true, 'tous', 'Virements et transferts de crédits'),
('previsions_definitives', 'Prévisions définitives', 'montant', 4, true, 'budget_primitif + budget_additionnel + modifications', true, 'tous', 'Budget final après modifications');

-- Colonnes spécifiques aux RECETTES
INSERT INTO colonnes_dynamiques (code, nom, type_donnee, ordre, est_calculee, formule_calcul, est_active, applicable_a, description) VALUES
('or_admis', 'OR admis', 'montant', 5, false, NULL, true, 'recette', 'Ordres de recettes admis'),
('recouvrement', 'Recouvrement', 'montant', 6, false, NULL, true, 'recette', 'Montant effectivement recouvré'),
('reste_recouvrer', 'Reste à recouvrer', 'montant', 7, true, 'or_admis - recouvrement', true, 'recette', 'Montant restant à recouvrer'),
('taux_execution_recette', 'Taux d''exécution', 'pourcentage', 8, true, '(or_admis / previsions_definitives) * 100', true, 'recette', 'Taux d''exécution des recettes');

-- Colonnes spécifiques aux DÉPENSES  
INSERT INTO colonnes_dynamiques (code, nom, type_donnee, ordre, est_calculee, formule_calcul, est_active, applicable_a, description) VALUES
('engagement', 'Engagement', 'montant', 5, false, NULL, true, 'depense', 'Montant engagé'),
('mandat_admis', 'Mandat admis', 'montant', 6, false, NULL, true, 'depense', 'Mandats de paiement admis'),
('paiement', 'Paiement', 'montant', 7, false, NULL, true, 'depense', 'Montant effectivement payé'),
('reste_payer', 'Reste à payer', 'montant', 8, true, 'mandat_admis - paiement', true, 'depense', 'Montant restant à payer'),
('taux_execution_depense', 'Taux d''exécution', 'pourcentage', 9, true, '(mandat_admis / previsions_definitives) * 100', true, 'depense', 'Taux d''exécution des dépenses');

-- ============================================================================
-- ÉTAPE 3: INSERTION DES RUBRIQUES BUDGÉTAIRES - RECETTES
-- ============================================================================

INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('70', 'IMPOTS SUR LES REVENUS, BENEFICES ET GAINS', 'recette', 'fonctionnement', 1, 0, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('708', 'Autres impôts sur les revenus', 'recette', 'fonctionnement', 2, 1, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('7080', 'Autres impôts sur les revenus - Impôt synthétique', 'recette', 'fonctionnement', 3, 2, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('71', 'IMPOTS SUR LE PATRIMOINE', 'recette', 'fonctionnement', 1, 3, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('714', 'Impôts fonciers sur les terrains - IFT', 'recette', 'fonctionnement', 2, 4, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('7140', 'Impôts fonciers sur les terrains - IFT', 'recette', 'fonctionnement', 3, 5, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('715', 'Impôt foncier sur les propriétés bâties – IFPB', 'recette', 'fonctionnement', 2, 6, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('7151', 'Impôt foncier sur les propriétés bâties – IFPB', 'recette', 'fonctionnement', 3, 7, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('7158', 'Autres impôts locaux sur les propriétés baties', 'recette', 'fonctionnement', 3, 8, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('718', 'Taxe annuelle sur autres patrimoines', 'recette', 'fonctionnement', 2, 9, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('7181', 'Taxes sur les appareils automatiques ou électroniques', 'recette', 'fonctionnement', 3, 10, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('7182', 'Taxes sur les appareils mecaniques', 'recette', 'fonctionnement', 3, 11, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('7188', 'Autres taxes et impots annuels', 'recette', 'fonctionnement', 3, 12, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('72', 'IMPOTS SUR LES BIENS ET SERVICES', 'recette', 'fonctionnement', 1, 13, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('725', 'Taxes particulières sur les biens', 'recette', 'fonctionnement', 2, 14, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('7251', 'Taxes sur l''électricité', 'recette', 'fonctionnement', 3, 15, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('7252', 'Taxes sur l''eau', 'recette', 'fonctionnement', 3, 16, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('7253', 'Surtaxe sur l''eau et l''électricité', 'recette', 'fonctionnement', 3, 17, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('7254', 'Taxes sur les eaux minérales', 'recette', 'fonctionnement', 3, 18, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('7258', 'Autres taxes particulières sur les biens', 'recette', 'fonctionnement', 3, 19, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('726', 'Taxes particulières sur les services', 'recette', 'fonctionnement', 2, 20, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('7261', 'taxes sur la publicité', 'recette', 'fonctionnement', 3, 21, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('7262', 'Taxe d’abattage', 'recette', 'fonctionnement', 3, 22, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('7263', 'Taxe de visite et de poinçonnage des viandes', 'recette', 'fonctionnement', 3, 23, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('7268', 'Autres taxes locales sur les services', 'recette', 'fonctionnement', 3, 24, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('727', 'Taxes particulières sur les activités', 'recette', 'fonctionnement', 2, 25, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('7273', 'Impôt de licence', 'recette', 'fonctionnement', 3, 26, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('7274', 'Prélèvement sur les produits de jeux - PPJ', 'recette', 'fonctionnement', 3, 27, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('7276', 'Taxes sur les fêtes, spectacles et manifestations…', 'recette', 'fonctionnement', 3, 28, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('7277', 'Taxes sur les établissements exerçant des activités à but lucratif', 'recette', 'fonctionnement', 3, 29, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('7278', 'Autres taxes locales sur les activités', 'recette', 'fonctionnement', 3, 30, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('728', 'Autres impôts sur les biens et services', 'recette', 'fonctionnement', 2, 31, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('7280', 'Autres impôts sur les biens et services', 'recette', 'fonctionnement', 3, 32, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('74', 'AUTRES RECETTES FISCALES', 'recette', 'fonctionnement', 1, 33, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('743', 'Amendes fiscales et pénalités', 'recette', 'fonctionnement', 2, 34, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('7431', 'Amendes fiscales', 'recette', 'fonctionnement', 3, 35, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('7432', 'Pénalité', 'recette', 'fonctionnement', 3, 36, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('7433', 'Intérêt moratoire', 'recette', 'fonctionnement', 3, 37, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('748', 'Taxes diverses', 'recette', 'fonctionnement', 2, 38, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('7482', 'Droits et taxes diverses : Activités agricoles', 'recette', 'fonctionnement', 3, 39, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('75', 'CONTRIBUTIONS RECUES DES TIERS', 'recette', 'fonctionnement', 1, 40, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('751', 'Subvention d''exploitation - Etat', 'recette', 'fonctionnement', 2, 41, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('7511', 'Dotation globale -EPP', 'recette', 'fonctionnement', 3, 42, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('7512', 'Dotation globale -CSB', 'recette', 'fonctionnement', 3, 43, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('7513', 'Dotation globale -Etat civil', 'recette', 'fonctionnement', 3, 44, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('7518', 'Dotation globale -Autres', 'recette', 'fonctionnement', 3, 45, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('752', 'Subventions d''exploitation reçcues des Collectivités Publiques', 'recette', 'fonctionnement', 2, 46, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('7522', 'Collectivités Territoriales Décentralisées', 'recette', 'fonctionnement', 3, 47, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('7523', 'Etablissements Publics à caractère Industriel et Commercial (EPIC)', 'recette', 'fonctionnement', 3, 48, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('7524', 'Etablissements Publics à caractère Administratifs (EPA)', 'recette', 'fonctionnement', 3, 49, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('7528', 'Autres Collectivités Publiques', 'recette', 'fonctionnement', 3, 50, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('755', 'Organismes privés locaux', 'recette', 'fonctionnement', 2, 51, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('7550', 'organisme privée locaux', 'recette', 'fonctionnement', 3, 52, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('76', 'PRODUITS FINANCIERS', 'recette', 'fonctionnement', 1, 53, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('761', 'Produits des prises de participation', 'recette', 'fonctionnement', 2, 54, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('7610', 'Produits des prises de participation', 'recette', 'fonctionnement', 3, 55, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('762', 'Produits des autres immobilisations financières', 'recette', 'fonctionnement', 2, 56, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('7621', 'Revenus des obligations et bons à plus d''un an', 'recette', 'fonctionnement', 3, 57, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('7622', 'Revenus des prêts à long et moyen terme', 'recette', 'fonctionnement', 3, 58, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('763', 'Revenus des autres créances', 'recette', 'fonctionnement', 2, 59, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('7630', 'Revenus des autres créances', 'recette', 'fonctionnement', 3, 60, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('764', 'Revenus des titres de placement et des prêts à court terme', 'recette', 'fonctionnement', 2, 61, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('7641', 'Revenus des obligations et bons à court terme', 'recette', 'fonctionnement', 3, 62, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('7642', 'Revenus des prêts à court terme', 'recette', 'fonctionnement', 3, 63, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('768', 'Autres produits financiers', 'recette', 'fonctionnement', 2, 64, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('7680', 'Autres produits financiers', 'recette', 'fonctionnement', 3, 65, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('77', 'RECETTES NON FISCALES', 'recette', 'fonctionnement', 1, 66, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('771', 'Redevances', 'recette', 'fonctionnement', 2, 67, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('7711', 'Redevances de collecte et de traitement des ordures ménagères - ROM', 'recette', 'fonctionnement', 3, 68, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('7712', 'Redevances de rejet des eaux usées - RREU', 'recette', 'fonctionnement', 3, 69, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('7713', 'Redevance et frais d''administration minière', 'recette', 'fonctionnement', 3, 70, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('7714', 'Redevances sur autorisations administratives', 'recette', 'fonctionnement', 3, 71, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('7715', 'Redevance fixe d''abonnement pour branchement', 'recette', 'fonctionnement', 3, 72, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('7716', 'Redevance versées par les fermiers et concessionnaires', 'recette', 'fonctionnement', 3, 73, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('7717', 'Produits des ristournes', 'recette', 'fonctionnement', 3, 74, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('7718', 'Autres redevances locales', 'recette', 'fonctionnement', 3, 75, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('772', 'Produits des activités des services', 'recette', 'fonctionnement', 2, 76, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('7721', 'Prestation de service', 'recette', 'fonctionnement', 3, 77, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('7722', 'Produits finis', 'recette', 'fonctionnement', 3, 78, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('7723', 'Produits intermédiaires', 'recette', 'fonctionnement', 3, 79, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('7724', 'Produits résiduels', 'recette', 'fonctionnement', 3, 80, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('7725', 'Travaux', 'recette', 'fonctionnement', 3, 81, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('7726', 'Marchandises', 'recette', 'fonctionnement', 3, 82, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('7727', 'revenus des domaines', 'recette', 'fonctionnement', 3, 83, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('7728', 'Autres produits des activités des services', 'recette', 'fonctionnement', 3, 84, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('773', 'Produits des activités annexes et accessoires', 'recette', 'fonctionnement', 2, 85, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('7731', 'Commissions et courtages', 'recette', 'fonctionnement', 3, 86, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('7732', 'Locations diverses', 'recette', 'fonctionnement', 3, 87, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('7733', 'Confiscations', 'recette', 'fonctionnement', 3, 88, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('7734', 'Droit de fourrières', 'recette', 'fonctionnement', 3, 89, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('7735', 'Droit de stationnement', 'recette', 'fonctionnement', 3, 90, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('7738', 'Autres', 'recette', 'fonctionnement', 3, 91, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('774', 'Production immobilisée', 'recette', 'fonctionnement', 2, 92, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('7741', 'Immobilisation incorporelle', 'recette', 'fonctionnement', 3, 93, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('7742', 'Immobilisations corporelle', 'recette', 'fonctionnement', 3, 94, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('10', 'FONDS, DOTATIONS ET RESERVES', 'recette', 'investissement', 1, 95, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('101', 'Dotations et fonds divers', 'recette', 'investissement', 2, 96, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('1011', 'Contreparties d''intégrations pratimoniales', 'recette', 'investissement', 3, 97, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('1012', 'Dotations de l’État', 'recette', 'investissement', 3, 98, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('1013', 'Dotations : autres collectivités ou organismes publics', 'recette', 'investissement', 3, 99, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('1014', 'Fonds de travaux électricité', 'recette', 'investissement', 3, 100, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('1015', 'Fonds de travaux réseau eau', 'recette', 'investissement', 3, 101, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('1016', 'Dons et legs en capital', 'recette', 'investissement', 3, 102, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('1017', 'Mises à disposition', 'recette', 'investissement', 3, 103, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('1018', 'Autres', 'recette', 'investissement', 3, 104, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('106', 'Réserves', 'recette', 'investissement', 2, 105, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('1061', 'Réserves des budgets annexes', 'recette', 'investissement', 3, 106, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('1064', 'Excédent de fonctionnement capitalisé', 'recette', 'investissement', 3, 107, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('1068', 'Autres réserves', 'recette', 'investissement', 3, 108, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('13', 'SUBVENTIONS D''EQUIPEMENT', 'recette', 'investissement', 1, 109, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('131', 'Subventions d''équipement reçues', 'recette', 'investissement', 2, 110, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('1311', 'Subventions reçues de l''Etat', 'recette', 'investissement', 3, 111, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('1312', 'Subventions reçues des Collectivités Territoriales Décentralisées', 'recette', 'investissement', 3, 112, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('1313', 'Subventions reçues des Organismes nationaux et internationaux', 'recette', 'investissement', 3, 113, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('1314', 'Aides bilatérales', 'recette', 'investissement', 3, 114, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('1315', 'Aides multilatérales', 'recette', 'investissement', 3, 115, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('1318', 'Autres subventions d''équipement reçues', 'recette', 'investissement', 3, 116, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('139', 'Subvention d''investissement transférée au compte de résultat', 'recette', 'investissement', 2, 117, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('1390', 'Subvention d''investissement transférée au compte de résultat', 'recette', 'investissement', 3, 118, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('14', 'CESSIONS D''IMMOBILISATIONS', 'recette', 'investissement', 1, 119, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('141', 'Cession d''immobilisations incorporelles', 'recette', 'investissement', 2, 120, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('1411', 'Frais de développement, de recherche et d''études', 'recette', 'investissement', 3, 121, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('1415', 'Concessions et droits similaires, brevets, licence, marques', 'recette', 'investissement', 3, 122, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('1418', 'Autres immobilisations incorporelles', 'recette', 'investissement', 3, 123, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('142', 'Cession d''immobilisations corporelles', 'recette', 'investissement', 2, 124, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('1421', 'Terrains', 'recette', 'investissement', 3, 125, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('1423', 'Bâtiments', 'recette', 'investissement', 3, 126, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('1424', 'Voies', 'recette', 'investissement', 3, 127, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('1425', 'Réseaux', 'recette', 'investissement', 3, 128, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('1426', 'Matériel et ouillage', 'recette', 'investissement', 3, 129, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('1427', 'Matériels de transport', 'recette', 'investissement', 3, 130, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('1428', 'Autres immobilisations corporelles', 'recette', 'investissement', 3, 131, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('147', 'Cession d''immobilisations financières', 'recette', 'investissement', 2, 132, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('1471', 'Ventes de titres de participations', 'recette', 'investissement', 3, 133, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('1472', 'Remboursements de prêts accordés à long terme et moyen terme', 'recette', 'investissement', 3, 134, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('1473', 'Remboursements de prêts accordés à court terme', 'recette', 'investissement', 3, 135, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('1474', 'Remboursements d''avances accordées', 'recette', 'investissement', 3, 136, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('1478', 'Autres immobilisations financières', 'recette', 'investissement', 3, 137, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('16', 'EMPRUNTS ET DETTES ASSIMILEES', 'recette', 'investissement', 1, 138, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('161', 'Emprunts en Ariary', 'recette', 'investissement', 2, 139, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('1611', 'Emprunts à long et moyen terme : part à plus d''un an', 'recette', 'investissement', 3, 140, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('1612', 'Emprunts à long et moyen terme : part à moins d''un an', 'recette', 'investissement', 3, 141, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('162', 'Emprunts en devises', 'recette', 'investissement', 2, 142, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('1621', 'Emprunts à long et moyen terme : part à plus d''un an', 'recette', 'investissement', 3, 143, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('1622', 'Emprunts à long et moyen terme : part à moins d''un an', 'recette', 'investissement', 3, 144, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('165', 'Dépôts et cautionnement reçus', 'recette', 'investissement', 2, 145, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('1650', 'Dépôts et cautionnement reçus', 'recette', 'investissement', 3, 146, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('167', 'Dettes sur contrat de location-financement', 'recette', 'investissement', 2, 147, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('1670', 'Dettes sur contrat de location-financement', 'recette', 'investissement', 3, 148, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('168', 'Autres emprunts et dettes assimilés', 'recette', 'investissement', 2, 149, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('1680', 'Autres emprunts et dettes assimilés', 'recette', 'investissement', 3, 150, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('1688', 'Intérêts courus sur emprunts et dettes assimilés', 'recette', 'investissement', 3, 151, false, true);

-- ============================================================================
-- ÉTAPE 4: INSERTION DES RUBRIQUES BUDGÉTAIRES - DÉPENSES
-- ============================================================================

INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('60', 'CHARGES DE PERSONNEL', 'depense', 'fonctionnement', 1, 152, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('601', 'Salaires et accessoires', 'depense', 'fonctionnement', 2, 153, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('6011', 'Personnel permanent', 'depense', 'fonctionnement', 3, 154, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('6012', 'Personnel non permanent', 'depense', 'fonctionnement', 3, 155, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('602', 'Indemnités liées à la solde', 'depense', 'fonctionnement', 2, 156, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('6021', 'Personnel permanent', 'depense', 'fonctionnement', 3, 157, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('6022', 'Personnel non permanent', 'depense', 'fonctionnement', 3, 158, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('603', 'Indemnités et avantages liés à la fonction', 'depense', 'fonctionnement', 2, 159, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('6031', 'Personnel permanent', 'depense', 'fonctionnement', 3, 160, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('6032', 'Personnel non permanent', 'depense', 'fonctionnement', 3, 161, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('604', 'Supplément familial de traitement', 'depense', 'fonctionnement', 2, 162, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('6041', 'Personnel permanent', 'depense', 'fonctionnement', 3, 163, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('6042', 'Personnel non permanent', 'depense', 'fonctionnement', 3, 164, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('606', 'Charges sociales patronales', 'depense', 'fonctionnement', 2, 165, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('6061', 'Cotisations à la CNAPS', 'depense', 'fonctionnement', 3, 166, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('6062', 'Cotisations caisse de retraites civiles et militaires', 'depense', 'fonctionnement', 3, 167, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('6063', 'CPR', 'depense', 'fonctionnement', 3, 168, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('6064', 'Cotisations aux OSIE', 'depense', 'fonctionnement', 3, 169, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('6068', 'Autres charges sociales patronales', 'depense', 'fonctionnement', 3, 170, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('61', 'ACHATS DE BIENS', 'depense', 'fonctionnement', 1, 171, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('611', 'Achats de biens de fonctionnement général', 'depense', 'fonctionnement', 2, 172, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('6111', 'Fournitures et articles de bureau', 'depense', 'fonctionnement', 3, 173, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('6112', 'Imprimés, cachets et docuements administratifs', 'depense', 'fonctionnement', 3, 174, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('6113', 'Consomptibles informatiques', 'depense', 'fonctionnement', 3, 175, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('6114', 'Produits, petits matériels et menues dépenses d''entretien', 'depense', 'fonctionnement', 3, 176, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('6115', 'Petits outillages et fournitures d''atelier', 'depense', 'fonctionnement', 3, 177, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('6116', 'Instruments spécialisés', 'depense', 'fonctionnement', 3, 178, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('6117', 'Habillement', 'depense', 'fonctionnement', 3, 179, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('612', 'Achats de biens à usage spécifique', 'depense', 'fonctionnement', 2, 180, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('6121', 'Fornitures scolaires', 'depense', 'fonctionnement', 3, 181, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('6122', 'Consommables médicaux', 'depense', 'fonctionnement', 3, 182, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('6123', 'Produits pahrmaceutiques', 'depense', 'fonctionnement', 3, 183, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('6124', 'Produits vétérianaires', 'depense', 'fonctionnement', 3, 184, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('6125', 'Produits alimentaires', 'depense', 'fonctionnement', 3, 185, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('6126', 'Intrants agricoles', 'depense', 'fonctionnement', 3, 186, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('6127', 'Fournitures sportives', 'depense', 'fonctionnement', 3, 187, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('6128', 'Fournitures ménagères', 'depense', 'fonctionnement', 3, 188, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('613', 'Carburants, Lubrifiants et combustibles', 'depense', 'fonctionnement', 2, 189, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('6131', 'Carburants et Lubrifiants', 'depense', 'fonctionnement', 3, 190, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('6132', 'Gaz', 'depense', 'fonctionnement', 3, 191, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('6138', 'Autres combustibles', 'depense', 'fonctionnement', 3, 192, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('616', 'Variation de stocks', 'depense', 'fonctionnement', 2, 193, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('6161', 'Variation des stocks de biens de fonctionnement général', 'depense', 'fonctionnement', 3, 194, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('6162', 'Variation des stoccks de biens à usage spécifique', 'depense', 'fonctionnement', 3, 195, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('6163', 'Variation des stocks de carburants, Lubrifiants et combustibles', 'depense', 'fonctionnement', 3, 196, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('6168', 'Variation des staock d''autres achats', 'depense', 'fonctionnement', 3, 197, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('618', 'Autres achats', 'depense', 'fonctionnement', 2, 198, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('6181', 'Achats de matières premières', 'depense', 'fonctionnement', 3, 199, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('6182', 'Achats de marchandises destinées à être revendues', 'depense', 'fonctionnement', 3, 200, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('6183', 'Emballages', 'depense', 'fonctionnement', 3, 201, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('62', 'ACHATS DE SERVICES ET CHARGES PERMANENTES', 'depense', 'fonctionnement', 1, 202, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('621', 'Entretien et maintenance', 'depense', 'fonctionnement', 2, 203, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('6211', 'Entretien de bâtiments', 'depense', 'fonctionnement', 3, 204, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('6212', 'Entretien des autres infrastructures', 'depense', 'fonctionnement', 3, 205, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('6213', 'Entretien de véhicules', 'depense', 'fonctionnement', 3, 206, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('6214', 'Entretien de matériels techniques', 'depense', 'fonctionnement', 3, 207, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('6215', 'Entretien et réparation des matériels et mobiliers de bureau', 'depense', 'fonctionnement', 3, 208, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('6216', 'Entretien et réparation des matériels et mobiliers de logement', 'depense', 'fonctionnement', 3, 209, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('6217', 'Entretien et réparation des matériels et mobiliers scolaires', 'depense', 'fonctionnement', 3, 210, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('6218', 'Maintenance du matériel informatique', 'depense', 'fonctionnement', 3, 211, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('622', 'Charges de représentation, d''information, de documentation et d''encadrement', 'depense', 'fonctionnement', 2, 212, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('6221', 'Fêtes et cérémonies officielles', 'depense', 'fonctionnement', 3, 213, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('6222', 'Charges de représentation : visites officielles', 'depense', 'fonctionnement', 3, 214, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('6223', 'Docuementation et abonnement', 'depense', 'fonctionnement', 3, 215, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('6224', 'Impression, reliures, insertions, publicité et promotion', 'depense', 'fonctionnement', 3, 216, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('6225', 'Frais de Colloques, séminaires, conférences', 'depense', 'fonctionnement', 3, 217, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('6226', 'Foires, exposition', 'depense', 'fonctionnement', 3, 218, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('623', 'Charges de transport', 'depense', 'fonctionnement', 2, 219, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('6231', 'Frais de déplacement intérieur', 'depense', 'fonctionnement', 3, 220, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('6232', 'Frais de déplacement extérieur', 'depense', 'fonctionnement', 3, 221, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('6233', 'Locations de voitures', 'depense', 'fonctionnement', 3, 222, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('6234', 'Transport administratif', 'depense', 'fonctionnement', 3, 223, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('6235', 'Transport de bien', 'depense', 'fonctionnement', 3, 224, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('624', 'Indemnités de mission', 'depense', 'fonctionnement', 2, 225, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('6241', 'Indemnité de mission intérieure', 'depense', 'fonctionnement', 3, 226, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('6242', 'Indemnité de mission extérieure', 'depense', 'fonctionnement', 3, 227, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('6243', 'Viatique', 'depense', 'fonctionnement', 3, 228, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('625', 'Eau et éléctricité', 'depense', 'fonctionnement', 2, 229, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('6250', 'Eau et électricité', 'depense', 'fonctionnement', 3, 230, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('626', 'Poste et télécommunications', 'depense', 'fonctionnement', 2, 231, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('6261', 'Frais postaux', 'depense', 'fonctionnement', 3, 232, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('6262', 'Redevances téléphoniques', 'depense', 'fonctionnement', 3, 233, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('6263', 'Redevances téléphoniques mobiles', 'depense', 'fonctionnement', 3, 234, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('6264', 'Internet', 'depense', 'fonctionnement', 3, 235, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('6265', 'Télex', 'depense', 'fonctionnement', 3, 236, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('6268', 'Autres', 'depense', 'fonctionnement', 3, 237, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('627', 'Charges locatives', 'depense', 'fonctionnement', 2, 238, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('6271', 'Location d''immeuble de bureau', 'depense', 'fonctionnement', 3, 239, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('6272', 'Location d''immeuble de logement', 'depense', 'fonctionnement', 3, 240, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('6273', 'Location d''immeuble de bureau-loggement', 'depense', 'fonctionnement', 3, 241, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('6274', 'Location de terrain', 'depense', 'fonctionnement', 3, 242, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('6275', 'Location de matériels', 'depense', 'fonctionnement', 3, 243, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('6278', 'Autres charges locatives', 'depense', 'fonctionnement', 3, 244, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('628', 'Services divers', 'depense', 'fonctionnement', 2, 245, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('6281', 'Rémunérations d''intermédiaires et honoraires', 'depense', 'fonctionnement', 3, 246, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('6282', 'Frais d''études et de recherche', 'depense', 'fonctionnement', 3, 247, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('6283', 'Frais de stage et de formation', 'depense', 'fonctionnement', 3, 248, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('6284', 'Assurances', 'depense', 'fonctionnement', 3, 249, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('6285', 'Services banciares et assimilés', 'depense', 'fonctionnement', 3, 250, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('6286', 'Cotisations et divers', 'depense', 'fonctionnement', 3, 251, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('6287', 'Personnels extérieurs au service', 'depense', 'fonctionnement', 3, 252, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('6288', 'Contrat de prestation de service', 'depense', 'fonctionnement', 3, 253, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('63', 'DEPENSES D''INTERVENTION', 'depense', 'fonctionnement', 1, 254, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('631', 'Intervention sociale', 'depense', 'fonctionnement', 2, 255, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('6310', 'Intervention sociale', 'depense', 'fonctionnement', 3, 256, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('632', 'Intervention économique', 'depense', 'fonctionnement', 2, 257, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('6320', 'Intervention économique', 'depense', 'fonctionnement', 3, 258, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('633', 'Intervention structurelle', 'depense', 'fonctionnement', 2, 259, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('6330', 'Intervention structurelle', 'depense', 'fonctionnement', 3, 260, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('638', 'Dépenses d''intervention diverses et imprévues', 'depense', 'fonctionnement', 2, 261, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('6380', 'Dépenses d''intervention diverses et imprévues', 'depense', 'fonctionnement', 3, 262, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('64', 'IMPOTS ET TAXES', 'depense', 'fonctionnement', 1, 263, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('641', 'Taxes et impôts directs', 'depense', 'fonctionnement', 2, 264, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('6418', 'Autres taxes et impôts directs', 'depense', 'fonctionnement', 3, 265, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('642', 'Taxes et impôts indirects', 'depense', 'fonctionnement', 2, 266, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('6420', 'Taxes et impôts indirects', 'depense', 'fonctionnement', 3, 267, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('643', 'Impôts, taxes et droits d''enregistrement', 'depense', 'fonctionnement', 2, 268, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('6430', 'Impôts, taxes et droits d''enregistrement', 'depense', 'fonctionnement', 3, 269, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('644', 'Droits à l''importation', 'depense', 'fonctionnement', 2, 270, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('6440', 'Droits à l''importation', 'depense', 'fonctionnement', 3, 271, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('648', 'Impôts, taxes et droits divers', 'depense', 'fonctionnement', 2, 272, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('6480', 'Impôts, taxes et droits divers', 'depense', 'fonctionnement', 3, 273, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('65', 'TRANSFERTS ET SUBVENTIONS', 'depense', 'fonctionnement', 1, 274, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('651', 'Transferts aux collectivités publiques', 'depense', 'fonctionnement', 2, 275, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('6510', 'Transferts aux collectivités publiques', 'depense', 'fonctionnement', 3, 276, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('653', 'Bourses', 'depense', 'fonctionnement', 2, 277, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('6531', 'Bourses à Madagascar', 'depense', 'fonctionnement', 3, 278, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('6532', 'Bourses à l''extérieur', 'depense', 'fonctionnement', 3, 279, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('6533', 'Présalaire, Prêt d''honneur', 'depense', 'fonctionnement', 3, 280, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('6534', 'Prix et récompenses officiels', 'depense', 'fonctionnement', 3, 281, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('654', 'Contributions obligatoires', 'depense', 'fonctionnement', 2, 282, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('6540', 'Contributions obligatoires', 'depense', 'fonctionnement', 3, 283, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('655', 'Transferts aux organismes publics', 'depense', 'fonctionnement', 2, 284, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('6550', 'Transferts aux organismes publics', 'depense', 'fonctionnement', 3, 285, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('656', 'Transferts aux privés', 'depense', 'fonctionnement', 2, 286, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('6561', 'Hospitalisation, traitement et soins', 'depense', 'fonctionnement', 3, 287, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('6562', 'Secours', 'depense', 'fonctionnement', 3, 288, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('6563', 'Indemnisation', 'depense', 'fonctionnement', 3, 289, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('6564', 'Régularisation des droits acquis', 'depense', 'fonctionnement', 3, 290, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('6565', 'Subvention au secteur privé', 'depense', 'fonctionnement', 3, 291, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('66', 'CHARGES FINANCIERES', 'depense', 'fonctionnement', 1, 292, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('661', 'Charges d''intérêt', 'depense', 'fonctionnement', 2, 293, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('6611', 'Intérêts des emprunts', 'depense', 'fonctionnement', 3, 294, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('6618', 'Autres charges d''intérêt', 'depense', 'fonctionnement', 3, 295, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('662', 'Intérêts banciares et opérations de financements à court terme', 'depense', 'fonctionnement', 2, 296, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('6621', 'Intérêts banciares et opérations de financements à court terme', 'depense', 'fonctionnement', 3, 297, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('6622', 'Intérêts des opérations de financements à court terme', 'depense', 'fonctionnement', 3, 298, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('663', 'Intérêts des comptes courants et des dépôts créditeurs', 'depense', 'fonctionnement', 2, 299, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('6631', 'Intérêts des comptes courants', 'depense', 'fonctionnement', 3, 300, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('6632', 'Intérêts des dépôts créditerus', 'depense', 'fonctionnement', 3, 301, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('666', 'Différences de change : pertes', 'depense', 'fonctionnement', 2, 302, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('6660', 'Pertes de changes', 'depense', 'fonctionnement', 3, 303, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('668', 'Autres charges financières', 'depense', 'fonctionnement', 2, 304, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('6681', 'Intérêts des autres dettes', 'depense', 'fonctionnement', 3, 305, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('6688', 'Autres charges financières', 'depense', 'fonctionnement', 3, 306, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('67', 'CHARGES DIVERSES', 'depense', 'fonctionnement', 1, 307, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('671', 'Remise gracieuse, dégrèvement et perte sur titre émis', 'depense', 'fonctionnement', 2, 308, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('6711', 'Remises gracieuses', 'depense', 'fonctionnement', 3, 309, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('6712', 'Dégrèvement sur titres émis', 'depense', 'fonctionnement', 3, 310, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('6713', 'Pertes sur créances irrecouvrables', 'depense', 'fonctionnement', 3, 311, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('6714', 'Perte sur dons extérieurs', 'depense', 'fonctionnement', 3, 312, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('6718', 'Autres', 'depense', 'fonctionnement', 3, 313, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('672', 'Reversement sur trop peçu', 'depense', 'fonctionnement', 2, 314, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('6720', 'Reversement sur trop perçu', 'depense', 'fonctionnement', 3, 315, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('673', 'Déficits budgets annexes', 'depense', 'fonctionnement', 2, 316, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('6730', 'Déficits budgets annexes', 'depense', 'fonctionnement', 3, 317, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('674', 'Frais de justice et de contentieux', 'depense', 'fonctionnement', 2, 318, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('6741', 'Frais de justice', 'depense', 'fonctionnement', 3, 319, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('6742', 'Frais de contentieux', 'depense', 'fonctionnement', 3, 320, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('675', 'Intérêts moratoires, Amendes et Pénalités', 'depense', 'fonctionnement', 2, 321, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('6751', 'Intérêts moratoires, Amendes et Pénalités', 'depense', 'fonctionnement', 3, 322, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('6752', 'Amendes', 'depense', 'fonctionnement', 3, 323, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('6753', 'Pénalités', 'depense', 'fonctionnement', 3, 324, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('678', 'Autres charges diverses', 'depense', 'fonctionnement', 2, 325, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('6781', 'Moins-values sur cessions d''immobilisations', 'depense', 'fonctionnement', 3, 326, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('6782', 'Quotes-part de résultat sur opérations faites en commun', 'depense', 'fonctionnement', 3, 327, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('6788', 'Autres', 'depense', 'fonctionnement', 3, 328, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('16', 'EMPRUNTS ET DETTES ASSIMILEES', 'depense', 'investissement', 1, 329, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('161', 'Emprunts en Ariary', 'depense', 'investissement', 2, 330, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('1611', 'Emprunts à long et moyen terme : part à plus d''un an', 'depense', 'investissement', 3, 331, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('1612', 'Emprunts à long et moyen terme : part à moins d''un an', 'depense', 'investissement', 3, 332, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('162', 'Emprunts en devises', 'depense', 'investissement', 2, 333, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('1621', 'Emprunts à long et moyen terme : part à plus d''un an', 'depense', 'investissement', 3, 334, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('1622', 'Emprunts à long et moyen terme : part à moins d''un an', 'depense', 'investissement', 3, 335, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('165', 'Dépôts et cautionnement reçus', 'depense', 'investissement', 2, 336, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('1650', 'Dépôts et cautionnement reçus', 'depense', 'investissement', 3, 337, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('167', 'Dettes sur contrat de location-financement', 'depense', 'investissement', 2, 338, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('1670', 'Dettes sur contrat de location-financement', 'depense', 'investissement', 3, 339, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('168', 'Autres emprunts et dettes assimilés', 'depense', 'investissement', 2, 340, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('1680', 'Autres emprunts et dettes assimilés', 'depense', 'investissement', 3, 341, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('1688', 'Intérêts courus sur emprunts et dettes assimilés', 'depense', 'investissement', 3, 342, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('20', 'IMMOBILISATION INCORPORELLES', 'depense', 'investissement', 1, 343, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('201', 'Frais de développement, de recherche et d''études', 'depense', 'investissement', 2, 344, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('2011', 'Formation', 'depense', 'investissement', 3, 345, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('2012', 'Animation et encadrement', 'depense', 'investissement', 3, 346, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('2013', 'Assistance technique', 'depense', 'investissement', 3, 347, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('2014', 'Logiciels informatiques et assimilés', 'depense', 'investissement', 3, 348, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('2015', 'Etudes et recherches', 'depense', 'investissement', 3, 349, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('2016', 'Suivi - Contrôle - Evaluations', 'depense', 'investissement', 3, 350, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('2017', 'Frais de pré-exploitation', 'depense', 'investissement', 3, 351, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('2018', 'Autres', 'depense', 'investissement', 3, 352, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('205', 'Concessions et droits similaires, brevets, licences, marques', 'depense', 'investissement', 2, 353, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('2051', 'Concessions et droits similaires', 'depense', 'investissement', 3, 354, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('2052', 'Brevets, licences, marques', 'depense', 'investissement', 3, 355, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('208', 'Autres immoblisations incorporelles', 'depense', 'investissement', 2, 356, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('2080', 'Autres immoblisations incorporelles', 'depense', 'investissement', 3, 357, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('21', 'IMMOBILISATION CORPORELLES', 'depense', 'investissement', 1, 358, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('211', 'Terrains', 'depense', 'investissement', 2, 359, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('2111', 'Terrains nus', 'depense', 'investissement', 3, 360, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('2112', 'Terrains bâtis', 'depense', 'investissement', 3, 361, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('2113', 'Terrains de gisement', 'depense', 'investissement', 3, 362, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('2114', 'Terrains de chantiers', 'depense', 'investissement', 3, 363, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('2115', 'Terrains de voiries', 'depense', 'investissement', 3, 364, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('2116', 'Cimetières', 'depense', 'investissement', 3, 365, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('2117', 'Bois et forêts', 'depense', 'investissement', 3, 366, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('2118', 'Autres', 'depense', 'investissement', 3, 367, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('212', 'Aménagement', 'depense', 'investissement', 2, 368, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('2121', 'Aménagement de terrain', 'depense', 'investissement', 3, 369, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('2122', 'Aménagement des aérodromes', 'depense', 'investissement', 3, 370, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('2123', 'Aménagement des ports', 'depense', 'investissement', 3, 371, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('2124', 'Travaux d''irrigation', 'depense', 'investissement', 3, 372, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('2125', 'Travaus d''urbanisme', 'depense', 'investissement', 3, 373, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('2128', 'Autres aménagements', 'depense', 'investissement', 3, 374, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('213', 'Construction ou Réhabilitation : Bâtiments', 'depense', 'investissement', 2, 375, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('2131', 'Batiments administratifs', 'depense', 'investissement', 3, 376, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('2132', 'Bâtiments scolaires', 'depense', 'investissement', 3, 377, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('2133', 'Batiments de cnetres de soins de santé', 'depense', 'investissement', 3, 378, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('2134', 'Autres bâtiments techniques', 'depense', 'investissement', 3, 379, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('2137', 'Installations, agencemetns et aménagements - Bâtiments', 'depense', 'investissement', 3, 380, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('2138', 'Autres constructions ou réhabilitations - Bâtiments', 'depense', 'investissement', 3, 381, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('214', 'Construction ou Réhabilitation : Voies', 'depense', 'investissement', 2, 382, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('2141', 'Routes', 'depense', 'investissement', 3, 383, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('2142', 'Voies ferrées', 'depense', 'investissement', 3, 384, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('2143', 'Voies d''eau', 'depense', 'investissement', 3, 385, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('2144', 'Pistes d''aérodrome', 'depense', 'investissement', 3, 386, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('2147', 'Installations, agencements et aménagements - Voies', 'depense', 'investissement', 3, 387, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('2148', 'Autres constructions ou réhabilitations - Voies', 'depense', 'investissement', 3, 388, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('215', 'Construction ou Réhabilitation : Réseaux', 'depense', 'investissement', 2, 389, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('2151', 'Réseau d''aduction d''eau', 'depense', 'investissement', 3, 390, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('2152', 'Réseau d''assainissement', 'depense', 'investissement', 3, 391, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('2153', 'Réseau téléphonique', 'depense', 'investissement', 3, 392, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('2154', 'Réseau de communication', 'depense', 'investissement', 3, 393, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('2155', 'Réseau d''électricité', 'depense', 'investissement', 3, 394, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('2156', 'Réseau d''irrigation', 'depense', 'investissement', 3, 395, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('2157', 'Installations, agencements et aménagements - Réseaux', 'depense', 'investissement', 3, 396, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('2158', 'Autres constructions ou réhabilitations - Réseaux', 'depense', 'investissement', 3, 397, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('216', 'Matériels et outillages', 'depense', 'investissement', 2, 398, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('2161', 'Matériels techniques', 'depense', 'investissement', 3, 399, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('2162', 'Matériels agricoles', 'depense', 'investissement', 3, 400, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('2163', 'Matériels informatiques', 'depense', 'investissement', 3, 401, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('2164', 'Matériels et mobiliers de bureau', 'depense', 'investissement', 3, 402, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('2165', 'Matériels et mobiliers de logement', 'depense', 'investissement', 3, 403, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('2166', 'Matériels et mobiliers scolaires', 'depense', 'investissement', 3, 404, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('2167', 'Outillages', 'depense', 'investissement', 3, 405, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('2168', 'Autres matériels et outillages', 'depense', 'investissement', 3, 406, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('217', 'Matériels de transoport', 'depense', 'investissement', 2, 407, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('2171', 'Renouvellement des vehicules du parc administratif', 'depense', 'investissement', 3, 408, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('2172', 'Matériel automobile', 'depense', 'investissement', 3, 409, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('2173', 'Matériel fluvial', 'depense', 'investissement', 3, 410, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('2174', 'Matériel ferroviaire', 'depense', 'investissement', 3, 411, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('2175', 'Matériel naval', 'depense', 'investissement', 3, 412, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('2176', 'Matériel aérien', 'depense', 'investissement', 3, 413, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('2178', 'Autres moyens de locomotion', 'depense', 'investissement', 3, 414, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('218', 'Autres immobilisations corporelles', 'depense', 'investissement', 2, 415, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('2181', 'Cheptel', 'depense', 'investissement', 3, 416, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('2182', 'Emballages récupérables', 'depense', 'investissement', 3, 417, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('2183', 'Installations complexes spécialisées', 'depense', 'investissement', 3, 418, false, true);
INSERT INTO rubriques_budgetaires (code, intitule, type, section, niveau, ordre, est_calculee, est_active) VALUES
('2188', 'Autres immobilisations corporelles', 'depense', 'investissement', 3, 419, false, true);

-- ============================================================================
-- ÉTAPE 5: VÉRIFICATIONS
-- ============================================================================

-- Vérifier les colonnes dynamiques
SELECT 
    applicable_a,
    COUNT(*) as nb_colonnes
FROM colonnes_dynamiques
WHERE est_active = true
GROUP BY applicable_a
ORDER BY applicable_a;

-- Vérifier les rubriques budgétaires
SELECT 
    type,
    section,
    COUNT(*) as nb_rubriques
FROM rubriques_budgetaires
WHERE est_active = true
GROUP BY type, section
ORDER BY type, section;

-- Afficher quelques recettes
SELECT code, intitule, section, niveau
FROM rubriques_budgetaires
WHERE type = 'recette'
ORDER BY ordre
LIMIT 10;

-- Afficher quelques dépenses
SELECT code, intitule, section, niveau
FROM rubriques_budgetaires
WHERE type = 'depense'
ORDER BY ordre
LIMIT 10;

-- Vérifier qu'il n'y a pas de doublons
SELECT code, type, COUNT(*) as nb
FROM rubriques_budgetaires
GROUP BY code, type
HAVING COUNT(*) > 1;

-- ============================================================================
-- FIN DU SCRIPT
-- ============================================================================

/*
✅ CORRECTIONS APPORTÉES:

1. Suppression de 16 doublons détectés dans le fichier Excel:
   - 14 doublons dans les RECETTES (codes: 10, 101, 1011-1018, 106, 1061, 1064, 1068)
   - 2 doublons dans les DÉPENSES (codes: 20, 21)

2. Total de rubriques après nettoyage: 420 rubriques uniques
   - 152 recettes
   - 268 dépenses

INSTRUCTIONS D'UTILISATION:

1. Exécutez ce script dans Supabase SQL Editor

2. Vérifiez l'absence de doublons avec la dernière requête

3. Exécutez ensuite le script 004_seed_donnees_test.sql pour créer des données de test

4. Utilisez l'interface web pour:
   - Saisir les lignes budgétaires: /admin/comptes-administratifs/lignes-budgetaires
   - Visualiser le tableau d'équilibre: /admin/comptes-administratifs/equilibre
*/
