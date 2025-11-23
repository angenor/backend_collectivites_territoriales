"""
Schémas Pydantic pour la géographie
"""

from pydantic import BaseModel, Field
from typing import Optional, List
from uuid import UUID
from decimal import Decimal

from app.schemas.common import TimestampSchema


# ============================================================================
# RÉGIONS
# ============================================================================

class RegionBase(BaseModel):
    code: str = Field(..., max_length=10, description="Code unique de la région")
    nom: str = Field(..., max_length=255, description="Nom de la région")
    description: Optional[str] = Field(None, description="Description")
    actif: bool = True


class RegionCreate(RegionBase):
    pass


class RegionUpdate(BaseModel):
    nom: Optional[str] = Field(None, max_length=255)
    description: Optional[str] = None
    actif: Optional[bool] = None


class Region(RegionBase, TimestampSchema):
    id: UUID

    model_config = {"from_attributes": True}


# ============================================================================
# DÉPARTEMENTS
# ============================================================================

class DepartementBase(BaseModel):
    code: str = Field(..., max_length=10)
    nom: str = Field(..., max_length=255)
    region_id: UUID
    description: Optional[str] = None
    actif: bool = True


class DepartementCreate(DepartementBase):
    pass


class DepartementUpdate(BaseModel):
    nom: Optional[str] = Field(None, max_length=255)
    region_id: Optional[UUID] = None
    description: Optional[str] = None
    actif: Optional[bool] = None


class Departement(DepartementBase, TimestampSchema):
    id: UUID

    model_config = {"from_attributes": True}


class DepartementDetail(Departement):
    """Département avec région"""
    region: Region


# ============================================================================
# COMMUNES
# ============================================================================

class CommuneBase(BaseModel):
    code: str = Field(..., max_length=10)
    nom: str = Field(..., max_length=255)
    departement_id: UUID
    region_id: UUID
    population: Optional[int] = Field(None, ge=0)
    superficie: Optional[Decimal] = Field(None, ge=0)
    description: Optional[str] = None
    actif: bool = True


class CommuneCreate(CommuneBase):
    pass


class CommuneUpdate(BaseModel):
    nom: Optional[str] = Field(None, max_length=255)
    population: Optional[int] = Field(None, ge=0)
    superficie: Optional[Decimal] = Field(None, ge=0)
    description: Optional[str] = None
    actif: Optional[bool] = None


class Commune(CommuneBase, TimestampSchema):
    id: UUID

    model_config = {"from_attributes": True}


class CommuneDetail(Commune):
    """Commune avec hiérarchie complète"""
    departement: Departement
    region: Region


# ============================================================================
# SCHÉMAS DE RECHERCHE
# ============================================================================

class HierarchieGeographique(BaseModel):
    """Hiérarchie géographique complète"""
    region: Region
    departements: List[Departement]
    communes: List[Commune]
