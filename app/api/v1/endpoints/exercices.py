"""
Endpoints pour les exercices fiscaux et périodes
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from app.database import get_db
from app.schemas.exercices import (
    Exercice, ExerciceCreate, ExerciceUpdate, ExerciceDetail,
    Periode, PeriodeCreate, PeriodeUpdate, PeriodeDetail
)
from app.api.deps import get_current_active_user
from app.models.revenus import Exercice as ExerciceModel, Periode as PeriodeModel

router = APIRouter()


# ============================================================================
# EXERCICES FISCAUX
# ============================================================================

@router.get("/exercices", response_model=List[ExerciceDetail], summary="Liste des exercices fiscaux")
def get_exercices(
    skip: int = 0,
    limit: int = 100,
    actif_only: bool = True,
    statut: str = Query(None),
    db: Session = Depends(get_db)
):
    """
    Récupère la liste de tous les exercices fiscaux.

    - **skip**: Nombre d'éléments à ignorer (pagination)
    - **limit**: Nombre maximum d'éléments à retourner
    - **actif_only**: Si True, retourne uniquement les exercices actifs
    - **statut**: Filtrer par statut (ouvert, cloturé)
    """
    query = db.query(ExerciceModel)

    if actif_only:
        query = query.filter(ExerciceModel.actif == True)

    if statut:
        query = query.filter(ExerciceModel.statut == statut)

    exercices = query.order_by(ExerciceModel.annee.desc()).offset(skip).limit(limit).all()
    return exercices


@router.get("/exercices/{exercice_id}", response_model=ExerciceDetail, summary="Détails d'un exercice")
def get_exercice(
    exercice_id: UUID,
    db: Session = Depends(get_db)
):
    """Récupère un exercice fiscal spécifique par son ID."""
    exercice = db.query(ExerciceModel).filter(ExerciceModel.id == exercice_id).first()

    if not exercice:
        raise HTTPException(
            status_code=404,
            detail=f"Exercice avec l'ID {exercice_id} introuvable"
        )

    return exercice


@router.post("/exercices", response_model=ExerciceDetail, status_code=201, summary="Créer un exercice fiscal")
def create_exercice(
    data: ExerciceCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """Crée un nouvel exercice fiscal (nécessite d'être authentifié)."""
    # Vérifier que l'année n'existe pas déjà
    existing = db.query(ExerciceModel).filter(ExerciceModel.annee == data.annee).first()
    if existing:
        raise HTTPException(
            status_code=400,
            detail=f"Un exercice pour l'année {data.annee} existe déjà"
        )

    # Créer le nouvel exercice
    db_exercice = ExerciceModel(
        annee=data.annee,
        date_debut=data.date_debut,
        date_fin=data.date_fin,
        statut=data.statut,
        actif=data.actif
    )

    db.add(db_exercice)
    db.commit()
    db.refresh(db_exercice)

    return db_exercice


@router.put("/exercices/{exercice_id}", response_model=ExerciceDetail, summary="Modifier un exercice fiscal")
def update_exercice(
    exercice_id: UUID,
    data: ExerciceUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """Met à jour un exercice fiscal existant (nécessite d'être authentifié)."""
    exercice = db.query(ExerciceModel).filter(ExerciceModel.id == exercice_id).first()

    if not exercice:
        raise HTTPException(
            status_code=404,
            detail=f"Exercice avec l'ID {exercice_id} introuvable"
        )

    # Mettre à jour les champs fournis
    update_data = data.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(exercice, field, value)

    db.commit()
    db.refresh(exercice)

    return exercice


@router.delete("/exercices/{exercice_id}", summary="Supprimer un exercice fiscal")
def delete_exercice(
    exercice_id: UUID,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """Désactive un exercice fiscal (soft delete - nécessite d'être authentifié)."""
    exercice = db.query(ExerciceModel).filter(ExerciceModel.id == exercice_id).first()

    if not exercice:
        raise HTTPException(
            status_code=404,
            detail=f"Exercice avec l'ID {exercice_id} introuvable"
        )

    # Soft delete : désactiver au lieu de supprimer
    exercice.actif = False
    db.commit()

    return {"message": f"Exercice {exercice.annee} désactivé avec succès"}


# ============================================================================
# PÉRIODES
# ============================================================================

@router.get("/periodes", response_model=List[PeriodeDetail], summary="Liste des périodes")
def get_periodes(
    skip: int = 0,
    limit: int = 100,
    actif_only: bool = True,
    exercice_id: UUID = Query(None),
    type_periode: str = Query(None),
    db: Session = Depends(get_db)
):
    """
    Récupère la liste de toutes les périodes.

    - **skip**: Nombre d'éléments à ignorer (pagination)
    - **limit**: Nombre maximum d'éléments à retourner
    - **actif_only**: Si True, retourne uniquement les périodes actives
    - **exercice_id**: Filtrer par exercice fiscal
    - **type_periode**: Filtrer par type (mensuel, trimestriel, etc.)
    """
    query = db.query(PeriodeModel)

    if actif_only:
        query = query.filter(PeriodeModel.actif == True)

    if exercice_id:
        query = query.filter(PeriodeModel.exercice_id == exercice_id)

    if type_periode:
        query = query.filter(PeriodeModel.type_periode == type_periode)

    periodes = query.order_by(PeriodeModel.ordre, PeriodeModel.date_debut).offset(skip).limit(limit).all()
    return periodes


@router.get("/periodes/{periode_id}", response_model=PeriodeDetail, summary="Détails d'une période")
def get_periode(
    periode_id: UUID,
    db: Session = Depends(get_db)
):
    """Récupère une période spécifique par son ID."""
    periode = db.query(PeriodeModel).filter(PeriodeModel.id == periode_id).first()

    if not periode:
        raise HTTPException(
            status_code=404,
            detail=f"Période avec l'ID {periode_id} introuvable"
        )

    return periode


@router.post("/periodes", response_model=PeriodeDetail, status_code=201, summary="Créer une période")
def create_periode(
    data: PeriodeCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """Crée une nouvelle période (nécessite d'être authentifié)."""
    # Vérifier que le code n'existe pas déjà pour cet exercice
    existing = db.query(PeriodeModel).filter(
        PeriodeModel.exercice_id == data.exercice_id,
        PeriodeModel.code == data.code
    ).first()
    if existing:
        raise HTTPException(
            status_code=400,
            detail=f"Une période avec le code '{data.code}' existe déjà pour cet exercice"
        )

    # Créer la nouvelle période
    db_periode = PeriodeModel(
        code=data.code,
        nom=data.nom,
        exercice_id=data.exercice_id,
        date_debut=data.date_debut,
        date_fin=data.date_fin,
        type_periode=data.type_periode,
        ordre=data.ordre,
        actif=data.actif
    )

    db.add(db_periode)
    db.commit()
    db.refresh(db_periode)

    return db_periode


@router.put("/periodes/{periode_id}", response_model=PeriodeDetail, summary="Modifier une période")
def update_periode(
    periode_id: UUID,
    data: PeriodeUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """Met à jour une période existante (nécessite d'être authentifié)."""
    periode = db.query(PeriodeModel).filter(PeriodeModel.id == periode_id).first()

    if not periode:
        raise HTTPException(
            status_code=404,
            detail=f"Période avec l'ID {periode_id} introuvable"
        )

    # Mettre à jour les champs fournis
    update_data = data.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(periode, field, value)

    db.commit()
    db.refresh(periode)

    return periode


@router.delete("/periodes/{periode_id}", summary="Supprimer une période")
def delete_periode(
    periode_id: UUID,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """Désactive une période (soft delete - nécessite d'être authentifié)."""
    periode = db.query(PeriodeModel).filter(PeriodeModel.id == periode_id).first()

    if not periode:
        raise HTTPException(
            status_code=404,
            detail=f"Période avec l'ID {periode_id} introuvable"
        )

    # Soft delete : désactiver au lieu de supprimer
    periode.actif = False
    db.commit()

    return {"message": f"Période '{periode.nom}' désactivée avec succès"}
