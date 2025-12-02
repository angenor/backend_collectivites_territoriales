"""
Pydantic schemas for accounting models.
PlanComptable, Exercice, DonneesRecettes, DonneesDepenses.
"""

from datetime import date, datetime
from decimal import Decimal
from typing import List, Optional

from pydantic import Field, field_validator

from app.models.enums import SectionBudgetaire, TypeMouvement
from app.schemas.base import BaseSchema, TimestampSchema


# =====================
# PlanComptable Schemas
# =====================

class PlanComptableBase(BaseSchema):
    """Base schema for PlanComptable."""
    code: str = Field(..., min_length=1, max_length=10)
    intitule: str = Field(..., min_length=1, max_length=255)
    niveau: int = Field(..., ge=1, le=3)
    type_mouvement: TypeMouvement
    section: SectionBudgetaire
    parent_code: Optional[str] = Field(None, max_length=10)
    est_sommable: bool = True
    ordre_affichage: Optional[int] = None
    actif: bool = True


class PlanComptableCreate(PlanComptableBase):
    """Schema for creating a PlanComptable entry."""
    pass


class PlanComptableUpdate(BaseSchema):
    """Schema for updating a PlanComptable entry."""
    intitule: Optional[str] = Field(None, min_length=1, max_length=255)
    parent_code: Optional[str] = Field(None, max_length=10)
    est_sommable: Optional[bool] = None
    ordre_affichage: Optional[int] = None
    actif: Optional[bool] = None


class PlanComptableRead(PlanComptableBase, TimestampSchema):
    """Schema for reading a PlanComptable entry."""
    id: int


class PlanComptableList(BaseSchema):
    """Simplified schema for listing."""
    code: str
    intitule: str
    niveau: int
    type_mouvement: TypeMouvement
    section: SectionBudgetaire
    parent_code: Optional[str] = None


class PlanComptableTree(PlanComptableRead):
    """PlanComptable with children for tree structure."""
    enfants: List["PlanComptableTree"] = []


# =====================
# Exercice Schemas
# =====================

class ExerciceBase(BaseSchema):
    """Base schema for Exercice."""
    annee: int = Field(..., ge=2000, le=2100)
    libelle: Optional[str] = Field(None, max_length=50)
    date_debut: date
    date_fin: date
    cloture: bool = False

    @field_validator("date_fin")
    @classmethod
    def validate_dates(cls, v: date, info) -> date:
        """Ensure date_fin > date_debut."""
        if "date_debut" in info.data and v <= info.data["date_debut"]:
            raise ValueError("date_fin doit être postérieure à date_debut")
        return v


class ExerciceCreate(ExerciceBase):
    """Schema for creating an Exercice."""
    pass


class ExerciceUpdate(BaseSchema):
    """Schema for updating an Exercice."""
    libelle: Optional[str] = Field(None, max_length=50)
    date_debut: Optional[date] = None
    date_fin: Optional[date] = None
    cloture: Optional[bool] = None


class ExerciceRead(ExerciceBase, TimestampSchema):
    """Schema for reading an Exercice."""
    id: int


class ExerciceList(BaseSchema):
    """Simplified schema for listing exercices."""
    id: int
    annee: int
    libelle: Optional[str] = None
    cloture: bool


# =====================
# DonneesRecettes Schemas
# =====================

class DonneesRecettesBase(BaseSchema):
    """Base schema for DonneesRecettes."""
    commune_id: int
    exercice_id: int
    compte_code: str = Field(..., min_length=1, max_length=10)
    budget_primitif: Decimal = Field(default=Decimal("0.00"), ge=0)
    budget_additionnel: Decimal = Field(default=Decimal("0.00"))
    modifications: Decimal = Field(default=Decimal("0.00"))
    previsions_definitives: Decimal = Field(default=Decimal("0.00"), ge=0)
    or_admis: Decimal = Field(default=Decimal("0.00"), ge=0)
    recouvrement: Decimal = Field(default=Decimal("0.00"), ge=0)
    reste_a_recouvrer: Decimal = Field(default=Decimal("0.00"), ge=0)
    commentaire: Optional[str] = None


class DonneesRecettesCreate(DonneesRecettesBase):
    """Schema for creating DonneesRecettes."""
    pass


