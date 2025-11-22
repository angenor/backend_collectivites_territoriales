"""
Modèles pour la hiérarchie géographique de Madagascar
"""

import uuid
from sqlalchemy import Column, String, Text, Integer, Numeric, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.models.base import Base, TimestampMixin, ActiveMixin


class Region(Base, TimestampMixin, ActiveMixin):
    """Régions administratives de Madagascar (22 régions)"""
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
