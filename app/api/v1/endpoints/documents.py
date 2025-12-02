"""
Public documents API endpoints.
Access to public documents and file downloads.
"""

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session, joinedload

from app.api.deps import DbSession, get_db
from app.models.comptabilite import Exercice
from app.models.documents import Document
from app.models.geographie import Commune
from app.models.enums import TypeDocument
from app.schemas.documents import (
    DocumentDownloadInfo,
    DocumentFilter,
    DocumentList,
    DocumentWithDetails,
)

router = APIRouter(prefix="/documents", tags=["Documents"])


@router.get(
    "",
    response_model=list[DocumentList],
    summary="Liste des documents publics",
    description="Retourne la liste des documents publics avec filtres optionnels."
)
async def list_documents(
    commune_id: Optional[int] = Query(
        None,
        description="Filtrer par commune"
    ),
    exercice_annee: Optional[int] = Query(
        None,
        description="Filtrer par année d'exercice"
    ),
    type_document: Optional[TypeDocument] = Query(
        None,
        description="Filtrer par type de document"
    ),
    search: Optional[str] = Query(
        None,
        min_length=2,
        max_length=100,
        description="Recherche dans le titre"
    ),
    limit: int = Query(
        50,
        ge=1,
        le=200,
        description="Nombre maximum de résultats"
    ),
    offset: int = Query(
        0,
        ge=0,
        description="Nombre de résultats à ignorer"
    ),
    db: Session = Depends(get_db),
):
    """
    Get list of public documents with optional filters.

    Only returns documents marked as public.

    - **commune_id**: Filter by commune
    - **exercice_annee**: Filter by fiscal year
    - **type_document**: Filter by document type
    - **search**: Search in title
    - **limit**: Max results (default 50, max 200)
    - **offset**: Skip results for pagination
    """
    query = db.query(Document).filter(Document.public == True)

    if commune_id:
        query = query.filter(Document.commune_id == commune_id)

    if exercice_annee:
        exercice = db.query(Exercice).filter(Exercice.annee == exercice_annee).first()
        if exercice:
            query = query.filter(Document.exercice_id == exercice.id)

    if type_document:
        query = query.filter(Document.type_document == type_document)

    if search:
        query = query.filter(Document.titre.ilike(f"%{search}%"))

    documents = query.order_by(
        Document.created_at.desc()
    ).offset(offset).limit(limit).all()

    return [
        DocumentList(
            id=doc.id,
            type_document=doc.type_document,
            titre=doc.titre,
            nom_fichier=doc.nom_fichier,
            taille_formatee=doc.taille_formatee,
            mime_type=doc.mime_type,
            public=doc.public,
            created_at=doc.created_at
        )
        for doc in documents
    ]


@router.get(
    "/types",
    response_model=list[str],
    summary="Types de documents",
    description="Retourne la liste des types de documents disponibles."
)
async def list_document_types():
    """
    Get list of available document types.
    """
    return [t.value for t in TypeDocument]


@router.get(
    "/by-commune/{commune_id}",
    response_model=list[DocumentList],
    summary="Documents d'une commune",
    description="Retourne les documents publics d'une commune."
)
async def get_documents_by_commune(
    commune_id: int,
    exercice_annee: Optional[int] = Query(
        None,
        description="Filtrer par année d'exercice"
    ),
    db: Session = Depends(get_db),
):
    """
    Get public documents for a specific commune.
    """
    commune = db.query(Commune).filter(Commune.id == commune_id).first()
    if not commune:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Commune non trouvée"
        )

    query = db.query(Document).filter(
        Document.commune_id == commune_id,
        Document.public == True
    )

    if exercice_annee:
        exercice = db.query(Exercice).filter(Exercice.annee == exercice_annee).first()
        if exercice:
            query = query.filter(Document.exercice_id == exercice.id)

    documents = query.order_by(Document.created_at.desc()).all()

    return [
        DocumentList(
            id=doc.id,
            type_document=doc.type_document,
            titre=doc.titre,
            nom_fichier=doc.nom_fichier,
            taille_formatee=doc.taille_formatee,
            mime_type=doc.mime_type,
            public=doc.public,
            created_at=doc.created_at
        )
        for doc in documents
    ]


@router.get(
    "/{document_id}",
    response_model=DocumentWithDetails,
    summary="Détail d'un document",
    description="Retourne les détails d'un document public."
)
async def get_document(
    document_id: int,
    db: Session = Depends(get_db),
):
    """
    Get a public document by ID.
    """
    document = db.query(Document).options(
        joinedload(Document.commune),
        joinedload(Document.exercice),
        joinedload(Document.uploadeur)
    ).filter(
        Document.id == document_id,
        Document.public == True
    ).first()

    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document non trouvé ou non public"
        )

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
        commune_nom=document.commune.nom if document.commune else None,
        exercice_annee=document.exercice.annee if document.exercice else None,
        uploadeur_nom=document.uploadeur.nom_complet if document.uploadeur else None
    )


@router.get(
    "/{document_id}/download",
    response_model=DocumentDownloadInfo,
    summary="Télécharger un document",
    description="Retourne les informations pour télécharger un document."
)
async def download_document(
    document_id: int,
    db: Session = Depends(get_db),
):
    """
    Get download info for a public document.

    Also increments the download counter.

    Note: In production, this endpoint should return a signed URL
    or stream the file directly. This implementation returns the
    file path for simplicity.
    """
    document = db.query(Document).filter(
        Document.id == document_id,
        Document.public == True
    ).first()

    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document non trouvé ou non public"
        )

    # Increment download counter
    document.nb_telechargements += 1
    db.commit()

    return DocumentDownloadInfo(
        id=document.id,
        nom_fichier=document.nom_fichier,
        chemin_fichier=document.chemin_fichier,
        mime_type=document.mime_type,
        taille_octets=document.taille_octets
    )


@router.get(
    "/{document_id}/file",
    summary="Télécharger le fichier",
    description="Télécharge directement le fichier.",
    response_class=FileResponse
)
async def get_document_file(
    document_id: int,
    db: Session = Depends(get_db),
):
    """
    Download the actual file.

    Returns the file as a download response.
    """
    document = db.query(Document).filter(
        Document.id == document_id,
        Document.public == True
    ).first()

    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document non trouvé ou non public"
        )

    # Increment download counter
    document.nb_telechargements += 1
    db.commit()

    # Check if file exists
    import os
    if not os.path.exists(document.chemin_fichier):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Fichier introuvable sur le serveur"
        )

    return FileResponse(
        path=document.chemin_fichier,
        filename=document.nom_fichier,
        media_type=document.mime_type or "application/octet-stream"
    )
