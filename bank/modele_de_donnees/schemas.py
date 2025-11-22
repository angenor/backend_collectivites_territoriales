"""
Schémas Pydantic pour la validation des données avec FastAPI
Ces schémas définissent la structure des données pour les requêtes et réponses API
"""

from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional, List, Dict, Any
from datetime import datetime, date
from uuid import UUID
from decimal import Decimal


# ============================================================================
# SCHÉMAS DE BASE
# ============================================================================

class TimestampSchema(BaseModel):
    """Schéma de base avec timestamps"""
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# ============================================================================
# SCHÉMAS GÉOGRAPHIQUES
# ============================================================================

class RegionBase(BaseModel):
    code: str = Field(..., max_length=10)
    nom: str = Field(..., max_length=255)
    description: Optional[str] = None
    actif: bool = True


class RegionCreate(RegionBase):
    pass


class RegionUpdate(BaseModel):
    nom: Optional[str] = Field(None, max_length=255)
    description: Optional[str] = None
    actif: Optional[bool] = None


class RegionInDB(RegionBase, TimestampSchema):
    id: UUID

    class Config:
        from_attributes = True


class DepartementBase(BaseModel):
    code: str = Field(..., max_length=10)
    nom: str = Field(..., max_length=255)
    region_id: UUID
    description: Optional[str] = None
    actif: bool = True


class DepartementCreate(DepartementBase):
    pass


class DepartementInDB(DepartementBase, TimestampSchema):
    id: UUID

    class Config:
        from_attributes = True


class CommuneBase(BaseModel):
    code: str = Field(..., max_length=10)
    nom: str = Field(..., max_length=255)
    departement_id: UUID
    region_id: UUID
    population: Optional[int] = None
    superficie: Optional[Decimal] = None
    description: Optional[str] = None
    actif: bool = True


class CommuneCreate(CommuneBase):
    pass


class CommuneInDB(CommuneBase, TimestampSchema):
    id: UUID

    class Config:
        from_attributes = True


class CommuneDetail(CommuneInDB):
    """Commune avec détails de la hiérarchie"""
    departement: DepartementInDB
    region: RegionInDB


# ============================================================================
# SCHÉMAS PROJETS MINIERS
# ============================================================================

class TypeMineraiBase(BaseModel):
    code: str = Field(..., max_length=50)
    nom: str = Field(..., max_length=255)
    description: Optional[str] = None
    actif: bool = True


class TypeMineraiCreate(TypeMineraiBase):
    pass


class TypeMineraiInDB(TypeMineraiBase, TimestampSchema):
    id: UUID

    class Config:
        from_attributes = True


class SocieteMiniereBase(BaseModel):
    code: str = Field(..., max_length=50)
    nom: str = Field(..., max_length=255)
    raison_sociale: Optional[str] = Field(None, max_length=255)
    nif: Optional[str] = Field(None, max_length=50)
    stat: Optional[str] = Field(None, max_length=50)
    adresse: Optional[str] = None
    telephone: Optional[str] = Field(None, max_length=50)
    email: Optional[EmailStr] = None
    actif: bool = True


class SocieteMiniereCreate(SocieteMiniereBase):
    pass


class SocieteMiniereInDB(SocieteMiniereBase, TimestampSchema):
    id: UUID

    class Config:
        from_attributes = True


class ProjetMinierBase(BaseModel):
    code: str = Field(..., max_length=50)
    nom: str = Field(..., max_length=255)
    societe_miniere_id: UUID
    type_minerai_id: UUID
    commune_id: UUID
    date_debut: Optional[date] = None
    date_fin: Optional[date] = None
    statut: str = Field(default="actif", max_length=50)
    description: Optional[str] = None
    actif: bool = True


class ProjetMinierCreate(ProjetMinierBase):
    pass


class ProjetMinierInDB(ProjetMinierBase, TimestampSchema):
    id: UUID

    class Config:
        from_attributes = True


# ============================================================================
# SCHÉMAS REVENUS
# ============================================================================

class ExerciceBase(BaseModel):
    annee: int = Field(..., ge=2000, le=2100)
    date_debut: date
    date_fin: date
    statut: str = Field(default="ouvert", max_length=50)
    actif: bool = True


class ExerciceCreate(ExerciceBase):
    pass


class ExerciceInDB(ExerciceBase, TimestampSchema):
    id: UUID

    class Config:
        from_attributes = True


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


class PeriodeInDB(PeriodeBase, TimestampSchema):
    id: UUID

    class Config:
        from_attributes = True


class CategorieRubriqueBase(BaseModel):
    code: str = Field(..., max_length=50)
    nom: str = Field(..., max_length=255)
    description: Optional[str] = None
    ordre: Optional[int] = None
    actif: bool = True


class CategorieRubriqueCreate(CategorieRubriqueBase):
    pass


class CategorieRubriqueInDB(CategorieRubriqueBase, TimestampSchema):
    id: UUID

    class Config:
        from_attributes = True


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


class RubriqueInDB(RubriqueBase, TimestampSchema):
    id: UUID

    class Config:
        from_attributes = True


class RubriqueDetail(RubriqueInDB):
    """Rubrique avec catégorie et sous-rubriques"""
    categorie: Optional[CategorieRubriqueInDB] = None
    sous_rubriques: List['RubriqueInDB'] = []


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


class RevenuInDB(RevenuBase, TimestampSchema):
    id: UUID
    ecart: Optional[Decimal] = None
    taux_realisation: Optional[Decimal] = None
    valide: bool = False
    valide_par: Optional[UUID] = None
    valide_le: Optional[datetime] = None
    created_by: Optional[UUID] = None
    updated_by: Optional[UUID] = None

    class Config:
        from_attributes = True


