"""
Admin API endpoints for fiscal year (exercice) management.
CRUD operations for exercices (admin only).
"""

from datetime import date
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.api.deps import CurrentAdmin, get_db
from app.models.comptabilite import DonneesDepenses, DonneesRecettes, Exercice
from app.schemas.comptabilite import (
    ExerciceCreate,
    ExerciceList,
    ExerciceRead,
    ExerciceUpdate,
)
from app.schemas.base import Message

router = APIRouter(prefix="/exercices", tags=["Admin - Exercices"])


@router.get(
    "",
    response_model=list[ExerciceList],
    summary="Liste des exercices",
    description="Retourne la liste de tous les exercices.",
)
async def list_exercices(
    current_user: CurrentAdmin,
    cloture: Optional[bool] = Query(None, description="Filtrer par statut de clôture"),
    limit: int = Query(50, ge=1, le=100, description="Nombre maximum de résultats"),
    db: Session = Depends(get_db),
):
    """
    Get list of all fiscal years.
    """
    query = db.query(Exercice)

    if cloture is not None:
        query = query.filter(Exercice.cloture == cloture)

    exercices = query.order_by(Exercice.annee.desc()).limit(limit).all()

    return [
        ExerciceList(
            id=e.id,
            annee=e.annee,
            libelle=e.libelle,
            cloture=e.cloture,
        )
        for e in exercices
    ]


@router.get(
    "/{exercice_id}",
    response_model=ExerciceRead,
    summary="Détail d'un exercice",
    description="Retourne les détails complets d'un exercice.",
)
async def get_exercice(
    exercice_id: int,
    current_user: CurrentAdmin,
    db: Session = Depends(get_db),
):
    """
    Get a fiscal year by ID.
    """
    exercice = db.query(Exercice).filter(Exercice.id == exercice_id).first()

    if not exercice:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Exercice non trouvé"
        )

    return ExerciceRead(
        id=exercice.id,
        annee=exercice.annee,
        libelle=exercice.libelle,
        date_debut=exercice.date_debut,
        date_fin=exercice.date_fin,
        cloture=exercice.cloture,
        created_at=exercice.created_at,
        updated_at=exercice.updated_at,
    )


@router.post(
    "",
    response_model=ExerciceRead,
    status_code=status.HTTP_201_CREATED,
    summary="Créer un exercice",
    description="Crée un nouvel exercice budgétaire.",
)
async def create_exercice(
    data: ExerciceCreate,
    current_user: CurrentAdmin,
    db: Session = Depends(get_db),
):
    """
    Create a new fiscal year.

    - **annee**: Year (e.g., 2024)
    - **libelle**: Optional label (e.g., "Exercice 2024")
    - **date_debut**: Start date
    - **date_fin**: End date
    - **cloture**: Whether the year is closed (default: false)
    """
    # Check if year already exists
    existing = db.query(Exercice).filter(Exercice.annee == data.annee).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"L'exercice {data.annee} existe déjà",
        )

    exercice = Exercice(
        annee=data.annee,
        libelle=data.libelle or f"Exercice {data.annee}",
        date_debut=data.date_debut,
        date_fin=data.date_fin,
        cloture=data.cloture,
    )
    db.add(exercice)
    db.commit()
    db.refresh(exercice)

    return ExerciceRead(
        id=exercice.id,
        annee=exercice.annee,
        libelle=exercice.libelle,
        date_debut=exercice.date_debut,
        date_fin=exercice.date_fin,
        cloture=exercice.cloture,
        created_at=exercice.created_at,
        updated_at=exercice.updated_at,
    )


@router.put(
    "/{exercice_id}",
    response_model=ExerciceRead,
    summary="Modifier un exercice",
    description="Modifie un exercice budgétaire.",
)
async def update_exercice(
    exercice_id: int,
    data: ExerciceUpdate,
    current_user: CurrentAdmin,
    db: Session = Depends(get_db),
):
    """
    Update a fiscal year.
    """
    exercice = db.query(Exercice).filter(Exercice.id == exercice_id).first()

    if not exercice:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Exercice non trouvé"
        )

    # Cannot modify closed exercice (except to reopen)
    if exercice.cloture and data.cloture is not False:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Impossible de modifier un exercice clôturé",
        )

    # Update fields
    update_data = data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(exercice, field, value)

    db.commit()
    db.refresh(exercice)

    return ExerciceRead(
        id=exercice.id,
        annee=exercice.annee,
        libelle=exercice.libelle,
        date_debut=exercice.date_debut,
        date_fin=exercice.date_fin,
        cloture=exercice.cloture,
        created_at=exercice.created_at,
        updated_at=exercice.updated_at,
    )


