"""
Schémas Pydantic pour les documents et types de documents
"""

from pydantic import BaseModel, Field
from typing import Optional, List
from uuid import UUID
from datetime import datetime

from app.schemas.common import TimestampSchema


# ============================================================================
# TYPES DE DOCUMENTS
# ============================================================================

class TypeDocumentBase(BaseModel):
    code: str = Field(..., max_length=50, description="Code unique du type de document")
    nom: str = Field(..., max_length=255, description="Nom du type de document")
    description: Optional[str] = Field(None, description="Description")
    extensions_autorisees: Optional[List[str]] = Field(None, description="Extensions autorisées (ex: ['.pdf', '.xlsx'])")
    taille_max_mo: Optional[int] = Field(10, description="Taille maximale en Mo")
    actif: bool = True


class TypeDocumentCreate(TypeDocumentBase):
    pass


class TypeDocumentUpdate(BaseModel):
    nom: Optional[str] = Field(None, max_length=255)
    description: Optional[str] = None
    extensions_autorisees: Optional[List[str]] = None
    taille_max_mo: Optional[int] = None
    actif: Optional[bool] = None


class TypeDocument(TypeDocumentBase, TimestampSchema):
    id: UUID

    model_config = {"from_attributes": True}


# ============================================================================
# DOCUMENTS
# ============================================================================

class DocumentBase(BaseModel):
    titre: str = Field(..., max_length=255, description="Titre du document")
    description: Optional[str] = Field(None, description="Description")
    type_document_id: Optional[UUID] = Field(None, description="ID du type de document")
    commune_id: Optional[UUID] = Field(None, description="ID de la commune")
    exercice_id: Optional[UUID] = Field(None, description="ID de l'exercice")
    revenu_id: Optional[UUID] = Field(None, description="ID du revenu")
    tags: Optional[List[str]] = Field(None, description="Tags pour la recherche")


class DocumentCreate(DocumentBase):
    nom_fichier: str = Field(..., max_length=255, description="Nom du fichier")
    chemin_fichier: str = Field(..., description="Chemin de stockage")
    extension: Optional[str] = Field(None, max_length=10)
    taille_ko: Optional[int] = None
    contenu_texte: Optional[str] = Field(None, description="Contenu extrait pour indexation")
    uploaded_by: Optional[UUID] = None


class DocumentUpdate(BaseModel):
    titre: Optional[str] = Field(None, max_length=255)
    description: Optional[str] = None
    type_document_id: Optional[UUID] = None
    commune_id: Optional[UUID] = None
    exercice_id: Optional[UUID] = None
    revenu_id: Optional[UUID] = None
    tags: Optional[List[str]] = None
    indexe: Optional[bool] = None


class Document(DocumentBase, TimestampSchema):
    id: UUID
    nom_fichier: str
    chemin_fichier: str
    extension: Optional[str] = None
    taille_ko: Optional[int] = None
    indexe: bool = False
    uploaded_by: Optional[UUID] = None

    model_config = {"from_attributes": True}


class DocumentDetail(Document):
    """Document avec relations"""
    type_document: Optional[TypeDocument] = None
    # Note: commune, exercice could be added here if needed


# ============================================================================
# RECHERCHE
# ============================================================================

class DocumentSearchParams(BaseModel):
    """Paramètres de recherche de documents"""
    query: Optional[str] = Field(None, description="Texte à rechercher (full-text)")
    type_document_id: Optional[UUID] = None
    commune_id: Optional[UUID] = None
    exercice_id: Optional[UUID] = None
    tags: Optional[List[str]] = None
    extension: Optional[str] = None
    date_debut: Optional[datetime] = None
    date_fin: Optional[datetime] = None
    skip: int = 0
    limit: int = 100


class DocumentSearchResult(BaseModel):
    """Résultat de recherche avec score de pertinence"""
    document: DocumentDetail
    score: Optional[float] = Field(None, description="Score de pertinence (pour full-text search)")
    highlight: Optional[str] = Field(None, description="Extrait avec mise en évidence")
