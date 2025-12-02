"""
Geographic models for Madagascar administrative hierarchy.
Province → Region → Commune
"""

from decimal import Decimal
from typing import TYPE_CHECKING, List, Optional

from sqlalchemy import Enum, ForeignKey, Index, Integer, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from app.models.base import TimestampMixin
from app.models.enums import TypeCommune

if TYPE_CHECKING:
    from app.models.utilisateurs import Utilisateur
    from app.models.comptabilite import DonneesRecettes, DonneesDepenses
    from app.models.projets_miniers import ProjetCommune, RevenuMinier
    from app.models.documents import Document
    from app.models.cms import PageCompteAdministratif
    from app.models.annexes import StatistiqueVisite


class Province(Base, TimestampMixin):
    """
    Les 6 provinces de Madagascar.
    Premier niveau de la hiérarchie administrative.
    """
    __tablename__ = "provinces"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    code: Mapped[str] = mapped_column(String(10), unique=True, nullable=False)
    nom: Mapped[str] = mapped_column(String(100), nullable=False)

    # Relations
    regions: Mapped[List["Region"]] = relationship(
        "Region",
        back_populates="province",
        cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<Province(id={self.id}, code='{self.code}', nom='{self.nom}')>"


class Region(Base, TimestampMixin):
    """
    Les 22 régions de Madagascar.
    Deuxième niveau de la hiérarchie administrative.
    """
    __tablename__ = "regions"
    __table_args__ = (
        Index("idx_regions_province", "province_id"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    code: Mapped[str] = mapped_column(String(10), unique=True, nullable=False)
    nom: Mapped[str] = mapped_column(String(100), nullable=False)
    province_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("provinces.id", ondelete="CASCADE"),
        nullable=False
    )

    # Relations
    province: Mapped["Province"] = relationship(
        "Province",
        back_populates="regions"
    )
    communes: Mapped[List["Commune"]] = relationship(
        "Commune",
        back_populates="region",
        cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<Region(id={self.id}, code='{self.code}', nom='{self.nom}')>"


class Commune(Base, TimestampMixin):
    """
    Communes de Madagascar (collectivités territoriales).
    Troisième niveau de la hiérarchie administrative.
    """
    __tablename__ = "communes"
    __table_args__ = (
        Index("idx_communes_region", "region_id"),
        Index("idx_communes_nom", "nom"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    code: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    nom: Mapped[str] = mapped_column(String(150), nullable=False)
    type_commune: Mapped[Optional[TypeCommune]] = mapped_column(
        Enum(TypeCommune, name="type_commune_enum", create_type=False),
        nullable=True
    )
    region_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("regions.id", ondelete="CASCADE"),
        nullable=False
    )
    population: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    superficie_km2: Mapped[Optional[Decimal]] = mapped_column(
        Numeric(10, 2),
        nullable=True
    )

    # Relations
    region: Mapped["Region"] = relationship(
        "Region",
        back_populates="communes"
    )

    # Relations vers autres tables (définies dans les autres modules)
    utilisateurs: Mapped[List["Utilisateur"]] = relationship(
        "Utilisateur",
        back_populates="commune"
    )
    donnees_recettes: Mapped[List["DonneesRecettes"]] = relationship(
        "DonneesRecettes",
        back_populates="commune"
    )
    donnees_depenses: Mapped[List["DonneesDepenses"]] = relationship(
        "DonneesDepenses",
        back_populates="commune"
    )
    projets_communes: Mapped[List["ProjetCommune"]] = relationship(
        "ProjetCommune",
        back_populates="commune"
    )
    revenus_miniers: Mapped[List["RevenuMinier"]] = relationship(
        "RevenuMinier",
        back_populates="commune"
    )
    documents: Mapped[List["Document"]] = relationship(
        "Document",
        back_populates="commune"
    )
    pages_compte_administratif: Mapped[List["PageCompteAdministratif"]] = relationship(
        "PageCompteAdministratif",
        back_populates="commune"
    )
    statistiques_visites: Mapped[List["StatistiqueVisite"]] = relationship(
        "StatistiqueVisite",
        back_populates="commune"
    )

    def __repr__(self) -> str:
        return f"<Commune(id={self.id}, code='{self.code}', nom='{self.nom}')>"