class DonneesRecettesUpdate(BaseSchema):
    """Schema for updating DonneesRecettes."""
    budget_primitif: Optional[Decimal] = Field(None, ge=0)
    budget_additionnel: Optional[Decimal] = None
    modifications: Optional[Decimal] = None
    previsions_definitives: Optional[Decimal] = Field(None, ge=0)
    or_admis: Optional[Decimal] = Field(None, ge=0)
    recouvrement: Optional[Decimal] = Field(None, ge=0)
    reste_a_recouvrer: Optional[Decimal] = Field(None, ge=0)
    commentaire: Optional[str] = None


class DonneesRecettesRead(DonneesRecettesBase, TimestampSchema):
    """Schema for reading DonneesRecettes."""
    id: int
    valide: bool = False
    valide_par: Optional[int] = None
    valide_le: Optional[datetime] = None
    # Calculated fields
    taux_execution: Optional[Decimal] = None


class DonneesRecettesList(BaseSchema):
    """Simplified schema for listing."""
    id: int
    compte_code: str
    previsions_definitives: Decimal
    or_admis: Decimal
    recouvrement: Decimal


class DonneesRecettesWithCompte(DonneesRecettesRead):
    """DonneesRecettes with account info."""
    compte: PlanComptableList


class DonneesRecettesValidation(BaseSchema):
    """Schema for validating DonneesRecettes."""
    valide: bool
    commentaire: Optional[str] = None


# =====================
# DonneesDepenses Schemas
# =====================

class DonneesDepensesBase(BaseSchema):
    """Base schema for DonneesDepenses."""
    commune_id: int
    exercice_id: int
    compte_code: str = Field(..., min_length=1, max_length=10)
    budget_primitif: Decimal = Field(default=Decimal("0.00"), ge=0)
    budget_additionnel: Decimal = Field(default=Decimal("0.00"))
    modifications: Decimal = Field(default=Decimal("0.00"))
    previsions_definitives: Decimal = Field(default=Decimal("0.00"), ge=0)
    engagement: Decimal = Field(default=Decimal("0.00"), ge=0)
    mandat_admis: Decimal = Field(default=Decimal("0.00"), ge=0)
    paiement: Decimal = Field(default=Decimal("0.00"), ge=0)
    reste_a_payer: Decimal = Field(default=Decimal("0.00"), ge=0)
    programme: Optional[str] = Field(None, max_length=100)
    commentaire: Optional[str] = None


class DonneesDepensesCreate(DonneesDepensesBase):
    """Schema for creating DonneesDepenses."""
    pass


class DonneesDepensesUpdate(BaseSchema):
    """Schema for updating DonneesDepenses."""
    budget_primitif: Optional[Decimal] = Field(None, ge=0)
    budget_additionnel: Optional[Decimal] = None
    modifications: Optional[Decimal] = None
    previsions_definitives: Optional[Decimal] = Field(None, ge=0)
    engagement: Optional[Decimal] = Field(None, ge=0)
    mandat_admis: Optional[Decimal] = Field(None, ge=0)
    paiement: Optional[Decimal] = Field(None, ge=0)
    reste_a_payer: Optional[Decimal] = Field(None, ge=0)
    programme: Optional[str] = Field(None, max_length=100)
    commentaire: Optional[str] = None


class DonneesDepensesRead(DonneesDepensesBase, TimestampSchema):
    """Schema for reading DonneesDepenses."""
    id: int
    valide: bool = False
    valide_par: Optional[int] = None
    valide_le: Optional[datetime] = None
    # Calculated fields
    taux_execution: Optional[Decimal] = None


class DonneesDepensesList(BaseSchema):
    """Simplified schema for listing."""
    id: int
    compte_code: str
    previsions_definitives: Decimal
    mandat_admis: Decimal
    paiement: Decimal


class DonneesDepensesWithCompte(DonneesDepensesRead):
    """DonneesDepenses with account info."""
    compte: PlanComptableList


class DonneesDepensesValidation(BaseSchema):
    """Schema for validating DonneesDepenses."""
    valide: bool
    commentaire: Optional[str] = None


# Update forward references
PlanComptableTree.model_rebuild()
