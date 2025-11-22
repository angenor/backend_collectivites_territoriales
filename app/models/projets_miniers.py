"""
Modèles pour les projets miniers et sociétés
"""

import uuid
from sqlalchemy import Column, String, Text, Date, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.models.base import Base, TimestampMixin, ActiveMixin


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