@router.put(
    "/{exercice_id}/cloturer",
    response_model=ExerciceRead,
    summary="Clôturer un exercice",
    description="Clôture un exercice budgétaire (irréversible).",
)
async def close_exercice(
    exercice_id: int,
    current_user: CurrentAdmin,
    force: bool = Query(
        False, description="Forcer la clôture même avec des données non validées"
    ),
    db: Session = Depends(get_db),
):
    """
    Close a fiscal year.

    Once closed, no modifications can be made to the data.
    """
    exercice = db.query(Exercice).filter(Exercice.id == exercice_id).first()

    if not exercice:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Exercice non trouvé"
        )

    if exercice.cloture:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="L'exercice est déjà clôturé",
        )

    # Check for unvalidated data
    if not force:
        unvalidated_recettes = (
            db.query(DonneesRecettes)
            .filter(
                DonneesRecettes.exercice_id == exercice_id,
                DonneesRecettes.valide == False,
            )
            .count()
        )

        unvalidated_depenses = (
            db.query(DonneesDepenses)
            .filter(
                DonneesDepenses.exercice_id == exercice_id,
                DonneesDepenses.valide == False,
            )
            .count()
        )

        if unvalidated_recettes > 0 or unvalidated_depenses > 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Impossible de clôturer : {unvalidated_recettes} recettes et {unvalidated_depenses} dépenses non validées. Utilisez force=true pour forcer.",
            )

    exercice.cloture = True
    db.commit()
    db.refresh(exercice)

    return ExerciceRead(
        id=exercice.id,
        annee=exercice.annee,
        libelle=exercice.libelle,
        date_debut=exercice.date_debut,
        date_fin=exercice.date_fin,
        cloture=exercice.cloture,
        created_at=exercice.created_at,
        updated_at=exercice.updated_at,
    )


@router.put(
    "/{exercice_id}/rouvrir",
    response_model=ExerciceRead,
    summary="Rouvrir un exercice",
    description="Rouvre un exercice clôturé (admin uniquement).",
)
async def reopen_exercice(
    exercice_id: int,
    current_user: CurrentAdmin,
    db: Session = Depends(get_db),
):
    """
    Reopen a closed fiscal year.

    This allows modifications to the data again.
    Use with caution.
    """
    exercice = db.query(Exercice).filter(Exercice.id == exercice_id).first()

    if not exercice:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Exercice non trouvé"
        )

    if not exercice.cloture:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="L'exercice n'est pas clôturé",
        )

    exercice.cloture = False
    db.commit()
    db.refresh(exercice)

    return ExerciceRead(
        id=exercice.id,
        annee=exercice.annee,
        libelle=exercice.libelle,
        date_debut=exercice.date_debut,
        date_fin=exercice.date_fin,
        cloture=exercice.cloture,
        created_at=exercice.created_at,
        updated_at=exercice.updated_at,
    )


@router.delete(
    "/{exercice_id}",
    response_model=Message,
    summary="Supprimer un exercice",
    description="Supprime un exercice (uniquement si vide).",
)
async def delete_exercice(
    exercice_id: int,
    current_user: CurrentAdmin,
    db: Session = Depends(get_db),
):
    """
    Delete a fiscal year.

    Only possible if no data is associated with it.
    """
    exercice = db.query(Exercice).filter(Exercice.id == exercice_id).first()

    if not exercice:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Exercice non trouvé"
        )

    # Check for associated data
    recettes_count = (
        db.query(DonneesRecettes)
        .filter(DonneesRecettes.exercice_id == exercice_id)
        .count()
    )

    depenses_count = (
        db.query(DonneesDepenses)
        .filter(DonneesDepenses.exercice_id == exercice_id)
        .count()
    )

    if recettes_count > 0 or depenses_count > 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Impossible de supprimer : {recettes_count} recettes et {depenses_count} dépenses associées",
        )

    db.delete(exercice)
    db.commit()

    return Message(message=f"Exercice {exercice.annee} supprimé")


@router.get(
    "/{exercice_id}/statistiques",
    response_model=dict,
    summary="Statistiques d'un exercice",
    description="Retourne les statistiques d'un exercice.",
)
async def get_exercice_stats(
    exercice_id: int,
    current_user: CurrentAdmin,
    db: Session = Depends(get_db),
):
    """
    Get statistics for a fiscal year.
    """
    exercice = db.query(Exercice).filter(Exercice.id == exercice_id).first()

    if not exercice:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Exercice non trouvé"
        )

    # Count data
    recettes_total = (
        db.query(DonneesRecettes)
        .filter(DonneesRecettes.exercice_id == exercice_id)
        .count()
    )

    recettes_validees = (
        db.query(DonneesRecettes)
        .filter(
            DonneesRecettes.exercice_id == exercice_id,
            DonneesRecettes.valide == True,
        )
        .count()
    )

    depenses_total = (
        db.query(DonneesDepenses)
        .filter(DonneesDepenses.exercice_id == exercice_id)
        .count()
    )

    depenses_validees = (
        db.query(DonneesDepenses)
        .filter(
            DonneesDepenses.exercice_id == exercice_id,
            DonneesDepenses.valide == True,
        )
        .count()
    )

    # Count communes
    communes_recettes = (
        db.query(DonneesRecettes.commune_id)
        .filter(DonneesRecettes.exercice_id == exercice_id)
        .distinct()
        .count()
    )

    communes_depenses = (
        db.query(DonneesDepenses.commune_id)
        .filter(DonneesDepenses.exercice_id == exercice_id)
        .distinct()
        .count()
    )

    return {
        "exercice_id": exercice_id,
        "annee": exercice.annee,
        "cloture": exercice.cloture,
        "recettes": {
            "total": recettes_total,
            "validees": recettes_validees,
            "non_validees": recettes_total - recettes_validees,
            "taux_validation": (
                round(recettes_validees / recettes_total * 100, 1)
                if recettes_total > 0
                else 0
            ),
        },
        "depenses": {
            "total": depenses_total,
            "validees": depenses_validees,
            "non_validees": depenses_total - depenses_validees,
            "taux_validation": (
                round(depenses_validees / depenses_total * 100, 1)
                if depenses_total > 0
                else 0
            ),
        },
        "communes_avec_recettes": communes_recettes,
        "communes_avec_depenses": communes_depenses,
    }
