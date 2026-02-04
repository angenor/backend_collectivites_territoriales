"""
Pydantic schemas for mining projects.
SocieteMiniere, ProjetMinier, ProjetCommune, RevenuMinier.
"""

from datetime import date
from decimal import Decimal
from typing import List, Optional

from pydantic import EmailStr, Field, HttpUrl

from app.models.enums import StatutProjetMinier, TypeRevenuMinier
from app.schemas.base import BaseSchema, TimestampSchema


# =====================
# SocieteMiniere Schemas
# =====================

class SocieteMiniereBase(BaseSchema):
    """Base schema for SocieteMiniere."""
    nom: str = Field(..., min_length=1, max_length=200)
    nif: Optional[str] = Field(None, max_length=50)
    stat: Optional[str] = Field(None, max_length=50)
    siege_social: Optional[str] = Field(None, max_length=255)
    telephone: Optional[str] = Field(None, max_length=50)
    email: Optional[EmailStr] = None
    site_web: Optional[str] = Field(None, max_length=200)
    actif: bool = True


class SocieteMiniereCreate(SocieteMiniereBase):
    """Schema for creating a SocieteMiniere."""
    pass


class SocieteMiniereUpdate(BaseSchema):
    """Schema for updating a SocieteMiniere."""
    nom: Optional[str] = Field(None, min_length=1, max_length=200)
    nif: Optional[str] = Field(None, max_length=50)
    stat: Optional[str] = Field(None, max_length=50)
    siege_social: Optional[str] = Field(None, max_length=255)
    telephone: Optional[str] = Field(None, max_length=50)
    email: Optional[EmailStr] = None
    site_web: Optional[str] = Field(None, max_length=200)
    actif: Optional[bool] = None


class SocieteMiniereRead(SocieteMiniereBase, TimestampSchema):
    """Schema for reading a SocieteMiniere."""
    id: int


class SocieteMiniereList(BaseSchema):
    """Simplified schema for listing."""
    id: int
    nom: str
    actif: bool


class SocieteMiniereWithProjets(SocieteMiniereRead):
    """SocieteMiniere with its projects."""
    projets: List["ProjetMinierList"] = []


# =====================
# ProjetMinier Schemas
# =====================

class ProjetMinierBase(BaseSchema):
    """Base schema for ProjetMinier."""
    nom: str = Field(..., min_length=1, max_length=200)
    societe_id: int
    type_minerai: Optional[str] = Field(None, max_length=100)
    statut: Optional[StatutProjetMinier] = None
    date_debut_exploitation: Optional[date] = None
    surface_ha: Optional[Decimal] = Field(None, ge=0)
    description: Optional[str] = None


class ProjetCommuneNested(BaseSchema):
    """Schema imbriqué pour commune + pourcentage lors de la création d'un projet."""
    commune_id: int
    pourcentage_territoire: Decimal = Field(..., ge=0, le=100)
    date_debut: Optional[date] = None
    date_fin: Optional[date] = None


class ProjetMinierCreate(ProjetMinierBase):
    """Schema for creating a ProjetMinier."""
    communes: List[ProjetCommuneNested] = Field(default_factory=list)


class ProjetMinierUpdate(BaseSchema):
    """Schema for updating a ProjetMinier."""
    nom: Optional[str] = Field(None, min_length=1, max_length=200)
    societe_id: Optional[int] = None
    type_minerai: Optional[str] = Field(None, max_length=100)
    statut: Optional[StatutProjetMinier] = None
    date_debut_exploitation: Optional[date] = None
    surface_ha: Optional[Decimal] = Field(None, ge=0)
    description: Optional[str] = None


class ProjetMinierRead(ProjetMinierBase, TimestampSchema):
    """Schema for reading a ProjetMinier."""
    id: int


class ProjetMinierList(BaseSchema):
    """Simplified schema for listing."""
    id: int
    nom: str
    type_minerai: Optional[str] = None
    statut: Optional[StatutProjetMinier] = None


class ProjetMinierWithSociete(ProjetMinierRead):
    """ProjetMinier with société info."""
    societe: SocieteMiniereList


class ProjetMinierWithCommunes(ProjetMinierRead):
    """ProjetMinier with impacted communes."""
    societe: SocieteMiniereList
    communes: List["ProjetCommuneRead"] = []


# =====================
# ProjetCommune Schemas
# =====================

