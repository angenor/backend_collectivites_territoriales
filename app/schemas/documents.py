"""
Pydantic schemas for documents.
Document model for file attachments.
"""

from datetime import datetime
from typing import Optional

from pydantic import Field

from app.models.enums import TypeDocument
from app.schemas.base import BaseSchema, TimestampSchema


# =====================
# Document Schemas
# =====================

class DocumentBase(BaseSchema):
    """Base schema for Document."""
    commune_id: Optional[int] = None
    exercice_id: Optional[int] = None
    type_document: TypeDocument
    titre: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    public: bool = True


class DocumentCreate(DocumentBase):
    """Schema for creating a Document (metadata only, file uploaded separately)."""
    nom_fichier: str = Field(..., min_length=1, max_length=255)
    chemin_fichier: str = Field(..., min_length=1, max_length=500)
    taille_octets: Optional[int] = Field(None, ge=0)
    mime_type: Optional[str] = Field(None, max_length=100)


class DocumentUpdate(BaseSchema):
    """Schema for updating a Document."""
    commune_id: Optional[int] = None
    exercice_id: Optional[int] = None
    type_document: Optional[TypeDocument] = None
    titre: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    public: Optional[bool] = None


class DocumentRead(DocumentBase, TimestampSchema):
    """Schema for reading a Document."""
    id: int
    nom_fichier: str
    chemin_fichier: str
    taille_octets: Optional[int] = None
    mime_type: Optional[str] = None
    uploade_par: Optional[int] = None
    nb_telechargements: int = 0
    # Computed fields
    taille_formatee: Optional[str] = None
    extension: Optional[str] = None


class DocumentList(BaseSchema):
    """Simplified schema for listing documents."""
    id: int
    type_document: TypeDocument
    titre: str
    nom_fichier: str
    taille_formatee: Optional[str] = None
    mime_type: Optional[str] = None
    public: bool
    created_at: Optional[datetime] = None


class DocumentWithDetails(DocumentRead):
    """Document with commune and exercise info."""
    commune_nom: Optional[str] = None
    exercice_annee: Optional[int] = None
    uploadeur_nom: Optional[str] = None


# =====================
# Upload Schemas
# =====================

class DocumentUploadResponse(BaseSchema):
    """Response after file upload."""
    document_id: int
    nom_fichier: str
    chemin_fichier: str
    taille_octets: int
    mime_type: str
    message: str = "Fichier uploadé avec succès"


class DocumentDownloadInfo(BaseSchema):
    """Info for document download."""
    id: int
    nom_fichier: str
    chemin_fichier: str
    mime_type: Optional[str] = None
    taille_octets: Optional[int] = None


# =====================
# Filter/Search Schemas
# =====================

class DocumentFilter(BaseSchema):
    """Filter parameters for document search."""
    commune_id: Optional[int] = None
    exercice_id: Optional[int] = None
    type_document: Optional[TypeDocument] = None
    public: Optional[bool] = None
    search: Optional[str] = Field(None, max_length=100)


# =====================
# Annexes Schemas
# =====================

class NewsletterAbonneBase(BaseSchema):
    """Base schema for newsletter subscriber."""
    email: str = Field(..., max_length=255)
    nom: Optional[str] = Field(None, max_length=100)
    actif: bool = True


class NewsletterAbonneCreate(NewsletterAbonneBase):
    """Schema for creating a subscriber."""
    pass


class NewsletterAbonneRead(NewsletterAbonneBase, TimestampSchema):
    """Schema for reading a subscriber."""
    id: int
    date_inscription: datetime
    date_desinscription: Optional[datetime] = None


class StatistiqueVisiteRead(BaseSchema):
    """Schema for reading visit statistics."""
    id: int
    commune_id: Optional[int] = None
    page_url: str
    date_visite: datetime
    ip_anonymisee: Optional[str] = None
    user_agent: Optional[str] = None
    referrer: Optional[str] = None
    # Additional info
    commune_nom: Optional[str] = None


class StatistiqueVisiteCreate(BaseSchema):
    """Schema for creating visit statistic."""
    commune_id: Optional[int] = None
    page_url: str = Field(..., max_length=500)
    ip_anonymisee: Optional[str] = Field(None, max_length=45)
    user_agent: Optional[str] = None
    referrer: Optional[str] = Field(None, max_length=500)


class AuditLogRead(BaseSchema):
    """Schema for reading audit log entry."""
    id: int
    table_name: str
    record_id: int
    action: str
    old_values: Optional[dict] = None
    new_values: Optional[dict] = None
    utilisateur_id: Optional[int] = None
    ip_address: Optional[str] = None
    created_at: datetime
    # Additional info
    utilisateur_email: Optional[str] = None


class AuditLogFilter(BaseSchema):
    """Filter parameters for audit log search."""
    table_name: Optional[str] = None
    record_id: Optional[int] = None
    action: Optional[str] = None
    utilisateur_id: Optional[int] = None
    date_debut: Optional[datetime] = None
    date_fin: Optional[datetime] = None


# =====================
# Statistics Aggregation
# =====================

class StatistiquesVisitesResume(BaseSchema):
    """Summary of visit statistics."""
    periode_debut: datetime
    periode_fin: datetime
    total_visites: int
    visites_uniques: int
    pages_les_plus_visitees: list[dict]
    communes_les_plus_consultees: list[dict]


class StatistiquesDocuments(BaseSchema):
    """Summary of document statistics."""
    total_documents: int
    par_type: dict[str, int]
    total_telechargements: int
    documents_publics: int
    documents_prives: int
