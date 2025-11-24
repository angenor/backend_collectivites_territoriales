"""
Endpoints pour les documents et types de documents
"""

from fastapi import APIRouter, Depends, HTTPException, Query, UploadFile, File
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_, func
from typing import List, Optional
from uuid import UUID
import os
import shutil
from pathlib import Path
import mimetypes

from app.database import get_db
from app.schemas.documents import (
    TypeDocument, TypeDocumentCreate, TypeDocumentUpdate,
    Document, DocumentCreate, DocumentUpdate, DocumentDetail,
    DocumentSearchParams, DocumentSearchResult
)
from app.api.deps import get_current_active_user
from app.models.documents import TypeDocument as TypeDocumentModel, Document as DocumentModel
from app.models.utilisateurs import Utilisateur

router = APIRouter()

# Configuration
UPLOAD_DIR = Path("uploads/documents")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50 MB


# ============================================================================
# TYPES DE DOCUMENTS
# ============================================================================

@router.get("/types-documents", response_model=List[TypeDocument], summary="Liste des types de documents")
def get_types_documents(
    skip: int = 0,
    limit: int = 100,
    actif_only: bool = True,
    db: Session = Depends(get_db)
):
    """
    Récupère la liste de tous les types de documents.

    - **skip**: Nombre d'éléments à ignorer (pagination)
    - **limit**: Nombre maximum d'éléments à retourner
    - **actif_only**: Si True, retourne uniquement les types actifs
    """
    query = db.query(TypeDocumentModel)

    if actif_only:
        query = query.filter(TypeDocumentModel.actif == True)

    types = query.order_by(TypeDocumentModel.nom).offset(skip).limit(limit).all()
    return types


@router.get("/types-documents/{type_id}", response_model=TypeDocument, summary="Détails d'un type de document")
def get_type_document(
    type_id: UUID,
    db: Session = Depends(get_db)
):
    """Récupère un type de document spécifique par son ID."""
    type_doc = db.query(TypeDocumentModel).filter(TypeDocumentModel.id == type_id).first()

    if not type_doc:
        raise HTTPException(
            status_code=404,
            detail=f"Type de document avec l'ID {type_id} introuvable"
        )

    return type_doc


@router.post("/types-documents", response_model=TypeDocument, status_code=201, summary="Créer un type de document")
def create_type_document(
    data: TypeDocumentCreate,
    db: Session = Depends(get_db),
    current_user: Utilisateur = Depends(get_current_active_user)
):
    """Crée un nouveau type de document (nécessite d'être authentifié)."""
    # Vérifier que le code n'existe pas déjà
    existing = db.query(TypeDocumentModel).filter(TypeDocumentModel.code == data.code.upper()).first()
    if existing:
        raise HTTPException(
            status_code=400,
            detail=f"Un type de document avec le code '{data.code}' existe déjà"
        )

    # Créer le nouveau type
    db_type = TypeDocumentModel(
        code=data.code.upper(),
        nom=data.nom,
        description=data.description,
        extensions_autorisees=data.extensions_autorisees,
        taille_max_mo=data.taille_max_mo,
        actif=data.actif
    )

    db.add(db_type)
    db.commit()
    db.refresh(db_type)

    return db_type


@router.put("/types-documents/{type_id}", response_model=TypeDocument, summary="Modifier un type de document")
def update_type_document(
    type_id: UUID,
    data: TypeDocumentUpdate,
    db: Session = Depends(get_db),
    current_user: Utilisateur = Depends(get_current_active_user)
):
    """Met à jour un type de document existant (nécessite d'être authentifié)."""
    type_doc = db.query(TypeDocumentModel).filter(TypeDocumentModel.id == type_id).first()

    if not type_doc:
        raise HTTPException(
            status_code=404,
            detail=f"Type de document avec l'ID {type_id} introuvable"
        )

    # Mettre à jour les champs fournis
    update_data = data.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(type_doc, field, value)

    db.commit()
    db.refresh(type_doc)

    return type_doc


@router.delete("/types-documents/{type_id}", summary="Supprimer un type de document")
def delete_type_document(
    type_id: UUID,
    db: Session = Depends(get_db),
    current_user: Utilisateur = Depends(get_current_active_user)
):
    """Désactive un type de document (soft delete - nécessite d'être authentifié)."""
    type_doc = db.query(TypeDocumentModel).filter(TypeDocumentModel.id == type_id).first()

    if not type_doc:
        raise HTTPException(
            status_code=404,
            detail=f"Type de document avec l'ID {type_id} introuvable"
        )

    # Soft delete : désactiver au lieu de supprimer
    type_doc.actif = False
    db.commit()

    return {"message": f"Type de document '{type_doc.nom}' désactivé avec succès"}


