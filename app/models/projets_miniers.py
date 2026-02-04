"""
Mining projects and revenues models.
SocieteMiniere, ProjetMinier, ProjetCommune, RevenuMinier.
"""

from datetime import date
from decimal import Decimal
from typing import TYPE_CHECKING, List, Optional

from sqlalchemy import (
    Boolean, Date, Enum, ForeignKey, Index, Integer,
    Numeric, String, Text, UniqueConstraint
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from app.models.base import TimestampMixin
from app.models.enums import StatutProjetMinier, TypeRevenuMinier

if TYPE_CHECKING:
    from app.models.geographie import Commune
    from app.models.comptabilite import Exercice, PlanComptable, CompteAdministratif


class SocieteMiniere(Base, TimestampMixin):
    """
    Sociétés minières opérant à Madagascar.
    """
    __tablename__ = "societes_minieres"
    __table_args__ = (
        Index("idx_societes_minieres_nom", "nom"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nom: Mapped[str] = mapped_column(String(200), nullable=False)
    nif: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    stat: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    siege_social: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    telephone: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    email: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    site_web: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)
    actif: Mapped[bool] = mapped_column(Boolean, default=True)

    # Relations
    projets: Mapped[List["ProjetMinier"]] = relationship(
        "ProjetMinier",
        back_populates="societe"
    )

    def __repr__(self) -> str:
        return f"<SocieteMiniere(id={self.id}, nom='{self.nom}')>"


class ProjetMinier(Base, TimestampMixin):
    """
    Projets d'exploitation minière.
    """
    __tablename__ = "projets_miniers"
    __table_args__ = (
        Index("idx_projets_miniers_societe", "societe_id"),
        Index("idx_projets_miniers_statut", "statut"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nom: Mapped[str] = mapped_column(String(200), nullable=False)
    societe_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("societes_minieres.id", ondelete="RESTRICT"),
        nullable=False
    )
    type_minerai: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    statut: Mapped[Optional[StatutProjetMinier]] = mapped_column(
        Enum(StatutProjetMinier, name="statut_projet_minier", create_type=False, values_callable=lambda x: [e.value for e in x]),
        nullable=True
    )
    date_debut_exploitation: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    surface_ha: Mapped[Optional[Decimal]] = mapped_column(Numeric(12, 2), nullable=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Relations
    societe: Mapped["SocieteMiniere"] = relationship(
        "SocieteMiniere",
        back_populates="projets"
    )
    projets_communes: Mapped[List["ProjetCommune"]] = relationship(
        "ProjetCommune",
        back_populates="projet",
        cascade="all, delete-orphan"
    )
    revenus_miniers: Mapped[List["RevenuMinier"]] = relationship(
        "RevenuMinier",
        back_populates="projet"
    )

    def __repr__(self) -> str:
        return f"<ProjetMinier(id={self.id}, nom='{self.nom}')>"

    @property
    def communes(self) -> List["Commune"]:
        """Retourne la liste des communes impactées."""
        return [pc.commune for pc in self.projets_communes]


class ProjetCommune(Base):
    """
    Relation N-N entre projets miniers et communes.
    Communes impactées par les projets miniers.
    """
    __tablename__ = "projets_communes"
    __table_args__ = (
        UniqueConstraint("projet_id", "commune_id", name="uk_projet_commune"),
        Index("idx_projets_communes_projet", "projet_id"),
        Index("idx_projets_communes_commune", "commune_id"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    projet_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("projets_miniers.id", ondelete="CASCADE"),
        nullable=False
    )
    commune_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("communes.id", ondelete="CASCADE"),
        nullable=False
    )
    pourcentage_territoire: Mapped[Decimal] = mapped_column(
        Numeric(5, 2),
        nullable=False,
        default=Decimal("100.00")
    )
    date_debut: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    date_fin: Mapped[Optional[date]] = mapped_column(Date, nullable=True)

    # Relations
    projet: Mapped["ProjetMinier"] = relationship(
        "ProjetMinier",
        back_populates="projets_communes"
    )
    commune: Mapped["Commune"] = relationship(
        "Commune",
        back_populates="projets_communes"
    )

    def __repr__(self) -> str:
        return f"<ProjetCommune(projet_id={self.projet_id}, commune_id={self.commune_id})>"


class RevenuMinier(Base, TimestampMixin):
    """
    Revenus miniers spécifiques (ristournes, redevances).
    Enregistre les montants prévus et reçus par commune/exercice.
    """
    __tablename__ = "revenus_miniers"
    __table_args__ = (
        Index("idx_revenus_miniers_commune", "commune_id"),
        Index("idx_revenus_miniers_exercice", "exercice_id"),
        Index("idx_revenus_miniers_projet", "projet_id"),
        Index("idx_revenus_miniers_type", "type_revenu"),
        Index("idx_revenus_miniers_compte_admin", "compte_administratif_id"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    commune_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("communes.id", ondelete="CASCADE"),
        nullable=False
    )
    exercice_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("exercices.id", ondelete="CASCADE"),
        nullable=False
    )
    projet_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("projets_miniers.id", ondelete="RESTRICT"),
        nullable=False
    )
    type_revenu: Mapped[TypeRevenuMinier] = mapped_column(
        Enum(TypeRevenuMinier, name="type_revenu_minier", create_type=False, values_callable=lambda x: [e.value for e in x]),
        nullable=False
    )
    montant_prevu: Mapped[Decimal] = mapped_column(
        Numeric(18, 2),
        default=Decimal("0.00")
    )
    montant_recu: Mapped[Decimal] = mapped_column(
        Numeric(18, 2),
        default=Decimal("0.00")
    )
    date_reception: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    reference_paiement: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    compte_code: Mapped[str] = mapped_column(
        String(10),
        ForeignKey("plan_comptable.code", ondelete="RESTRICT"),
        nullable=False
    )
    compte_administratif_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("comptes_administratifs.id", ondelete="CASCADE"),
        nullable=False
    )
    commentaire: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Relations
    commune: Mapped["Commune"] = relationship(
        "Commune",
        back_populates="revenus_miniers"
    )
    exercice: Mapped["Exercice"] = relationship(
        "Exercice",
        back_populates="revenus_miniers"
    )
    projet: Mapped["ProjetMinier"] = relationship(
        "ProjetMinier",
        back_populates="revenus_miniers"
    )
    compte: Mapped["PlanComptable"] = relationship(
        "PlanComptable",
        back_populates="revenus_miniers"
    )
    compte_administratif: Mapped["CompteAdministratif"] = relationship(
        "CompteAdministratif",
        back_populates="revenus_miniers"
    )

    def __repr__(self) -> str:
        return f"<RevenuMinier(id={self.id}, type='{self.type_revenu.value}', commune_id={self.commune_id})>"

    @property
    def ecart(self) -> Decimal:
        """Calcule l'écart entre prévu et reçu."""
        return self.montant_recu - self.montant_prevu

    @property
    def taux_realisation(self) -> Decimal:
        """Calcule le taux de réalisation en pourcentage."""
        if self.montant_prevu > 0:
            return (self.montant_recu / self.montant_prevu) * 100
        return Decimal("0.00")