class RevenuDetail(RevenuInDB):
    """Revenu avec tous les détails"""
    commune: CommuneInDB
    rubrique: RubriqueInDB
    periode: PeriodeInDB
    projet_minier: Optional[ProjetMinierInDB] = None


# ============================================================================
# SCHÉMAS UTILISATEURS
# ============================================================================

class RoleBase(BaseModel):
    code: str = Field(..., max_length=50)
    nom: str = Field(..., max_length=255)
    description: Optional[str] = None
    permissions: Optional[Dict[str, Any]] = None
    actif: bool = True


class RoleCreate(RoleBase):
    pass


class RoleInDB(RoleBase, TimestampSchema):
    id: UUID

    class Config:
        from_attributes = True


class UtilisateurBase(BaseModel):
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=100)
    nom: str = Field(..., max_length=255)
    prenom: Optional[str] = Field(None, max_length=255)
    role_id: UUID
    commune_id: Optional[UUID] = None
    telephone: Optional[str] = Field(None, max_length=50)
    actif: bool = True


class UtilisateurCreate(UtilisateurBase):
    password: str = Field(..., min_length=8)


class UtilisateurUpdate(BaseModel):
    email: Optional[EmailStr] = None
    nom: Optional[str] = Field(None, max_length=255)
    prenom: Optional[str] = Field(None, max_length=255)
    telephone: Optional[str] = Field(None, max_length=50)
    actif: Optional[bool] = None


class UtilisateurInDB(UtilisateurBase, TimestampSchema):
    id: UUID
    email_verifie: bool = False
    dernier_login: Optional[datetime] = None

    class Config:
        from_attributes = True


class UtilisateurDetail(UtilisateurInDB):
    """Utilisateur avec rôle et commune"""
    role: RoleInDB
    commune: Optional[CommuneInDB] = None


# ============================================================================
# SCHÉMAS DOCUMENTS
# ============================================================================

class TypeDocumentBase(BaseModel):
    code: str = Field(..., max_length=50)
    nom: str = Field(..., max_length=255)
    description: Optional[str] = None
    extensions_autorisees: Optional[List[str]] = None
    taille_max_mo: int = Field(default=10, ge=1, le=100)
    actif: bool = True


class TypeDocumentCreate(TypeDocumentBase):
    pass


class TypeDocumentInDB(TypeDocumentBase, TimestampSchema):
    id: UUID

    class Config:
        from_attributes = True


class DocumentBase(BaseModel):
    titre: str = Field(..., max_length=255)
    nom_fichier: str = Field(..., max_length=255)
    chemin_fichier: str
    type_document_id: Optional[UUID] = None
    commune_id: Optional[UUID] = None
    exercice_id: Optional[UUID] = None
    revenu_id: Optional[UUID] = None
    description: Optional[str] = None
    tags: Optional[List[str]] = None


class DocumentCreate(DocumentBase):
    uploaded_by: Optional[UUID] = None


class DocumentInDB(DocumentBase, TimestampSchema):
    id: UUID
    taille_ko: Optional[int] = None
    extension: Optional[str] = None
    indexe: bool = False
    uploaded_by: Optional[UUID] = None

    class Config:
        from_attributes = True


# ============================================================================
# SCHÉMAS NEWSLETTER
# ============================================================================

class NewsletterAbonneBase(BaseModel):
    email: EmailStr
    nom: Optional[str] = Field(None, max_length=255)
    prenom: Optional[str] = Field(None, max_length=255)


class NewsletterAbonneCreate(NewsletterAbonneBase):
    pass


class NewsletterAbonneInDB(NewsletterAbonneBase, TimestampSchema):
    id: UUID
    actif: bool = True
    confirme: bool = False
    confirme_le: Optional[datetime] = None

    class Config:
        from_attributes = True


# ============================================================================
# SCHÉMAS DE RÉPONSE PERSONNALISÉS
# ============================================================================

class TableauCompteAdministratif(BaseModel):
    """Schéma pour le tableau de compte administratif complet"""
    commune: CommuneDetail
    exercice: ExerciceInDB
    periodes: List[PeriodeInDB]
    rubriques: List[RubriqueDetail]
    donnees: List[RevenuDetail]


class StatistiquesCommune(BaseModel):
    """Statistiques pour une commune"""
    commune: CommuneInDB
    total_recettes: Decimal
    total_depenses: Decimal
    solde: Decimal
    nb_projets_miniers: int
    exercices_disponibles: List[int]


class StatistiquesRegion(BaseModel):
    """Statistiques pour une région"""
    region: RegionInDB
    nb_communes: int
    nb_projets_miniers: int
    total_revenus_miniers: Decimal
    communes_top: List[Dict[str, Any]]


# ============================================================================
# SCHÉMAS POUR LES FILTRES
# ============================================================================

class RevenuFilter(BaseModel):
    """Filtres pour la recherche de revenus"""
    commune_code: Optional[str] = None
    region_code: Optional[str] = None
    exercice_annee: Optional[int] = None
    rubrique_code: Optional[str] = None
    projet_minier_id: Optional[UUID] = None
    date_debut: Optional[date] = None
    date_fin: Optional[date] = None
    valide: Optional[bool] = None


class PaginationParams(BaseModel):
    """Paramètres de pagination"""
    page: int = Field(default=1, ge=1)
    page_size: int = Field(default=50, ge=1, le=1000)


class PaginatedResponse(BaseModel):
    """Réponse paginée générique"""
    items: List[Any]
    total: int
    page: int
    page_size: int
    total_pages: int


# Configuration pour permettre la référence circulaire
RubriqueDetail.model_rebuild()