# ============================================================================
# DOCUMENTS - CRUD
# ============================================================================

@router.get("/documents", response_model=List[DocumentDetail], summary="Liste des documents")
def get_documents(
    skip: int = 0,
    limit: int = 100,
    type_document_id: UUID = Query(None),
    commune_id: UUID = Query(None),
    exercice_id: UUID = Query(None),
    extension: str = Query(None),
    db: Session = Depends(get_db)
):
    """
    Récupère la liste de tous les documents avec filtres optionnels.

    - **skip**: Nombre d'éléments à ignorer (pagination)
    - **limit**: Nombre maximum d'éléments à retourner
    - **type_document_id**: Filtrer par type de document
    - **commune_id**: Filtrer par commune
    - **exercice_id**: Filtrer par exercice
    - **extension**: Filtrer par extension (.pdf, .xlsx, etc.)
    """
    query = db.query(DocumentModel)

    if type_document_id:
        query = query.filter(DocumentModel.type_document_id == type_document_id)

    if commune_id:
        query = query.filter(DocumentModel.commune_id == commune_id)

    if exercice_id:
        query = query.filter(DocumentModel.exercice_id == exercice_id)

    if extension:
        query = query.filter(DocumentModel.extension == extension)

    documents = query.order_by(DocumentModel.created_at.desc()).offset(skip).limit(limit).all()
    return documents


@router.get("/documents/{document_id}", response_model=DocumentDetail, summary="Détails d'un document")
def get_document(
    document_id: UUID,
    db: Session = Depends(get_db)
):
    """Récupère un document spécifique par son ID."""
    document = db.query(DocumentModel).filter(DocumentModel.id == document_id).first()

    if not document:
        raise HTTPException(
            status_code=404,
            detail=f"Document avec l'ID {document_id} introuvable"
        )

    return document


@router.post("/documents/upload", response_model=DocumentDetail, status_code=201, summary="Uploader un document")
async def upload_document(
    file: UploadFile = File(...),
    titre: str = Query(...),
    description: Optional[str] = Query(None),
    type_document_id: Optional[UUID] = Query(None),
    commune_id: Optional[UUID] = Query(None),
    exercice_id: Optional[UUID] = Query(None),
    revenu_id: Optional[UUID] = Query(None),
    tags: Optional[str] = Query(None),  # Comma-separated tags
    db: Session = Depends(get_db),
    current_user: Utilisateur = Depends(get_current_active_user)
):
    """
    Upload un nouveau document (nécessite d'être authentifié).

    - **file**: Fichier à uploader
    - **titre**: Titre du document
    - **description**: Description (optionnel)
    - **type_document_id**: Type de document (optionnel)
    - **commune_id**, **exercice_id**, **revenu_id**: Liens optionnels
    - **tags**: Tags séparés par des virgules (ex: "budget,2024,rapport")
    """
    # Vérifier la taille du fichier
    content = await file.read()
    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=400,
            detail=f"Fichier trop volumineux (max {MAX_FILE_SIZE // 1024 // 1024} MB)"
        )

    # Réinitialiser le pointeur de fichier
    await file.seek(0)

    # Extraire l'extension
    extension = Path(file.filename).suffix.lower()

    # Vérifier le type de document si spécifié
    if type_document_id:
        type_doc = db.query(TypeDocumentModel).filter(TypeDocumentModel.id == type_document_id).first()
        if type_doc and type_doc.extensions_autorisees:
            if extension not in type_doc.extensions_autorisees:
                raise HTTPException(
                    status_code=400,
                    detail=f"Extension {extension} non autorisée pour ce type de document. Autorisées: {', '.join(type_doc.extensions_autorisees)}"
                )

    # Générer un nom de fichier unique
    import uuid
    unique_filename = f"{uuid.uuid4()}{extension}"
    file_path = UPLOAD_DIR / unique_filename

    # Sauvegarder le fichier
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Parser les tags
    tags_list = [tag.strip() for tag in tags.split(",")] if tags else []

    # Créer l'enregistrement en base
    db_document = DocumentModel(
        titre=titre,
        nom_fichier=file.filename,
        chemin_fichier=str(file_path),
        extension=extension,
        taille_ko=len(content) // 1024,
        type_document_id=type_document_id,
        commune_id=commune_id,
        exercice_id=exercice_id,
        revenu_id=revenu_id,
        description=description,
        tags=tags_list,
        uploaded_by=current_user.id,
        indexe=False  # L'indexation sera faite de manière asynchrone
    )

    db.add(db_document)
    db.commit()
    db.refresh(db_document)

    return db_document


