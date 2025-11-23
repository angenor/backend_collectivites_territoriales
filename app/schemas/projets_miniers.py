"""
Schémas Pydantic pour les projets miniers
"""

from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from uuid import UUID
from datetime import date

from app.schemas.common import TimestampSchema


# ============================================================================
# TYPES DE MINERAIS
# ============================================================================

class TypeMineraiBase(BaseModel):
    code: str = Field(..., max_length=50, description="Code unique du type de minerai")
    nom: str = Field(..., max_length=255, description="Nom du minerai")
    description: Optional[str] = Field(None, description="Description")
    actif: bool = True


class TypeMineraiCreate(TypeMineraiBase):
    pass


class TypeMineraiUpdate(BaseModel):
    nom: Optional[str] = Field(None, max_length=255)
    description: Optional[str] = None
    actif: Optional[bool] = None


class TypeMinerai(TypeMineraiBase, TimestampSchema):
    id: UUID

    model_config = {"from_attributes": True}


# ============================================================================
# SOCIÉTÉS MINIÈRES
# ============================================================================

class SocieteMiniereBase(BaseModel):
    code: str = Field(..., max_length=50, description="Code unique de la société")
    nom: str = Field(..., max_length=255, description="Nom de la société")
    raison_sociale: Optional[str] = Field(None, max_length=255, description="Raison sociale")
    nif: Optional[str] = Field(None, max_length=50, description="Numéro d'Identification Fiscale")
    stat: Optional[str] = Field(None, max_length=50, description="Numéro statistique")
    adresse: Optional[str] = Field(None, description="Adresse complète")
    telephone: Optional[str] = Field(None, max_length=50)
    email: Optional[EmailStr] = None
    actif: bool = True


class SocieteMiniereCreate(SocieteMiniereBase):
    pass


class SocieteMiniereUpdate(BaseModel):
    nom: Optional[str] = Field(None, max_length=255)
    raison_sociale: Optional[str] = Field(None, max_length=255)
    nif: Optional[str] = Field(None, max_length=50)
    stat: Optional[str] = Field(None, max_length=50)
    adresse: Optional[str] = None
    telephone: Optional[str] = Field(None, max_length=50)
    email: Optional[EmailStr] = None
    actif: Optional[bool] = None


class SocieteMiniere(SocieteMiniereBase, TimestampSchema):
    id: UUID

    model_config = {"from_attributes": True}


# ============================================================================
# PROJETS MINIERS
# ============================================================================

class ProjetMinierBase(BaseModel):
    code: str = Field(..., max_length=50, description="Code unique du projet")
    nom: str = Field(..., max_length=255, description="Nom du projet")
    societe_miniere_id: UUID = Field(..., description="ID de la société minière")
    type_minerai_id: UUID = Field(..., description="ID du type de minerai")
    commune_id: UUID = Field(..., description="ID de la commune")
    date_debut: Optional[date] = Field(None, description="Date de début du projet")
    date_fin: Optional[date] = Field(None, description="Date de fin du projet")
    statut: str = Field(default="actif", description="Statut: actif, suspendu, terminé")
    description: Optional[str] = None
    actif: bool = True


class ProjetMinierCreate(ProjetMinierBase):
    pass


class ProjetMinierUpdate(BaseModel):
    nom: Optional[str] = Field(None, max_length=255)
    societe_miniere_id: Optional[UUID] = None
    type_minerai_id: Optional[UUID] = None
    commune_id: Optional[UUID] = None
    date_debut: Optional[date] = None
    date_fin: Optional[date] = None
    statut: Optional[str] = None
    description: Optional[str] = None
    actif: Optional[bool] = None


class ProjetMinier(ProjetMinierBase, TimestampSchema):
    id: UUID

    model_config = {"from_attributes": True}


class ProjetMinierDetail(ProjetMinier):
    """Projet minier avec relations complètes"""
    societe_miniere: SocieteMiniere
    type_minerai: TypeMinerai
    # commune: CommuneBase # Éviter import circulaire pour l'instant
