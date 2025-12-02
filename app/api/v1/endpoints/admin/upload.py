"""
Admin API endpoints for file uploads.
Handle file uploads for images and documents.
"""

import os
import uuid
from datetime import datetime
from pathlib import Path
from typing import Optional

from fastapi import APIRouter, Depends, File, HTTPException, Query, UploadFile, status
from sqlalchemy.orm import Session

from app.api.deps import CurrentEditor, get_db
from app.core.config import settings
from app.models.documents import Document
from app.models.comptabilite import Exercice
from app.models.geographie import Commune
from app.models.enums import TypeDocument
from app.schemas.documents import DocumentRead, DocumentWithDetails
from app.schemas.base import Message

router = APIRouter(prefix="/upload", tags=["Admin - Upload"])

# Allowed file types
ALLOWED_IMAGE_TYPES = {
    "image/jpeg": ".jpg",
    "image/png": ".png",
    "image/gif": ".gif",
    "image/webp": ".webp",
}

ALLOWED_DOCUMENT_TYPES = {
    "application/pdf": ".pdf",
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet": ".xlsx",
    "application/vnd.ms-excel": ".xls",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document": ".docx",
    "application/msword": ".doc",
}

# Max file sizes (in bytes)
MAX_IMAGE_SIZE = 5 * 1024 * 1024  # 5MB
MAX_DOCUMENT_SIZE = 20 * 1024 * 1024  # 20MB


def get_upload_dir() -> Path:
    """Get upload directory, creating it if needed."""
    upload_dir = Path(settings.UPLOAD_DIR if hasattr(settings, "UPLOAD_DIR") else "uploads")
    upload_dir.mkdir(parents=True, exist_ok=True)
    return upload_dir


def format_file_size(size_bytes: int) -> str:
    """Format file size in human readable format."""
    if size_bytes < 1024:
        return f"{size_bytes} B"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.1f} KB"
    else:
        return f"{size_bytes / (1024 * 1024):.1f} MB"


@router.post(
    "/image",
    response_model=dict,
    summary="Upload une image",
    description="Upload une image (JPEG, PNG, GIF, WebP).",
)
async def upload_image(
    file: UploadFile = File(..., description="Fichier image"),
    folder: str = Query("images", description="Dossier de destination"),
    current_user: CurrentEditor = None,
):
    """
    Upload an image file.

    Returns the URL path to the uploaded image.
    """
    # Validate file type
    if file.content_type not in ALLOWED_IMAGE_TYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Type de fichier non autorisé. Types acceptés: {', '.join(ALLOWED_IMAGE_TYPES.keys())}",
        )

    # Read content
    content = await file.read()

    # Validate size
    if len(content) > MAX_IMAGE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Fichier trop volumineux. Maximum: {format_file_size(MAX_IMAGE_SIZE)}",
        )

    # Generate unique filename
    ext = ALLOWED_IMAGE_TYPES[file.content_type]
    filename = f"{uuid.uuid4().hex}{ext}"

    # Create destination directory
    upload_dir = get_upload_dir() / folder
    upload_dir.mkdir(parents=True, exist_ok=True)

    # Save file
    file_path = upload_dir / filename
    with open(file_path, "wb") as f:
        f.write(content)

    # Return URL
    url = f"/uploads/{folder}/{filename}"

    return {
        "success": True,
        "url": url,
        "filename": filename,
        "original_name": file.filename,
        "size": len(content),
        "size_formatted": format_file_size(len(content)),
        "mime_type": file.content_type,
    }


@router.post(
    "/document",
    response_model=DocumentWithDetails,
    summary="Upload un document",
    description="Upload un document (PDF, Excel, Word) et l'enregistre en base.",
)
async def upload_document(
    file: UploadFile = File(..., description="Fichier document"),
    commune_id: int = Query(..., description="ID de la commune"),
    exercice_id: int = Query(..., description="ID de l'exercice"),
    type_document: TypeDocument = Query(..., description="Type de document"),
    titre: str = Query(..., min_length=1, max_length=255, description="Titre du document"),
    description: Optional[str] = Query(None, description="Description"),
    public: bool = Query(True, description="Document public"),
    current_user: CurrentEditor = None,
    db: Session = Depends(get_db),
):
    """
    Upload a document and save it to the database.
    """
    # Validate file type
    if file.content_type not in ALLOWED_DOCUMENT_TYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Type de fichier non autorisé. Types acceptés: PDF, Excel, Word",
        )

    # Validate commune
    commune = db.query(Commune).filter(Commune.id == commune_id).first()
    if not commune:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Commune non trouvée"
        )

    # Validate exercice
    exercice = db.query(Exercice).filter(Exercice.id == exercice_id).first()
    if not exercice:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Exercice non trouvé"
        )

    # Read content
    content = await file.read()

    # Validate size
    if len(content) > MAX_DOCUMENT_SIZE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Fichier trop volumineux. Maximum: {format_file_size(MAX_DOCUMENT_SIZE)}",
        )

    # Generate unique filename
    ext = ALLOWED_DOCUMENT_TYPES[file.content_type]
    filename = f"{uuid.uuid4().hex}{ext}"

    # Create destination directory
    upload_dir = get_upload_dir() / "documents" / str(commune_id) / str(exercice.annee)
    upload_dir.mkdir(parents=True, exist_ok=True)

    # Save file
    file_path = upload_dir / filename
    with open(file_path, "wb") as f:
        f.write(content)

    # Create database entry
    document = Document(
        commune_id=commune_id,
        exercice_id=exercice_id,
        type_document=type_document,
        titre=titre,
        description=description,
        public=public,
        nom_fichier=file.filename,
        chemin_fichier=str(file_path),
        taille_octets=len(content),
        mime_type=file.content_type,
        uploade_par=current_user.id,
    )
    db.add(document)
    db.commit()
    db.refresh(document)

    return DocumentWithDetails(
        id=document.id,
        commune_id=document.commune_id,
        exercice_id=document.exercice_id,
        type_document=document.type_document,
        titre=document.titre,
        description=document.description,
        public=document.public,
        nom_fichier=document.nom_fichier,
        chemin_fichier=document.chemin_fichier,
        taille_octets=document.taille_octets,
        mime_type=document.mime_type,
        uploade_par=document.uploade_par,
        nb_telechargements=document.nb_telechargements,
        taille_formatee=document.taille_formatee,
        extension=document.extension,
        created_at=document.created_at,
        updated_at=document.updated_at,
        commune_nom=commune.nom,
        exercice_annee=exercice.annee,
        uploadeur_nom=current_user.nom_complet,
    )


