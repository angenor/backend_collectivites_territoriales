"""
Modèles SQLAlchemy pour la plateforme de suivi des revenus miniers
Base de données: PostgreSQL avec FastAPI
"""

from datetime import datetime
from typing import List, Optional
from sqlalchemy import (
    Boolean, Column, DateTime, Integer, String, Text, Numeric,
    ForeignKey, Date, ARRAY, Index, text
)
from sqlalchemy.dialects.postgresql import UUID, JSONB, INET
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import uuid

Base = declarative_base()


# ============================================================================
# MIXINS
# ============================================================================

class TimestampMixin:
    """Mixin pour ajouter les timestamps created_at et updated_at"""
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False
    )


class ActiveMixin:
    """Mixin pour le soft delete"""
    actif = Column(Boolean, default=True, nullable=False)


# ============================================================================
# TABLES DE RÉFÉRENCE GÉOGRAPHIQUE
# ============================================================================

class Region(Base, TimestampMixin, ActiveMixin):
    """Régions administratives de Madagascar"""
    __tablename__ = "regions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    code = Column(String(10), unique=True, nullable=False, index=True)
    nom = Column(String(255), nullable=False)
    description = Column(Text)

    # Relations
    departements = relationship("Departement", back_populates="region", cascade="all, delete-orphan")
    communes = relationship("Commune", back_populates="region", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Region(code='{self.code}', nom='{self.nom}')>"


class Departement(Base, TimestampMixin, ActiveMixin):
    """Départements/Districts administratifs"""
    __tablename__ = "departements"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    code = Column(String(10), unique=True, nullable=False, index=True)
    nom = Column(String(255), nullable=False)
    region_id = Column(UUID(as_uuid=True), ForeignKey("regions.id", ondelete="CASCADE"), nullable=False)
    description = Column(Text)

    # Relations
    region = relationship("Region", back_populates="departements")
    communes = relationship("Commune", back_populates="departement", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Departement(code='{self.code}', nom='{self.nom}')>"


class Commune(Base, TimestampMixin, ActiveMixin):
    """Communes bénéficiaires des revenus miniers"""
    __tablename__ = "communes"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    code = Column(String(10), unique=True, nullable=False, index=True)
    nom = Column(String(255), nullable=False)
    departement_id = Column(UUID(as_uuid=True), ForeignKey("departements.id", ondelete="CASCADE"), nullable=False)
    region_id = Column(UUID(as_uuid=True), ForeignKey("regions.id", ondelete="CASCADE"), nullable=False)
    population = Column(Integer)
    superficie = Column(Numeric(10, 2))
    description = Column(Text)

    # Relations
    departement = relationship("Departement", back_populates="communes")
    region = relationship("Region", back_populates="communes")
    projets_miniers = relationship("ProjetMinier", back_populates="commune", cascade="all, delete-orphan")
    revenus = relationship("Revenu", back_populates="commune", cascade="all, delete-orphan")
    documents = relationship("Document", back_populates="commune", cascade="all, delete-orphan")
    utilisateurs = relationship("Utilisateur", back_populates="commune")
    messages_securises = relationship("MessageSecurise", back_populates="commune")

    def __repr__(self):
        return f"<Commune(code='{self.code}', nom='{self.nom}')>"


# ============================================================================
# TABLES DES PROJETS MINIERS
# ============================================================================

class TypeMinerai(Base, TimestampMixin, ActiveMixin):
    """Types de minerais exploités"""
    __tablename__ = "types_minerais"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    code = Column(String(50), unique=True, nullable=False, index=True)
    nom = Column(String(255), nullable=False)
    description = Column(Text)

    # Relations
    projets_miniers = relationship("ProjetMinier", back_populates="type_minerai")

    def __repr__(self):
        return f"<TypeMinerai(code='{self.code}', nom='{self.nom}')>"


class SocieteMiniere(Base, TimestampMixin, ActiveMixin):
    """Sociétés minières exploitantes"""
    __tablename__ = "societes_minieres"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    code = Column(String(50), unique=True, nullable=False, index=True)
    nom = Column(String(255), nullable=False)
    raison_sociale = Column(String(255))
    nif = Column(String(50))
    stat = Column(String(50))
    adresse = Column(Text)
    telephone = Column(String(50))
    email = Column(String(255))

    # Relations
    projets_miniers = relationship("ProjetMinier", back_populates="societe_miniere", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<SocieteMiniere(code='{self.code}', nom='{self.nom}')>"


class ProjetMinier(Base, TimestampMixin, ActiveMixin):
    """Projets d'extraction minière sources de revenus"""
    __tablename__ = "projets_miniers"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    code = Column(String(50), unique=True, nullable=False, index=True)
    nom = Column(String(255), nullable=False)
    societe_miniere_id = Column(UUID(as_uuid=True), ForeignKey("societes_minieres.id", ondelete="CASCADE"), nullable=False)
    type_minerai_id = Column(UUID(as_uuid=True), ForeignKey("types_minerais.id", ondelete="RESTRICT"), nullable=False)
    commune_id = Column(UUID(as_uuid=True), ForeignKey("communes.id", ondelete="CASCADE"), nullable=False)
    date_debut = Column(Date)
    date_fin = Column(Date)
    statut = Column(String(50), default="actif")  # actif, suspendu, terminé
    description = Column(Text)

    # Relations
    societe_miniere = relationship("SocieteMiniere", back_populates="projets_miniers")
    type_minerai = relationship("TypeMinerai", back_populates="projets_miniers")
    commune = relationship("Commune", back_populates="projets_miniers")
    revenus = relationship("Revenu", back_populates="projet_minier")

    def __repr__(self):
        return f"<ProjetMinier(code='{self.code}', nom='{self.nom}')>"


# ============================================================================
# TABLES DE GESTION DES REVENUS
# ============================================================================

class Exercice(Base, TimestampMixin, ActiveMixin):
    """Exercices fiscaux"""
    __tablename__ = "exercices"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    annee = Column(Integer, unique=True, nullable=False, index=True)
    date_debut = Column(Date, nullable=False)
    date_fin = Column(Date, nullable=False)
    statut = Column(String(50), default="ouvert")  # ouvert, cloturé

    # Relations
    periodes = relationship("Periode", back_populates="exercice", cascade="all, delete-orphan")
    documents = relationship("Document", back_populates="exercice")
    logs_telechargements = relationship("LogTelechargement", back_populates="exercice")

    def __repr__(self):
        return f"<Exercice(annee={self.annee}, statut='{self.statut}')>"


class Periode(Base, TimestampMixin, ActiveMixin):
    """Périodes (colonnes du tableau)"""
    __tablename__ = "periodes"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    code = Column(String(50), nullable=False)
    nom = Column(String(255), nullable=False)
    exercice_id = Column(UUID(as_uuid=True), ForeignKey("exercices.id", ondelete="CASCADE"), nullable=False)
    date_debut = Column(Date, nullable=False)
    date_fin = Column(Date, nullable=False)
    type_periode = Column(String(50))  # mensuel, trimestriel, semestriel, annuel
    ordre = Column(Integer)

    # Relations
    exercice = relationship("Exercice", back_populates="periodes")
    revenus = relationship("Revenu", back_populates="periode", cascade="all, delete-orphan")

    # Contrainte unique
    __table_args__ = (
        Index('idx_periode_exercice_code', 'exercice_id', 'code', unique=True),
    )

    def __repr__(self):
        return f"<Periode(code='{self.code}', nom='{self.nom}')>"


class CategorieRubrique(Base, TimestampMixin, ActiveMixin):
    """Catégories de rubriques pour organisation"""
    __tablename__ = "categories_rubriques"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    code = Column(String(50), unique=True, nullable=False, index=True)
    nom = Column(String(255), nullable=False)
    description = Column(Text)
    ordre = Column(Integer)

    # Relations
    rubriques = relationship("Rubrique", back_populates="categorie")

    def __repr__(self):
        return f"<CategorieRubrique(code='{self.code}', nom='{self.nom}')>"


class Rubrique(Base, TimestampMixin, ActiveMixin):
    """Rubriques (lignes du tableau) - structure hiérarchique flexible"""
    __tablename__ = "rubriques"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    code = Column(String(50), unique=True, nullable=False, index=True)
    nom = Column(String(255), nullable=False)
    categorie_id = Column(UUID(as_uuid=True), ForeignKey("categories_rubriques.id", ondelete="SET NULL"))
    parent_id = Column(UUID(as_uuid=True), ForeignKey("rubriques.id", ondelete="CASCADE"))
    niveau = Column(Integer, default=1)
    ordre = Column(Integer)
    type = Column(String(50))  # recette, depense, solde, autre
    formule = Column(Text)  # Formule de calcul si applicable (JSON)
    est_calculee = Column(Boolean, default=False)
    afficher_total = Column(Boolean, default=True)
    description = Column(Text)

    # Relations
    categorie = relationship("CategorieRubrique", back_populates="rubriques")
    parent = relationship("Rubrique", remote_side=[id], backref="sous_rubriques")
    revenus = relationship("Revenu", back_populates="rubrique", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Rubrique(code='{self.code}', nom='{self.nom}', type='{self.type}')>"


class Revenu(Base, TimestampMixin):
    """Données de revenus - cœur du système"""
    __tablename__ = "revenus"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    commune_id = Column(UUID(as_uuid=True), ForeignKey("communes.id", ondelete="CASCADE"), nullable=False)
    rubrique_id = Column(UUID(as_uuid=True), ForeignKey("rubriques.id", ondelete="CASCADE"), nullable=False)
    periode_id = Column(UUID(as_uuid=True), ForeignKey("periodes.id", ondelete="CASCADE"), nullable=False)
    projet_minier_id = Column(UUID(as_uuid=True), ForeignKey("projets_miniers.id", ondelete="SET NULL"))

    montant = Column(Numeric(15, 2), nullable=False, default=0)
    montant_prevu = Column(Numeric(15, 2))
    ecart = Column(Numeric(15, 2))
    taux_realisation = Column(Numeric(5, 2))

    observations = Column(Text)
    documents = Column(JSONB)  # Références aux documents justificatifs

    valide = Column(Boolean, default=False)
    valide_par = Column(UUID(as_uuid=True), ForeignKey("utilisateurs.id", ondelete="SET NULL"))
    valide_le = Column(DateTime)

    created_by = Column(UUID(as_uuid=True), ForeignKey("utilisateurs.id", ondelete="SET NULL"))
    updated_by = Column(UUID(as_uuid=True), ForeignKey("utilisateurs.id", ondelete="SET NULL"))

    # Relations
    commune = relationship("Commune", back_populates="revenus")
    rubrique = relationship("Rubrique", back_populates="revenus")
    periode = relationship("Periode", back_populates="revenus")
    projet_minier = relationship("ProjetMinier", back_populates="revenus")
    validateur = relationship("Utilisateur", foreign_keys=[valide_par])
    createur = relationship("Utilisateur", foreign_keys=[created_by])
    modificateur = relationship("Utilisateur", foreign_keys=[updated_by])
    valeurs_colonnes = relationship("ValeurColonnePersonnalisee", back_populates="revenu", cascade="all, delete-orphan")

    # Index et contraintes
    __table_args__ = (
        Index('idx_revenus_commune', 'commune_id'),
        Index('idx_revenus_rubrique', 'rubrique_id'),
        Index('idx_revenus_periode', 'periode_id'),
        Index('idx_revenus_projet', 'projet_minier_id'),
        Index('idx_revenus_unique', 'commune_id', 'rubrique_id', 'periode_id', 'projet_minier_id', unique=True),
    )

    def __repr__(self):
        return f"<Revenu(commune_id={self.commune_id}, montant={self.montant})>"


# ============================================================================
# TABLES DE CONFIGURATION DYNAMIQUE
# ============================================================================

class ColonnePersonnalisee(Base, TimestampMixin, ActiveMixin):
    """Colonnes personnalisées pour extensibilité du tableau"""
    __tablename__ = "colonnes_personnalisees"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    code = Column(String(50), unique=True, nullable=False, index=True)
    nom = Column(String(255), nullable=False)
    type_donnee = Column(String(50))  # text, number, date, boolean, json
    ordre = Column(Integer)
    obligatoire = Column(Boolean, default=False)
    visible = Column(Boolean, default=True)
    editable = Column(Boolean, default=True)
    valeur_defaut = Column(Text)

    # Relations
    valeurs = relationship("ValeurColonnePersonnalisee", back_populates="colonne", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<ColonnePersonnalisee(code='{self.code}', nom='{self.nom}')>"


class ValeurColonnePersonnalisee(Base, TimestampMixin):
    """Valeurs pour les colonnes personnalisées"""
    __tablename__ = "valeurs_colonnes_personnalisees"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    colonne_id = Column(UUID(as_uuid=True), ForeignKey("colonnes_personnalisees.id", ondelete="CASCADE"), nullable=False)
    revenu_id = Column(UUID(as_uuid=True), ForeignKey("revenus.id", ondelete="CASCADE"), nullable=False)
    valeur = Column(Text)

    # Relations
    colonne = relationship("ColonnePersonnalisee", back_populates="valeurs")
    revenu = relationship("Revenu", back_populates="valeurs_colonnes")

    # Contrainte unique
    __table_args__ = (
        Index('idx_valeur_colonne_revenu', 'colonne_id', 'revenu_id', unique=True),
    )

    def __repr__(self):
        return f"<ValeurColonnePersonnalisee(colonne_id={self.colonne_id}, valeur='{self.valeur}')>"


# ============================================================================
# TABLES DE GESTION DES UTILISATEURS
# ============================================================================

class Role(Base, TimestampMixin, ActiveMixin):
    """Rôles des utilisateurs avec permissions"""
    __tablename__ = "roles"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    code = Column(String(50), unique=True, nullable=False, index=True)
    nom = Column(String(255), nullable=False)
    description = Column(Text)
    permissions = Column(JSONB)  # Liste des permissions en JSON

    # Relations
    utilisateurs = relationship("Utilisateur", back_populates="role")

    def __repr__(self):
        return f"<Role(code='{self.code}', nom='{self.nom}')>"


class Utilisateur(Base, TimestampMixin, ActiveMixin):
    """Utilisateurs de la plateforme (administrateurs et éditeurs)"""
    __tablename__ = "utilisateurs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, nullable=False, index=True)
    username = Column(String(100), unique=True, nullable=False, index=True)
    nom = Column(String(255), nullable=False)
    prenom = Column(String(255))
    password_hash = Column(String(255), nullable=False)
    role_id = Column(UUID(as_uuid=True), ForeignKey("roles.id", ondelete="RESTRICT"), nullable=False)
    commune_id = Column(UUID(as_uuid=True), ForeignKey("communes.id", ondelete="SET NULL"))
    telephone = Column(String(50))
    dernier_login = Column(DateTime)
    email_verifie = Column(Boolean, default=False)
    token_verification = Column(String(255))
    token_reset_password = Column(String(255))
    token_expiration = Column(DateTime)

    # Relations
    role = relationship("Role", back_populates="utilisateurs")
    commune = relationship("Commune", back_populates="utilisateurs")
    documents_uploadés = relationship("Document", foreign_keys="Document.uploaded_by", back_populates="uploader")
    logs_visites = relationship("LogVisite", back_populates="utilisateur")
    logs_telechargements = relationship("LogTelechargement", back_populates="utilisateur")
    logs_activites = relationship("LogActivite", back_populates="utilisateur")
    messages_envoyes = relationship("MessageSecurise", foreign_keys="MessageSecurise.expediteur_id", back_populates="expediteur")
    messages_recus = relationship("MessageSecurise", foreign_keys="MessageSecurise.destinataire_id", back_populates="destinataire")
    campagnes_newsletter = relationship("NewsletterCampagne", back_populates="createur")

    def __repr__(self):
        return f"<Utilisateur(username='{self.username}', email='{self.email}')>"


# ============================================================================
# TABLES DE GESTION DES DOCUMENTS
# ============================================================================

class TypeDocument(Base, TimestampMixin, ActiveMixin):
    """Types de documents avec contraintes"""
    __tablename__ = "types_documents"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    code = Column(String(50), unique=True, nullable=False, index=True)
    nom = Column(String(255), nullable=False)
    description = Column(Text)
    extensions_autorisees = Column(ARRAY(Text))  # ['.pdf', '.xlsx', '.docx']
    taille_max_mo = Column(Integer, default=10)

    # Relations
    documents = relationship("Document", back_populates="type_document")

    def __repr__(self):
        return f"<TypeDocument(code='{self.code}', nom='{self.nom}')>"


class Document(Base, TimestampMixin):
    """Documents justificatifs avec indexation full-text"""
    __tablename__ = "documents"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    titre = Column(String(255), nullable=False)
    nom_fichier = Column(String(255), nullable=False)
    chemin_fichier = Column(Text, nullable=False)
    type_document_id = Column(UUID(as_uuid=True), ForeignKey("types_documents.id", ondelete="SET NULL"))
    taille_ko = Column(Integer)
    extension = Column(String(10))
    commune_id = Column(UUID(as_uuid=True), ForeignKey("communes.id", ondelete="CASCADE"))
    exercice_id = Column(UUID(as_uuid=True), ForeignKey("exercices.id", ondelete="CASCADE"))
    revenu_id = Column(UUID(as_uuid=True), ForeignKey("revenus.id", ondelete="CASCADE"))
    description = Column(Text)
    tags = Column(ARRAY(Text))
    indexe = Column(Boolean, default=False)
    contenu_texte = Column(Text)  # Contenu extrait pour la recherche
    uploaded_by = Column(UUID(as_uuid=True), ForeignKey("utilisateurs.id", ondelete="SET NULL"))

    # Relations
    type_document = relationship("TypeDocument", back_populates="documents")
    commune = relationship("Commune", back_populates="documents")
    exercice = relationship("Exercice", back_populates="documents")
    uploader = relationship("Utilisateur", back_populates="documents_uploadés")
    logs_telechargements = relationship("LogTelechargement", back_populates="document")

    # Index pour la recherche
    __table_args__ = (
        Index('idx_documents_tags', 'tags', postgresql_using='gin'),
    )

    def __repr__(self):
        return f"<Document(titre='{self.titre}', nom_fichier='{self.nom_fichier}')>"


# ============================================================================
# TABLES DE NEWSLETTER
# ============================================================================

class NewsletterAbonne(Base, TimestampMixin, ActiveMixin):
    """Abonnés à la newsletter"""
    __tablename__ = "newsletter_abonnes"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, nullable=False, index=True)
    nom = Column(String(255))
    prenom = Column(String(255))
    token_confirmation = Column(String(255))
    confirme = Column(Boolean, default=False)
    confirme_le = Column(DateTime)

    def __repr__(self):
        return f"<NewsletterAbonne(email='{self.email}', confirme={self.confirme})>"


class NewsletterCampagne(Base, TimestampMixin):
    """Campagnes d'envoi de newsletter"""
    __tablename__ = "newsletter_campagnes"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    titre = Column(String(255), nullable=False)
    sujet = Column(String(255), nullable=False)
    contenu = Column(Text, nullable=False)
    date_envoi = Column(DateTime)
    statut = Column(String(50), default="brouillon")  # brouillon, programmée, envoyée
    nb_destinataires = Column(Integer)
    nb_envoyes = Column(Integer, default=0)
    nb_ouverts = Column(Integer, default=0)
    nb_clics = Column(Integer, default=0)
    created_by = Column(UUID(as_uuid=True), ForeignKey("utilisateurs.id", ondelete="SET NULL"))

    # Relations
    createur = relationship("Utilisateur", back_populates="campagnes_newsletter")

    def __repr__(self):
        return f"<NewsletterCampagne(titre='{self.titre}', statut='{self.statut}')>"


# ============================================================================
# TABLES DE LOGS ET STATISTIQUES
# ============================================================================

class LogVisite(Base):
    """Logs de visites du site"""
    __tablename__ = "logs_visites"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    page = Column(String(255))
    utilisateur_id = Column(UUID(as_uuid=True), ForeignKey("utilisateurs.id", ondelete="SET NULL"))
    ip_adresse = Column(INET)
    user_agent = Column(Text)
    session_id = Column(String(255))
    duree_secondes = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relations
    utilisateur = relationship("Utilisateur", back_populates="logs_visites")

    def __repr__(self):
        return f"<LogVisite(page='{self.page}', created_at={self.created_at})>"


class LogTelechargement(Base):
    """Logs de téléchargements"""
    __tablename__ = "logs_telechargements"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    document_id = Column(UUID(as_uuid=True), ForeignKey("documents.id", ondelete="SET NULL"))
    type_export = Column(String(50))  # excel, word, pdf
    commune_id = Column(UUID(as_uuid=True), ForeignKey("communes.id", ondelete="SET NULL"))
    exercice_id = Column(UUID(as_uuid=True), ForeignKey("exercices.id", ondelete="SET NULL"))
    utilisateur_id = Column(UUID(as_uuid=True), ForeignKey("utilisateurs.id", ondelete="SET NULL"))
    ip_adresse = Column(INET)
    user_agent = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relations
    document = relationship("Document", back_populates="logs_telechargements")
    commune = relationship("Commune")
    exercice = relationship("Exercice", back_populates="logs_telechargements")
    utilisateur = relationship("Utilisateur", back_populates="logs_telechargements")

    def __repr__(self):
        return f"<LogTelechargement(type_export='{self.type_export}', created_at={self.created_at})>"


class LogActivite(Base):
    """Logs d'activité système pour audit"""
    __tablename__ = "logs_activites"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    utilisateur_id = Column(UUID(as_uuid=True), ForeignKey("utilisateurs.id", ondelete="SET NULL"))
    action = Column(String(100), nullable=False)  # CREATE, UPDATE, DELETE, LOGIN, LOGOUT
    entite = Column(String(100))  # nom de la table concernée
    entite_id = Column(UUID(as_uuid=True))
    anciennes_valeurs = Column(JSONB)
    nouvelles_valeurs = Column(JSONB)
    ip_adresse = Column(INET)
    user_agent = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)

    # Relations
    utilisateur = relationship("Utilisateur", back_populates="logs_activites")

    # Index
    __table_args__ = (
        Index('idx_logs_activites_utilisateur', 'utilisateur_id'),
        Index('idx_logs_activites_action', 'action'),
    )

    def __repr__(self):
        return f"<LogActivite(action='{self.action}', entite='{self.entite}')>"


# ============================================================================
# TABLES POUR ÉCHANGE SÉCURISÉ D'INFORMATIONS
# ============================================================================

class MessageSecurise(Base, TimestampMixin):
    """Messages sécurisés entre utilisateurs"""
    __tablename__ = "messages_securises"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    sujet = Column(String(255), nullable=False)
    contenu = Column(Text, nullable=False)
    expediteur_id = Column(UUID(as_uuid=True), ForeignKey("utilisateurs.id", ondelete="SET NULL"))
    destinataire_id = Column(UUID(as_uuid=True), ForeignKey("utilisateurs.id", ondelete="CASCADE"), nullable=False)
    commune_id = Column(UUID(as_uuid=True), ForeignKey("communes.id", ondelete="SET NULL"))
    lu = Column(Boolean, default=False)
    lu_le = Column(DateTime)
    priorite = Column(String(50), default="normale")  # basse, normale, haute, urgente
    fichiers_joints = Column(JSONB)
    archive = Column(Boolean, default=False)

    # Relations
    expediteur = relationship("Utilisateur", foreign_keys=[expediteur_id], back_populates="messages_envoyes")
    destinataire = relationship("Utilisateur", foreign_keys=[destinataire_id], back_populates="messages_recus")
    commune = relationship("Commune", back_populates="messages_securises")

    def __repr__(self):
        return f"<MessageSecurise(sujet='{self.sujet}', lu={self.lu})>"