class ProjetCommuneBase(BaseSchema):
    """Base schema for ProjetCommune relation."""
    projet_id: int
    commune_id: int
    pourcentage_territoire: Decimal = Field(..., ge=0, le=100)
    date_debut: Optional[date] = None
    date_fin: Optional[date] = None


class ProjetCommuneCreate(ProjetCommuneBase):
    """Schema for creating a ProjetCommune relation."""
    pass


class ProjetCommuneUpdate(BaseSchema):
    """Schema for updating a ProjetCommune relation."""
    pourcentage_territoire: Optional[Decimal] = Field(None, ge=0, le=100)
    date_debut: Optional[date] = None
    date_fin: Optional[date] = None


class ProjetCommuneRead(ProjetCommuneBase):
    """Schema for reading a ProjetCommune relation."""
    id: int
    # Include commune info for display
    commune_nom: Optional[str] = None
    commune_code: Optional[str] = None


# =====================
# RevenuMinier Schemas
# =====================

class RevenuMinierBase(BaseSchema):
    """Base schema for RevenuMinier."""
    commune_id: int
    exercice_id: int
    projet_id: int
    type_revenu: TypeRevenuMinier
    montant_prevu: Decimal = Field(default=Decimal("0.00"), ge=0)
    montant_recu: Decimal = Field(default=Decimal("0.00"), ge=0)
    date_reception: Optional[date] = None
    reference_paiement: Optional[str] = Field(None, max_length=100)
    compte_code: str = Field(..., min_length=1, max_length=10)
    compte_administratif_id: int
    commentaire: Optional[str] = None


class RevenuMinierCreate(RevenuMinierBase):
    """Schema for creating a RevenuMinier."""
    pass


class RevenuMinierUpdate(BaseSchema):
    """Schema for updating a RevenuMinier."""
    projet_id: Optional[int] = None
    type_revenu: Optional[TypeRevenuMinier] = None
    montant_prevu: Optional[Decimal] = Field(None, ge=0)
    montant_recu: Optional[Decimal] = Field(None, ge=0)
    date_reception: Optional[date] = None
    reference_paiement: Optional[str] = Field(None, max_length=100)
    compte_code: Optional[str] = Field(None, min_length=1, max_length=10)
    compte_administratif_id: Optional[int] = None
    commentaire: Optional[str] = None


class RevenuMinierRead(RevenuMinierBase, TimestampSchema):
    """Schema for reading a RevenuMinier."""
    id: int
    # Calculated fields
    ecart: Optional[Decimal] = None
    taux_realisation: Optional[Decimal] = None


class RevenuMinierList(BaseSchema):
    """Simplified schema for listing."""
    id: int
    type_revenu: TypeRevenuMinier
    montant_prevu: Decimal
    montant_recu: Decimal
    date_reception: Optional[date] = None


class RevenuMinierWithDetails(RevenuMinierRead):
    """RevenuMinier with commune and project info."""
    commune_nom: Optional[str] = None
    exercice_annee: Optional[int] = None
    projet_nom: Optional[str] = None
    compte_intitule: Optional[str] = None
    compte_administratif_label: Optional[str] = None


# =====================
# Statistiques minières
# =====================

class StatistiquesRevenusMiniers(BaseSchema):
    """Mining revenue statistics."""
    commune_id: int
    exercice_annee: int
    # Par type de revenu
    ristournes_prevues: Decimal = Field(default=Decimal("0.00"))
    ristournes_recues: Decimal = Field(default=Decimal("0.00"))
    redevances_prevues: Decimal = Field(default=Decimal("0.00"))
    redevances_recues: Decimal = Field(default=Decimal("0.00"))
    # Totaux
    total_prevu: Decimal = Field(default=Decimal("0.00"))
    total_recu: Decimal = Field(default=Decimal("0.00"))
    ecart_total: Decimal = Field(default=Decimal("0.00"))
    taux_realisation: Optional[Decimal] = None


class ResumeProjetMinier(BaseSchema):
    """Mining project summary."""
    projet_id: int
    projet_nom: str
    societe_nom: Optional[str] = None
    type_minerai: Optional[str] = None
    statut: Optional[StatutProjetMinier] = None
    nb_communes_impactees: int
    surface_totale_ha: Optional[Decimal] = None
    total_revenus_annee: Optional[Decimal] = None


# Update forward references
SocieteMiniereWithProjets.model_rebuild()
ProjetMinierWithCommunes.model_rebuild()