@router.delete(
    "/document/{document_id}",
    response_model=Message,
    summary="Supprimer un document",
    description="Supprime un document de la base et du système de fichiers.",
)
async def delete_document(
    document_id: int,
    current_user: CurrentEditor = None,
    db: Session = Depends(get_db),
):
    """
    Delete a document.
    """
    document = db.query(Document).filter(Document.id == document_id).first()

    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Document non trouvé"
        )

    # Delete file from filesystem
    if document.chemin_fichier and os.path.exists(document.chemin_fichier):
        try:
            os.remove(document.chemin_fichier)
        except OSError:
            pass  # File might not exist

    # Delete from database
    db.delete(document)
    db.commit()

    return Message(message="Document supprimé")


@router.put(
    "/document/{document_id}",
    response_model=DocumentWithDetails,
    summary="Modifier un document",
    description="Modifie les métadonnées d'un document.",
)
async def update_document(
    document_id: int,
    titre: Optional[str] = Query(None, min_length=1, max_length=255),
    description: Optional[str] = Query(None),
    type_document: Optional[TypeDocument] = Query(None),
    public: Optional[bool] = Query(None),
    current_user: CurrentEditor = None,
    db: Session = Depends(get_db),
):
    """
    Update document metadata.
    """
    document = db.query(Document).filter(Document.id == document_id).first()

    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Document non trouvé"
        )

    if titre is not None:
        document.titre = titre
    if description is not None:
        document.description = description
    if type_document is not None:
        document.type_document = type_document
    if public is not None:
        document.public = public

    db.commit()
    db.refresh(document)

    commune = db.query(Commune).filter(Commune.id == document.commune_id).first()
    exercice = db.query(Exercice).filter(Exercice.id == document.exercice_id).first()

    return DocumentWithDetails(
        id=document.id,
        commune_id=document.commune_id,
        exercice_id=document.exercice_id,
        type_document=document.type_document,
        titre=document.titre,
        description=document.description,
        public=document.public,
        nom_fichier=document.nom_fichier,
        chemin_fichier=document.chemin_fichier,
        taille_octets=document.taille_octets,
        mime_type=document.mime_type,
        uploade_par=document.uploade_par,
        nb_telechargements=document.nb_telechargements,
        taille_formatee=document.taille_formatee,
        extension=document.extension,
        created_at=document.created_at,
        updated_at=document.updated_at,
        commune_nom=commune.nom if commune else None,
        exercice_annee=exercice.annee if exercice else None,
        uploadeur_nom=None,
    )


@router.get(
    "/documents",
    response_model=list[DocumentWithDetails],
    summary="Liste des documents",
    description="Liste tous les documents avec filtres.",
)
async def list_documents(
    commune_id: Optional[int] = Query(None, description="Filtrer par commune"),
    exercice_id: Optional[int] = Query(None, description="Filtrer par exercice"),
    type_document: Optional[TypeDocument] = Query(None, description="Filtrer par type"),
    public: Optional[bool] = Query(None, description="Filtrer par visibilité"),
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
    current_user: CurrentEditor = None,
    db: Session = Depends(get_db),
):
    """
    List all documents with filters.
    """
    query = db.query(Document)

    if commune_id:
        query = query.filter(Document.commune_id == commune_id)
    if exercice_id:
        query = query.filter(Document.exercice_id == exercice_id)
    if type_document:
        query = query.filter(Document.type_document == type_document)
    if public is not None:
        query = query.filter(Document.public == public)

    documents = query.order_by(Document.created_at.desc()).offset(offset).limit(limit).all()

    results = []
    for doc in documents:
        commune = db.query(Commune).filter(Commune.id == doc.commune_id).first()
        exercice = db.query(Exercice).filter(Exercice.id == doc.exercice_id).first()

        results.append(
            DocumentWithDetails(
                id=doc.id,
                commune_id=doc.commune_id,
                exercice_id=doc.exercice_id,
                type_document=doc.type_document,
                titre=doc.titre,
                description=doc.description,
                public=doc.public,
                nom_fichier=doc.nom_fichier,
                chemin_fichier=doc.chemin_fichier,
                taille_octets=doc.taille_octets,
                mime_type=doc.mime_type,
                uploade_par=doc.uploade_par,
                nb_telechargements=doc.nb_telechargements,
                taille_formatee=doc.taille_formatee,
                extension=doc.extension,
                created_at=doc.created_at,
                updated_at=doc.updated_at,
                commune_nom=commune.nom if commune else None,
                exercice_annee=exercice.annee if exercice else None,
                uploadeur_nom=None,
            )
        )

    return results
