"""
Fiscal years (Exercices) API endpoints.
Public read access to fiscal year information.
"""

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.api.deps import DbSession, get_db
from app.models.comptabilite import Exercice
from app.schemas.comptabilite import ExerciceList, ExerciceRead

router = APIRouter(prefix="/exercices", tags=["Exercices"])


@router.get(
    "",
    response_model=list[ExerciceList],
    summary="Liste des exercices",
    description="Retourne la liste des exercices budgétaires disponibles."
)
async def list_exercices(
    cloture: Optional[bool] = Query(
        None,
        description="Filtrer par statut de clôture"
    ),
    limit: int = Query(
        50,
        ge=1,
        le=100,
        description="Nombre maximum de résultats"
    ),
    db: Session = Depends(get_db),
):
    """
    Get list of all fiscal years.

    - **cloture**: Filter by closure status (True = closed, False = open)
    - **limit**: Max results (default 50)

    Returns exercices ordered by year descending (most recent first).
    """
    query = db.query(Exercice)

    if cloture is not None:
        query = query.filter(Exercice.cloture == cloture)

    exercices = query.order_by(Exercice.annee.desc()).limit(limit).all()
    return exercices


@router.get(
    "/current",
    response_model=ExerciceRead,
    summary="Exercice en cours",
    description="Retourne l'exercice budgétaire en cours (non clôturé le plus récent)."
)
async def get_current_exercice(
    db: Session = Depends(get_db),
):
    """
    Get the current (most recent non-closed) fiscal year.
    """
    exercice = db.query(Exercice).filter(
        Exercice.cloture == False
    ).order_by(Exercice.annee.desc()).first()

    if not exercice:
        # If no open exercice, return the most recent one
        exercice = db.query(Exercice).order_by(Exercice.annee.desc()).first()

    if not exercice:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Aucun exercice trouvé"
        )

    return exercice


@router.get(
    "/years",
    response_model=list[int],
    summary="Années disponibles",
    description="Retourne la liste des années d'exercice disponibles."
)
async def list_available_years(
    db: Session = Depends(get_db),
):
    """
    Get list of available years.

    Returns just the years as a simple list of integers.
    """
    exercices = db.query(Exercice.annee).order_by(
        Exercice.annee.desc()
    ).all()

    return [e.annee for e in exercices]


@router.get(
    "/{annee}",
    response_model=ExerciceRead,
    summary="Détail d'un exercice",
    description="Retourne les détails d'un exercice budgétaire par année."
)
async def get_exercice(
    annee: int,
    db: Session = Depends(get_db),
):
    """
    Get a fiscal year by year.

    - **annee**: The fiscal year (e.g., 2023, 2024)
    """
    exercice = db.query(Exercice).filter(
        Exercice.annee == annee
    ).first()

    if not exercice:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Exercice {annee} non trouvé"
        )

    return exercice
