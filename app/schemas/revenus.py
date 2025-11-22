"""
Schémas Pydantic pour les revenus
"""

from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from uuid import UUID
from datetime import date, datetime
from decimal import Decimal

from app.schemas.common import TimestampSchema


# Exercices
class ExerciceBase(BaseModel):
    annee: int = Field(..., ge=2000, le=2100)
    date_debut: date
    date_fin: date
    statut: str = Field(default="ouvert", max_length=50)
    actif: bool = True


class ExerciceCreate(ExerciceBase):
    pass


class Exercice(ExerciceBase, TimestampSchema):
    id: UUID
    model_config = {"from_attributes": True}


# Périodes
class PeriodeBase(BaseModel):
    code: str = Field(..., max_length=50)
    nom: str = Field(..., max_length=255)
    exercice_id: UUID
    date_debut: date
    date_fin: date
    type_periode: Optional[str] = Field(None, max_length=50)
    ordre: Optional[int] = None
    actif: bool = True


class PeriodeCreate(PeriodeBase):
    pass


class Periode(PeriodeBase, TimestampSchema):
    id: UUID
    model_config = {"from_attributes": True}


# Rubriques
class RubriqueBase(BaseModel):
    code: str = Field(..., max_length=50)
    nom: str = Field(..., max_length=255)
    categorie_id: Optional[UUID] = None
    parent_id: Optional[UUID] = None
    niveau: int = Field(default=1, ge=1)
    ordre: Optional[int] = None
    type: Optional[str] = Field(None, max_length=50)
    formule: Optional[str] = None
    est_calculee: bool = False
    afficher_total: bool = True
    description: Optional[str] = None
    actif: bool = True


class RubriqueCreate(RubriqueBase):
    pass


class Rubrique(RubriqueBase, TimestampSchema):
    id: UUID
    model_config = {"from_attributes": True}


# Revenus
class RevenuBase(BaseModel):
    commune_id: UUID
    rubrique_id: UUID
    periode_id: UUID
    projet_minier_id: Optional[UUID] = None
    montant: Decimal = Field(..., ge=0, decimal_places=2)
    montant_prevu: Optional[Decimal] = Field(None, ge=0, decimal_places=2)
    observations: Optional[str] = None
    documents: Optional[Dict[str, Any]] = None


class RevenuCreate(RevenuBase):
    created_by: Optional[UUID] = None


class RevenuUpdate(BaseModel):
    montant: Optional[Decimal] = Field(None, ge=0, decimal_places=2)
    montant_prevu: Optional[Decimal] = Field(None, ge=0, decimal_places=2)
    observations: Optional[str] = None
    documents: Optional[Dict[str, Any]] = None
    updated_by: Optional[UUID] = None


class Revenu(RevenuBase, TimestampSchema):
    id: UUID
    ecart: Optional[Decimal] = None
    taux_realisation: Optional[Decimal] = None
    valide: bool = False
    valide_par: Optional[UUID] = None
    valide_le: Optional[datetime] = None
    created_by: Optional[UUID] = None
    updated_by: Optional[UUID] = None

    model_config = {"from_attributes": True}


# Filtres
class RevenuFilter(BaseModel):
    """Filtres pour la recherche de revenus"""
    commune_code: Optional[str] = None
    region_code: Optional[str] = None
    exercice_annee: Optional[int] = None
    rubrique_code: Optional[str] = None
    projet_minier_id: Optional[UUID] = None
    valide: Optional[bool] = None
