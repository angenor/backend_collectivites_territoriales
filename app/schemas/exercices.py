"""
Schémas Pydantic pour les exercices fiscaux et périodes
"""

from pydantic import BaseModel, Field
from typing import Optional, List
from uuid import UUID
from datetime import date

from app.schemas.common import TimestampSchema


# ============================================================================
# EXERCICES FISCAUX
# ============================================================================

class ExerciceBase(BaseModel):
    annee: int = Field(..., description="Année fiscale")
    date_debut: date = Field(..., description="Date de début de l'exercice")
    date_fin: date = Field(..., description="Date de fin de l'exercice")
    statut: str = Field(default="ouvert", description="Statut: ouvert ou cloturé")
    actif: bool = True


class ExerciceCreate(ExerciceBase):
    pass


class ExerciceUpdate(BaseModel):
    date_debut: Optional[date] = None
    date_fin: Optional[date] = None
    statut: Optional[str] = None
    actif: Optional[bool] = None


class Exercice(ExerciceBase, TimestampSchema):
    id: UUID

    model_config = {"from_attributes": True}


# ============================================================================
# PÉRIODES
# ============================================================================

class PeriodeBase(BaseModel):
    code: str = Field(..., max_length=50, description="Code unique de la période")
    nom: str = Field(..., max_length=255, description="Nom de la période")
    exercice_id: UUID = Field(..., description="ID de l'exercice fiscal")
    date_debut: date = Field(..., description="Date de début de la période")
    date_fin: date = Field(..., description="Date de fin de la période")
    type_periode: Optional[str] = Field(None, max_length=50, description="Type: mensuel, trimestriel, semestriel, annuel")
    ordre: Optional[int] = Field(None, description="Ordre d'affichage")
    actif: bool = True


class PeriodeCreate(PeriodeBase):
    pass


class PeriodeUpdate(BaseModel):
    nom: Optional[str] = Field(None, max_length=255)
    date_debut: Optional[date] = None
    date_fin: Optional[date] = None
    type_periode: Optional[str] = Field(None, max_length=50)
    ordre: Optional[int] = None
    actif: Optional[bool] = None


class Periode(PeriodeBase, TimestampSchema):
    id: UUID

    model_config = {"from_attributes": True}


class PeriodeDetail(Periode):
    """Période avec exercice"""
    exercice: Exercice


class ExerciceDetail(Exercice):
    """Exercice avec périodes"""
    periodes: List[Periode] = []
