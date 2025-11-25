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


class RubriqueUpdate(BaseModel):
    nom: Optional[str] = Field(None, max_length=255)
    categorie_id: Optional[UUID] = None
    parent_id: Optional[UUID] = None
    niveau: Optional[int] = Field(None, ge=1)
    ordre: Optional[int] = None
    type: Optional[str] = Field(None, max_length=50)
    formule: Optional[str] = None
    est_calculee: Optional[bool] = None
    afficher_total: Optional[bool] = None
    description: Optional[str] = None
    actif: Optional[bool] = None


class Rubrique(RubriqueBase, TimestampSchema):
    id: UUID
    model_config = {"from_attributes": True}


# Revenus
class RevenuBase(BaseModel):
    commune_id: UUID
    rubrique_id: UUID
    periode_id: UUID
    projet_minier_id: Optional[UUID] = None

    # Colonnes de budget (communes à recettes et dépenses)
    budget_primitif: Decimal = Field(default=0, ge=0, decimal_places=2)
    budget_additionnel: Decimal = Field(default=0, decimal_places=2)
    modifications: Decimal = Field(default=0, decimal_places=2)
    previsions_definitives: Decimal = Field(default=0, ge=0, decimal_places=2)

    # Colonnes spécifiques aux RECETTES (si rubrique.type='recette')
    ordre_recette_admis: Decimal = Field(default=0, ge=0, decimal_places=2)
    recouvrement: Decimal = Field(default=0, ge=0, decimal_places=2)
    reste_a_recouvrer: Decimal = Field(default=0, decimal_places=2)

    # Colonnes spécifiques aux DEPENSES (si rubrique.type='depense')
    engagement: Decimal = Field(default=0, ge=0, decimal_places=2)
    mandat_admis: Decimal = Field(default=0, ge=0, decimal_places=2)
    paiement: Decimal = Field(default=0, ge=0, decimal_places=2)
    reste_a_payer: Decimal = Field(default=0, decimal_places=2)

    # Ancien modèle (backward compatibility - deprecated)
    montant: Decimal = Field(default=0, ge=0, decimal_places=2)
    montant_prevu: Optional[Decimal] = Field(None, ge=0, decimal_places=2)

    # Métadonnées
    observations: Optional[str] = None
    documents: Optional[Dict[str, Any]] = None


class RevenuCreate(RevenuBase):
    created_by: Optional[UUID] = None


class RevenuUpdate(BaseModel):
    # Colonnes de budget (communes à recettes et dépenses)
    budget_primitif: Optional[Decimal] = Field(None, ge=0, decimal_places=2)
    budget_additionnel: Optional[Decimal] = Field(None, decimal_places=2)
    modifications: Optional[Decimal] = Field(None, decimal_places=2)
    previsions_definitives: Optional[Decimal] = Field(None, ge=0, decimal_places=2)

    # Colonnes spécifiques aux RECETTES
    ordre_recette_admis: Optional[Decimal] = Field(None, ge=0, decimal_places=2)
    recouvrement: Optional[Decimal] = Field(None, ge=0, decimal_places=2)
    reste_a_recouvrer: Optional[Decimal] = Field(None, decimal_places=2)

    # Colonnes spécifiques aux DEPENSES
    engagement: Optional[Decimal] = Field(None, ge=0, decimal_places=2)
    mandat_admis: Optional[Decimal] = Field(None, ge=0, decimal_places=2)
    paiement: Optional[Decimal] = Field(None, ge=0, decimal_places=2)
    reste_a_payer: Optional[Decimal] = Field(None, decimal_places=2)

    # Ancien modèle (backward compatibility - deprecated)
    montant: Optional[Decimal] = Field(None, ge=0, decimal_places=2)
    montant_prevu: Optional[Decimal] = Field(None, ge=0, decimal_places=2)

    # Métadonnées
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


# RevenuDetail with nested relationships
class RevenuDetail(Revenu):
    """Revenu avec relations complètes (pour les endpoints avec joinedload)"""
    rubrique: Optional["Rubrique"] = None
    periode: Optional["Periode"] = None
    commune: Optional[Any] = None  # CommuneBase from geographie
    projet_minier: Optional[Any] = None  # ProjetMinier from projets_miniers


# Filtres
class RevenuFilter(BaseModel):
    """Filtres pour la recherche de revenus"""
    commune_code: Optional[str] = None
    region_code: Optional[str] = None
    exercice_annee: Optional[int] = None
    rubrique_code: Optional[str] = None
    projet_minier_id: Optional[UUID] = None
    valide: Optional[bool] = None
