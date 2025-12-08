"""
Pydantic schemas for geographic models.
Province, Region, Commune.
"""

from decimal import Decimal
from typing import List, Optional

from pydantic import Field

from app.models.enums import TypeCommune
from app.schemas.base import BaseSchema, TimestampSchema


# =====================
# Province Schemas
# =====================

class ProvinceBase(BaseSchema):
    """Base schema for Province."""
    code: str = Field(..., min_length=1, max_length=10)
    nom: str = Field(..., min_length=1, max_length=100)


class ProvinceCreate(ProvinceBase):
    """Schema for creating a Province."""
    pass


class ProvinceUpdate(BaseSchema):
    """Schema for updating a Province."""
    code: Optional[str] = Field(None, min_length=1, max_length=10)
    nom: Optional[str] = Field(None, min_length=1, max_length=100)


class ProvinceRead(ProvinceBase, TimestampSchema):
    """Schema for reading a Province."""
    id: int


class ProvinceList(BaseSchema):
    """Schema for listing Provinces."""
    id: int
    code: str
    nom: str


class ProvinceWithStats(BaseSchema):
    """Province with statistics (nb_regions, nb_communes)."""
    id: int
    code: str
    nom: str
    nb_regions: int = 0
    nb_communes: int = 0


class ProvinceWithRegions(ProvinceRead):
    """Province with nested regions."""
    regions: List["RegionList"] = []


# =====================
# Region Schemas
# =====================

class RegionBase(BaseSchema):
    """Base schema for Region."""
    code: str = Field(..., min_length=1, max_length=10)
    nom: str = Field(..., min_length=1, max_length=100)
    province_id: int


class RegionCreate(RegionBase):
    """Schema for creating a Region."""
    pass


class RegionUpdate(BaseSchema):
    """Schema for updating a Region."""
    code: Optional[str] = Field(None, min_length=1, max_length=10)
    nom: Optional[str] = Field(None, min_length=1, max_length=100)
    province_id: Optional[int] = None


class RegionRead(RegionBase, TimestampSchema):
    """Schema for reading a Region."""
    id: int


class RegionList(BaseSchema):
    """Schema for listing Regions."""
    id: int
    code: str
    nom: str
    province_id: int


class RegionWithStats(BaseSchema):
    """Region with statistics (nb_communes, province_nom)."""
    id: int
    code: str
    nom: str
    province_id: int
    nb_communes: int = 0
    province_nom: Optional[str] = None


class RegionWithProvince(RegionRead):
    """Region with nested province info."""
    province: ProvinceList


class RegionWithCommunes(RegionRead):
    """Region with nested communes."""
    communes: List["CommuneList"] = []


class RegionDetail(RegionRead):
    """Full region details with province and communes."""
    province: ProvinceList
    communes: List["CommuneList"] = []


# =====================
# Commune Schemas
# =====================

class CommuneBase(BaseSchema):
    """Base schema for Commune."""
    code: str = Field(..., min_length=1, max_length=20)
    nom: str = Field(..., min_length=1, max_length=150)
    type_commune: Optional[TypeCommune] = None
    region_id: int
    population: Optional[int] = Field(None, ge=0)
    superficie_km2: Optional[Decimal] = Field(None, ge=0)


class CommuneCreate(CommuneBase):
    """Schema for creating a Commune."""
    pass


class CommuneUpdate(BaseSchema):
    """Schema for updating a Commune."""
    code: Optional[str] = Field(None, min_length=1, max_length=20)
    nom: Optional[str] = Field(None, min_length=1, max_length=150)
    type_commune: Optional[TypeCommune] = None
    region_id: Optional[int] = None
    population: Optional[int] = Field(None, ge=0)
    superficie_km2: Optional[Decimal] = Field(None, ge=0)


class CommuneRead(CommuneBase, TimestampSchema):
    """Schema for reading a Commune."""
    id: int


class CommuneList(BaseSchema):
    """Schema for listing Communes."""
    id: int
    code: str
    nom: str
    type_commune: Optional[TypeCommune] = None
    region_id: int


class CommuneWithStats(BaseSchema):
    """Commune with statistics and parent names."""
    id: int
    code: str
    nom: str
    type_commune: Optional[TypeCommune] = None
    region_id: int
    region_nom: Optional[str] = None
    province_nom: Optional[str] = None
    nb_comptes_administratifs: int = 0


class CommuneWithRegion(CommuneRead):
    """Commune with nested region info."""
    region: RegionList


class CommuneDetail(CommuneRead):
    """Full commune details with region and province."""
    region: "RegionWithProvince"


class CommuneSearch(BaseSchema):
    """Schema for commune search results."""
    id: int
    code: str
    nom: str
    type_commune: Optional[TypeCommune] = None
    region_nom: str
    province_nom: str


# =====================
# Hierarchy Schema
# =====================

class HierarchieGeographique(BaseSchema):
    """Full geographic hierarchy."""
    provinces: List[ProvinceWithRegions]


# Update forward references
ProvinceWithRegions.model_rebuild()
RegionWithCommunes.model_rebuild()
RegionDetail.model_rebuild()
CommuneWithRegion.model_rebuild()
CommuneDetail.model_rebuild()
