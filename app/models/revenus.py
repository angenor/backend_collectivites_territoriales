"""
Modèles pour la gestion des revenus (cœur du système)
"""

import uuid
from sqlalchemy import Column, String, Text, Date, Integer, Numeric, Boolean, DateTime, ForeignKey, Index
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship

from app.models.base import Base, TimestampMixin, ActiveMixin


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
