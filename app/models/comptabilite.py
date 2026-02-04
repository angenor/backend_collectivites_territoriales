"""
Accounting models for budget and financial data.
PlanComptable, Exercice, DonneesRecettes, DonneesDepenses.
"""

from datetime import date, datetime
from decimal import Decimal
from typing import TYPE_CHECKING, List, Optional

from sqlalchemy import (
    Boolean, CheckConstraint, Date, DateTime, Enum, ForeignKey,
    Index, Integer, Numeric, String, Text, UniqueConstraint
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from app.models.base import TimestampMixin
from app.models.enums import SectionBudgetaire, TypeMouvement

if TYPE_CHECKING:
    from app.models.geographie import Commune
    from app.models.utilisateurs import Utilisateur
    from app.models.projets_miniers import RevenuMinier
    from app.models.documents import Document
    from app.models.cms import PageCompteAdministratif


class PlanComptable(Base, TimestampMixin):
    """
    Plan comptable hiérarchique des collectivités territoriales.
    Structure à 3 niveaux: catégorie principale, sous-catégorie, ligne détail.
    """
    __tablename__ = "plan_comptable"
    __table_args__ = (
        Index("idx_plan_comptable_parent", "parent_code"),
        Index("idx_plan_comptable_type", "type_mouvement", "section"),
        Index("idx_plan_comptable_niveau", "niveau"),
        Index("idx_plan_comptable_ordre", "type_mouvement", "section", "ordre_affichage"),
        CheckConstraint("niveau BETWEEN 1 AND 3", name="chk_niveau_1_3"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    code: Mapped[str] = mapped_column(String(10), unique=True, nullable=False)
    intitule: Mapped[str] = mapped_column(String(255), nullable=False)
    niveau: Mapped[int] = mapped_column(Integer, nullable=False)
    type_mouvement: Mapped[TypeMouvement] = mapped_column(
        Enum(TypeMouvement, name="type_mouvement", create_type=False, values_callable=lambda x: [e.value for e in x]),
        nullable=False
    )
    section: Mapped[SectionBudgetaire] = mapped_column(
        Enum(SectionBudgetaire, name="section_budgetaire", create_type=False, values_callable=lambda x: [e.value for e in x]),
        nullable=False
    )
    parent_code: Mapped[Optional[str]] = mapped_column(
        String(10),
        ForeignKey("plan_comptable.code", ondelete="SET NULL"),
        nullable=True
    )
    est_sommable: Mapped[bool] = mapped_column(Boolean, default=True)
    ordre_affichage: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    actif: Mapped[bool] = mapped_column(Boolean, default=True)

    # Relations self-referential
    parent: Mapped[Optional["PlanComptable"]] = relationship(
        "PlanComptable",
        remote_side=[code],
        foreign_keys=[parent_code],
        back_populates="enfants"
    )
    enfants: Mapped[List["PlanComptable"]] = relationship(
        "PlanComptable",
        back_populates="parent",
        foreign_keys=[parent_code]
    )

    # Relations vers données financières
    donnees_recettes: Mapped[List["DonneesRecettes"]] = relationship(
        "DonneesRecettes",
        back_populates="compte"
    )
    donnees_depenses: Mapped[List["DonneesDepenses"]] = relationship(
        "DonneesDepenses",
        back_populates="compte"
    )
    revenus_miniers: Mapped[List["RevenuMinier"]] = relationship(
        "RevenuMinier",
        back_populates="compte"
    )

    def __repr__(self) -> str:
        return f"<PlanComptable(code='{self.code}', intitule='{self.intitule[:30]}...')>"


class Exercice(Base, TimestampMixin):
    """
    Exercices budgétaires annuels.
    Représente une année fiscale.
    """
    __tablename__ = "exercices"
    __table_args__ = (
        Index("idx_exercices_annee", "annee"),
        CheckConstraint("date_fin > date_debut", name="chk_exercice_dates"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    annee: Mapped[int] = mapped_column(Integer, unique=True, nullable=False)
    libelle: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    date_debut: Mapped[date] = mapped_column(Date, nullable=False)
    date_fin: Mapped[date] = mapped_column(Date, nullable=False)
    cloture: Mapped[bool] = mapped_column(Boolean, default=False)

    # Relations
    donnees_recettes: Mapped[List["DonneesRecettes"]] = relationship(
        "DonneesRecettes",
        back_populates="exercice"
    )
    donnees_depenses: Mapped[List["DonneesDepenses"]] = relationship(
        "DonneesDepenses",
        back_populates="exercice"
    )
    revenus_miniers: Mapped[List["RevenuMinier"]] = relationship(
        "RevenuMinier",
        back_populates="exercice"
    )
    documents: Mapped[List["Document"]] = relationship(
        "Document",
        back_populates="exercice"
    )
    pages_compte_administratif: Mapped[List["PageCompteAdministratif"]] = relationship(
        "PageCompteAdministratif",
        back_populates="exercice"
    )

    def __repr__(self) -> str:
        return f"<Exercice(annee={self.annee}, cloture={self.cloture})>"


class DonneesRecettes(Base, TimestampMixin):
    """
    Données financières des recettes par commune/exercice/compte.
    Colonnes: budget primitif, additionnel, modifications, OR admis, recouvrement.
    """
    __tablename__ = "donnees_recettes"
    __table_args__ = (
        UniqueConstraint(
            "commune_id", "exercice_id", "compte_code",
            name="uk_recettes_commune_exercice_compte"
        ),
        Index("idx_recettes_commune", "commune_id"),
        Index("idx_recettes_exercice", "exercice_id"),
        Index("idx_recettes_compte", "compte_code"),
        Index("idx_recettes_commune_exercice", "commune_id", "exercice_id"),
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
    compte_code: Mapped[str] = mapped_column(
        String(10),
        ForeignKey("plan_comptable.code", ondelete="CASCADE"),
        nullable=False
    )

    # Colonnes financières (en Ariary - MGA)
    budget_primitif: Mapped[Decimal] = mapped_column(
        Numeric(18, 2), default=Decimal("0.00")
    )
    budget_additionnel: Mapped[Decimal] = mapped_column(
        Numeric(18, 2), default=Decimal("0.00")
    )
    modifications: Mapped[Decimal] = mapped_column(
        Numeric(18, 2), default=Decimal("0.00")
    )
    previsions_definitives: Mapped[Decimal] = mapped_column(
        Numeric(18, 2), default=Decimal("0.00")
    )
    or_admis: Mapped[Decimal] = mapped_column(
        Numeric(18, 2), default=Decimal("0.00")
    )
    recouvrement: Mapped[Decimal] = mapped_column(
        Numeric(18, 2), default=Decimal("0.00")
    )
    reste_a_recouvrer: Mapped[Decimal] = mapped_column(
        Numeric(18, 2), default=Decimal("0.00")
    )

    # Métadonnées
    commentaire: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    valide: Mapped[bool] = mapped_column(Boolean, default=False)
    valide_par: Mapped[Optional[int]] = mapped_column(
        Integer,
        ForeignKey("utilisateurs.id", ondelete="SET NULL"),
        nullable=True
    )
    valide_le: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)

    # Relations
    commune: Mapped["Commune"] = relationship(
        "Commune",
        back_populates="donnees_recettes"
    )
    exercice: Mapped["Exercice"] = relationship(
        "Exercice",
        back_populates="donnees_recettes"
    )
    compte: Mapped["PlanComptable"] = relationship(
        "PlanComptable",
        back_populates="donnees_recettes"
    )
    validateur: Mapped[Optional["Utilisateur"]] = relationship(
        "Utilisateur",
        back_populates="recettes_validees",
        foreign_keys=[valide_par]
    )

    def __repr__(self) -> str:
        return f"<DonneesRecettes(commune_id={self.commune_id}, exercice_id={self.exercice_id}, compte='{self.compte_code}')>"

    @property
    def previsions_calculees(self) -> Decimal:
        """Calcule les prévisions définitives."""
        return self.budget_primitif + self.budget_additionnel + self.modifications

    @property
    def reste_calcule(self) -> Decimal:
        """Calcule le reste à recouvrer."""
        return self.or_admis - self.recouvrement

    @property
    def taux_execution(self) -> Decimal:
        """Calcule le taux d'exécution en pourcentage."""
        prev = self.previsions_definitives or self.previsions_calculees
        if prev > 0:
            return (self.or_admis / prev) * 100
        return Decimal("0.00")


class DonneesDepenses(Base, TimestampMixin):
    """
    Données financières des dépenses par commune/exercice/compte.
    Colonnes: budget primitif, additionnel, modifications, engagement, mandat, paiement.
    """
    __tablename__ = "donnees_depenses"
    __table_args__ = (
        UniqueConstraint(
            "commune_id", "exercice_id", "compte_code",
            name="uk_depenses_commune_exercice_compte"
        ),
        Index("idx_depenses_commune", "commune_id"),
        Index("idx_depenses_exercice", "exercice_id"),
        Index("idx_depenses_compte", "compte_code"),
        Index("idx_depenses_commune_exercice", "commune_id", "exercice_id"),
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
    compte_code: Mapped[str] = mapped_column(
        String(10),
        ForeignKey("plan_comptable.code", ondelete="CASCADE"),
        nullable=False
    )

    # Colonnes financières (en Ariary - MGA)
    budget_primitif: Mapped[Decimal] = mapped_column(
        Numeric(18, 2), default=Decimal("0.00")
    )
    budget_additionnel: Mapped[Decimal] = mapped_column(
        Numeric(18, 2), default=Decimal("0.00")
    )
    modifications: Mapped[Decimal] = mapped_column(
        Numeric(18, 2), default=Decimal("0.00")
    )
    previsions_definitives: Mapped[Decimal] = mapped_column(
        Numeric(18, 2), default=Decimal("0.00")
    )
    engagement: Mapped[Decimal] = mapped_column(
        Numeric(18, 2), default=Decimal("0.00")
    )
    mandat_admis: Mapped[Decimal] = mapped_column(
        Numeric(18, 2), default=Decimal("0.00")
    )
    paiement: Mapped[Decimal] = mapped_column(
        Numeric(18, 2), default=Decimal("0.00")
    )
    reste_a_payer: Mapped[Decimal] = mapped_column(
        Numeric(18, 2), default=Decimal("0.00")
    )

    # Métadonnées
    programme: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    commentaire: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    valide: Mapped[bool] = mapped_column(Boolean, default=False)
    valide_par: Mapped[Optional[int]] = mapped_column(
        Integer,
        ForeignKey("utilisateurs.id", ondelete="SET NULL"),
        nullable=True
    )
    valide_le: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)

    # Relations
    commune: Mapped["Commune"] = relationship(
        "Commune",
        back_populates="donnees_depenses"
    )
    exercice: Mapped["Exercice"] = relationship(
        "Exercice",
        back_populates="donnees_depenses"
    )
    compte: Mapped["PlanComptable"] = relationship(
        "PlanComptable",
        back_populates="donnees_depenses"
    )
    validateur: Mapped[Optional["Utilisateur"]] = relationship(
        "Utilisateur",
        back_populates="depenses_validees",
        foreign_keys=[valide_par]
    )

    def __repr__(self) -> str:
        return f"<DonneesDepenses(commune_id={self.commune_id}, exercice_id={self.exercice_id}, compte='{self.compte_code}')>"

    @property
    def previsions_calculees(self) -> Decimal:
        """Calcule les prévisions définitives."""
        return self.budget_primitif + self.budget_additionnel + self.modifications

    @property
    def reste_calcule(self) -> Decimal:
        """Calcule le reste à payer."""
        return self.mandat_admis - self.paiement

    @property
    def taux_execution(self) -> Decimal:
        """Calcule le taux d'exécution en pourcentage."""
        prev = self.previsions_definitives or self.previsions_calculees
        if prev > 0:
            return (self.mandat_admis / prev) * 100
        return Decimal("0.00")


class ColonneDynamique(Base, TimestampMixin):
    """
    Colonnes dynamiques pour les tableaux de recettes et dépenses.
    Permet de définir les colonnes affichées dans les comptes administratifs.
    """
    __tablename__ = "colonnes_dynamiques"
    __table_args__ = (
        Index("idx_colonnes_applicable", "applicable_a"),
        Index("idx_colonnes_ordre", "applicable_a", "ordre"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    cle: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    label: Mapped[str] = mapped_column(String(100), nullable=False)
    applicable_a: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="tous"
    )  # recette | depense | tous | equilibre
    type_donnee: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="montant"
    )  # montant | pourcentage | texte | date | nombre
    formule: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    largeur: Mapped[int] = mapped_column(Integer, default=120)
    ordre: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    est_obligatoire: Mapped[bool] = mapped_column(Boolean, default=False)
    est_editable: Mapped[bool] = mapped_column(Boolean, default=True)
    est_visible: Mapped[bool] = mapped_column(Boolean, default=True)
    est_active: Mapped[bool] = mapped_column(Boolean, default=True)
    est_systeme: Mapped[bool] = mapped_column(Boolean, default=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    def __repr__(self) -> str:
        return f"<ColonneDynamique(cle='{self.cle}', label='{self.label}')>"


class CompteAdministratif(Base, TimestampMixin):
    """
    Enregistrement persistant d'un compte administratif (commune + exercice).
    Permet de suivre les comptes créés même sans données financières.
    """
    __tablename__ = "comptes_administratifs"
    __table_args__ = (
        UniqueConstraint(
            "commune_id", "exercice_id",
            name="uk_compte_administratif_commune_exercice"
        ),
        Index("idx_compte_admin_commune", "commune_id"),
        Index("idx_compte_admin_exercice", "exercice_id"),
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
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_by: Mapped[Optional[int]] = mapped_column(
        Integer,
        ForeignKey("utilisateurs.id", ondelete="SET NULL"),
        nullable=True
    )

    # Relations
    commune: Mapped["Commune"] = relationship("Commune")
    exercice: Mapped["Exercice"] = relationship("Exercice")
    createur: Mapped[Optional["Utilisateur"]] = relationship(
        "Utilisateur",
        foreign_keys=[created_by]
    )

    def __repr__(self) -> str:
        return f"<CompteAdministratif(commune_id={self.commune_id}, exercice_id={self.exercice_id})>"