@router.put("/documents/{document_id}", response_model=DocumentDetail, summary="Modifier un document")
def update_document(
    document_id: UUID,
    data: DocumentUpdate,
    db: Session = Depends(get_db),
    current_user: Utilisateur = Depends(get_current_active_user)
):
    """Met à jour les métadonnées d'un document (nécessite d'être authentifié)."""
    document = db.query(DocumentModel).filter(DocumentModel.id == document_id).first()

    if not document:
        raise HTTPException(
            status_code=404,
            detail=f"Document avec l'ID {document_id} introuvable"
        )

    # Mettre à jour les champs fournis
    update_data = data.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(document, field, value)

    db.commit()
    db.refresh(document)

    return document


@router.delete("/documents/{document_id}", summary="Supprimer un document")
def delete_document(
    document_id: UUID,
    db: Session = Depends(get_db),
    current_user: Utilisateur = Depends(get_current_active_user)
):
    """Supprime un document et son fichier physique (nécessite d'être authentifié)."""
    document = db.query(DocumentModel).filter(DocumentModel.id == document_id).first()

    if not document:
        raise HTTPException(
            status_code=404,
            detail=f"Document avec l'ID {document_id} introuvable"
        )

    # Supprimer le fichier physique
    file_path = Path(document.chemin_fichier)
    if file_path.exists():
        file_path.unlink()

    # Supprimer l'enregistrement
    db.delete(document)
    db.commit()

    return {"message": f"Document '{document.titre}' supprimé avec succès"}


# ============================================================================
# RECHERCHE FULL-TEXT
# ============================================================================

@router.get("/documents/search/full-text", response_model=List[DocumentDetail], summary="Recherche full-text")
def search_documents(
    query: str = Query(..., min_length=2, description="Texte à rechercher"),
    type_document_id: UUID = Query(None),
    commune_id: UUID = Query(None),
    exercice_id: UUID = Query(None),
    tags: Optional[str] = Query(None, description="Tags séparés par des virgules"),
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Recherche full-text dans les documents (titre, description, contenu_texte, tags).

    - **query**: Texte à rechercher (min 2 caractères)
    - **type_document_id**: Filtrer par type de document
    - **commune_id**: Filtrer par commune
    - **exercice_id**: Filtrer par exercice
    - **tags**: Filtrer par tags (séparés par des virgules)
    """
    # Construire la requête de base
    base_query = db.query(DocumentModel)

    # Recherche full-text PostgreSQL avec tsvector
    # Recherche dans titre, description, et contenu_texte
    search_vector = func.to_tsvector('french',
        func.coalesce(DocumentModel.titre, '') + ' ' +
        func.coalesce(DocumentModel.description, '') + ' ' +
        func.coalesce(DocumentModel.contenu_texte, '')
    )
    search_query = func.plainto_tsquery('french', query)

    base_query = base_query.filter(search_vector.op('@@')(search_query))

    # Appliquer les filtres additionnels
    if type_document_id:
        base_query = base_query.filter(DocumentModel.type_document_id == type_document_id)

    if commune_id:
        base_query = base_query.filter(DocumentModel.commune_id == commune_id)

    if exercice_id:
        base_query = base_query.filter(DocumentModel.exercice_id == exercice_id)

    if tags:
        tags_list = [tag.strip() for tag in tags.split(",")]
        # Recherche si au moins un tag correspond
        base_query = base_query.filter(DocumentModel.tags.overlap(tags_list))

    # Ordonner par pertinence (score ts_rank)
    rank = func.ts_rank(search_vector, search_query)
    documents = base_query.order_by(rank.desc()).offset(skip).limit(limit).all()

    return documents


@router.get("/documents/download/{document_id}", summary="Télécharger un document")
async def download_document(
    document_id: UUID,
    db: Session = Depends(get_db)
):
    """Télécharge un document par son ID."""
    from fastapi.responses import FileResponse

    document = db.query(DocumentModel).filter(DocumentModel.id == document_id).first()

    if not document:
        raise HTTPException(
            status_code=404,
            detail=f"Document avec l'ID {document_id} introuvable"
        )

    file_path = Path(document.chemin_fichier)
    if not file_path.exists():
        raise HTTPException(
            status_code=404,
            detail="Fichier physique introuvable"
        )

    # Déterminer le type MIME
    mime_type, _ = mimetypes.guess_type(str(file_path))
    if not mime_type:
        mime_type = "application/octet-stream"

    return FileResponse(
        path=str(file_path),
        filename=document.nom_fichier,
        media_type=mime_type
    )
