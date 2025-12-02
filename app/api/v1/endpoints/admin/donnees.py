"""
Admin API endpoints for financial data management.
CRUD operations for recettes and depenses (editor/admin only).
"""

from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session, joinedload

from app.api.deps import CurrentEditor, get_db
from app.models.comptabilite import (
    DonneesDepenses,
    DonneesRecettes,
    Exercice,
    PlanComptable,
)
from app.models.geographie import Commune
from app.schemas.comptabilite import (
    DonneesDepensesCreate,
    DonneesDepensesRead,
    DonneesDepensesUpdate,
    DonneesDepensesValidation,
    DonneesRecettesCreate,
    DonneesRecettesRead,
    DonneesRecettesUpdate,
    DonneesRecettesValidation,
)
from app.schemas.base import Message

router = APIRouter(prefix="/donnees", tags=["Admin - Données Financières"])


def _validate_commune_exercice_compte(
    db: Session, commune_id: int, exercice_id: int, compte_code: str
) -> tuple[Commune, Exercice, PlanComptable]:
    """Validate that commune, exercice and compte exist."""
    commune = db.query(Commune).filter(Commune.id == commune_id).first()
    if not commune:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Commune non trouvée"
        )

    exercice = db.query(Exercice).filter(Exercice.id == exercice_id).first()
    if not exercice:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Exercice non trouvé"
        )

    if exercice.cloture:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Impossible de modifier un exercice clôturé",
        )

    compte = db.query(PlanComptable).filter(PlanComptable.code == compte_code).first()
    if not compte:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Compte {compte_code} non trouvé",
        )

    return commune, exercice, compte


# =====================
# RECETTES ENDPOINTS
# =====================


@router.get(
    "/recettes",
    response_model=list[DonneesRecettesRead],
    summary="Liste des recettes",
    description="Retourne les recettes d'une commune pour un exercice.",
)
async def list_recettes(
    commune_id: int = Query(..., description="ID de la commune"),
    exercice_id: int = Query(..., description="ID de l'exercice"),
    current_user: CurrentEditor = None,
    db: Session = Depends(get_db),
):
    """
    Get all receipts for a commune/exercise.
    """
    recettes = (
        db.query(DonneesRecettes)
        .filter(
            DonneesRecettes.commune_id == commune_id,
            DonneesRecettes.exercice_id == exercice_id,
        )
        .order_by(DonneesRecettes.compte_code)
        .all()
    )

    return [
        DonneesRecettesRead(
            id=r.id,
            commune_id=r.commune_id,
            exercice_id=r.exercice_id,
            compte_code=r.compte_code,
            budget_primitif=r.budget_primitif,
            budget_additionnel=r.budget_additionnel,
            modifications=r.modifications,
            previsions_definitives=r.previsions_definitives or r.previsions_calculees,
            or_admis=r.or_admis,
            recouvrement=r.recouvrement,
            reste_a_recouvrer=r.reste_a_recouvrer,
            commentaire=r.commentaire,
            valide=r.valide,
            valide_par=r.valide_par,
            valide_le=r.valide_le,
            taux_execution=r.taux_execution,
            created_at=r.created_at,
            updated_at=r.updated_at,
        )
        for r in recettes
    ]


@router.post(
    "/recettes",
    response_model=DonneesRecettesRead,
    status_code=status.HTTP_201_CREATED,
    summary="Créer une recette",
    description="Crée une nouvelle ligne de recette.",
)
async def create_recette(
    data: DonneesRecettesCreate,
    current_user: CurrentEditor,
    db: Session = Depends(get_db),
):
    """
    Create a new receipt entry.
    """
    commune, exercice, compte = _validate_commune_exercice_compte(
        db, data.commune_id, data.exercice_id, data.compte_code
    )

    # Check if entry already exists
    existing = (
        db.query(DonneesRecettes)
        .filter(
            DonneesRecettes.commune_id == data.commune_id,
            DonneesRecettes.exercice_id == data.exercice_id,
            DonneesRecettes.compte_code == data.compte_code,
        )
        .first()
    )

    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Une entrée existe déjà pour cette commune/exercice/compte",
        )

    recette = DonneesRecettes(**data.model_dump())
    db.add(recette)
    db.commit()
    db.refresh(recette)

    return DonneesRecettesRead(
        id=recette.id,
        commune_id=recette.commune_id,
        exercice_id=recette.exercice_id,
        compte_code=recette.compte_code,
        budget_primitif=recette.budget_primitif,
        budget_additionnel=recette.budget_additionnel,
        modifications=recette.modifications,
        previsions_definitives=recette.previsions_definitives or recette.previsions_calculees,
        or_admis=recette.or_admis,
        recouvrement=recette.recouvrement,
        reste_a_recouvrer=recette.reste_a_recouvrer,
        commentaire=recette.commentaire,
        valide=recette.valide,
        valide_par=recette.valide_par,
        valide_le=recette.valide_le,
        taux_execution=recette.taux_execution,
        created_at=recette.created_at,
        updated_at=recette.updated_at,
    )


@router.put(
    "/recettes/{recette_id}",
    response_model=DonneesRecettesRead,
    summary="Modifier une recette",
    description="Modifie une ligne de recette existante.",
)
async def update_recette(
    recette_id: int,
    data: DonneesRecettesUpdate,
    current_user: CurrentEditor,
    db: Session = Depends(get_db),
):
    """
    Update a receipt entry.
    """
    recette = db.query(DonneesRecettes).filter(DonneesRecettes.id == recette_id).first()

    if not recette:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Recette non trouvée"
        )

    # Check exercice not closed
    exercice = db.query(Exercice).filter(Exercice.id == recette.exercice_id).first()
    if exercice and exercice.cloture:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Impossible de modifier un exercice clôturé",
        )

    # Update fields
    update_data = data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(recette, field, value)

    db.commit()
    db.refresh(recette)

    return DonneesRecettesRead(
        id=recette.id,
        commune_id=recette.commune_id,
        exercice_id=recette.exercice_id,
        compte_code=recette.compte_code,
        budget_primitif=recette.budget_primitif,
        budget_additionnel=recette.budget_additionnel,
        modifications=recette.modifications,
        previsions_definitives=recette.previsions_definitives or recette.previsions_calculees,
        or_admis=recette.or_admis,
        recouvrement=recette.recouvrement,
        reste_a_recouvrer=recette.reste_a_recouvrer,
        commentaire=recette.commentaire,
        valide=recette.valide,
        valide_par=recette.valide_par,
        valide_le=recette.valide_le,
        taux_execution=recette.taux_execution,
        created_at=recette.created_at,
        updated_at=recette.updated_at,
    )


@router.delete(
    "/recettes/{recette_id}",
    response_model=Message,
    summary="Supprimer une recette",
    description="Supprime une ligne de recette.",
)
async def delete_recette(
    recette_id: int,
    current_user: CurrentEditor,
    db: Session = Depends(get_db),
):
    """
    Delete a receipt entry.
    """
    recette = db.query(DonneesRecettes).filter(DonneesRecettes.id == recette_id).first()

    if not recette:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Recette non trouvée"
        )

    # Check exercice not closed
    exercice = db.query(Exercice).filter(Exercice.id == recette.exercice_id).first()
    if exercice and exercice.cloture:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Impossible de supprimer dans un exercice clôturé",
        )

    db.delete(recette)
    db.commit()

    return Message(message="Recette supprimée")


@router.put(
    "/recettes/{recette_id}/valider",
    response_model=DonneesRecettesRead,
    summary="Valider une recette",
    description="Valide ou invalide une ligne de recette.",
)
async def validate_recette(
    recette_id: int,
    data: DonneesRecettesValidation,
    current_user: CurrentEditor,
    db: Session = Depends(get_db),
):
    """
    Validate or invalidate a receipt entry.
    """
    recette = db.query(DonneesRecettes).filter(DonneesRecettes.id == recette_id).first()

    if not recette:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Recette non trouvée"
        )

    recette.valide = data.valide
    if data.valide:
        recette.valide_par = current_user.id
        recette.valide_le = datetime.now()
    else:
        recette.valide_par = None
        recette.valide_le = None

    if data.commentaire:
        recette.commentaire = data.commentaire

    db.commit()
    db.refresh(recette)

    return DonneesRecettesRead(
        id=recette.id,
        commune_id=recette.commune_id,
        exercice_id=recette.exercice_id,
        compte_code=recette.compte_code,
        budget_primitif=recette.budget_primitif,
        budget_additionnel=recette.budget_additionnel,
        modifications=recette.modifications,
        previsions_definitives=recette.previsions_definitives or recette.previsions_calculees,
        or_admis=recette.or_admis,
        recouvrement=recette.recouvrement,
        reste_a_recouvrer=recette.reste_a_recouvrer,
        commentaire=recette.commentaire,
        valide=recette.valide,
        valide_par=recette.valide_par,
        valide_le=recette.valide_le,
        taux_execution=recette.taux_execution,
        created_at=recette.created_at,
        updated_at=recette.updated_at,
    )


# =====================
# DEPENSES ENDPOINTS
# =====================


@router.get(
    "/depenses",
    response_model=list[DonneesDepensesRead],
    summary="Liste des dépenses",
    description="Retourne les dépenses d'une commune pour un exercice.",
)
async def list_depenses(
    commune_id: int = Query(..., description="ID de la commune"),
    exercice_id: int = Query(..., description="ID de l'exercice"),
    current_user: CurrentEditor = None,
    db: Session = Depends(get_db),
):
    """
    Get all expenses for a commune/exercise.
    """
    depenses = (
        db.query(DonneesDepenses)
        .filter(
            DonneesDepenses.commune_id == commune_id,
            DonneesDepenses.exercice_id == exercice_id,
        )
        .order_by(DonneesDepenses.compte_code)
        .all()
    )

    return [
        DonneesDepensesRead(
            id=d.id,
            commune_id=d.commune_id,
            exercice_id=d.exercice_id,
            compte_code=d.compte_code,
            budget_primitif=d.budget_primitif,
            budget_additionnel=d.budget_additionnel,
            modifications=d.modifications,
            previsions_definitives=d.previsions_definitives or d.previsions_calculees,
            engagement=d.engagement,
            mandat_admis=d.mandat_admis,
            paiement=d.paiement,
            reste_a_payer=d.reste_a_payer,
            programme=d.programme,
            commentaire=d.commentaire,
            valide=d.valide,
            valide_par=d.valide_par,
            valide_le=d.valide_le,
            taux_execution=d.taux_execution,
            created_at=d.created_at,
            updated_at=d.updated_at,
        )
        for d in depenses
    ]


@router.post(
    "/depenses",
    response_model=DonneesDepensesRead,
    status_code=status.HTTP_201_CREATED,
    summary="Créer une dépense",
    description="Crée une nouvelle ligne de dépense.",
)
async def create_depense(
    data: DonneesDepensesCreate,
    current_user: CurrentEditor,
    db: Session = Depends(get_db),
):
    """
    Create a new expense entry.
    """
    commune, exercice, compte = _validate_commune_exercice_compte(
        db, data.commune_id, data.exercice_id, data.compte_code
    )

    # Check if entry already exists
    existing = (
        db.query(DonneesDepenses)
        .filter(
            DonneesDepenses.commune_id == data.commune_id,
            DonneesDepenses.exercice_id == data.exercice_id,
            DonneesDepenses.compte_code == data.compte_code,
        )
        .first()
    )

    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Une entrée existe déjà pour cette commune/exercice/compte",
        )

    depense = DonneesDepenses(**data.model_dump())
    db.add(depense)
    db.commit()
    db.refresh(depense)

    return DonneesDepensesRead(
        id=depense.id,
        commune_id=depense.commune_id,
        exercice_id=depense.exercice_id,
        compte_code=depense.compte_code,
        budget_primitif=depense.budget_primitif,
        budget_additionnel=depense.budget_additionnel,
        modifications=depense.modifications,
        previsions_definitives=depense.previsions_definitives or depense.previsions_calculees,
        engagement=depense.engagement,
        mandat_admis=depense.mandat_admis,
        paiement=depense.paiement,
        reste_a_payer=depense.reste_a_payer,
        programme=depense.programme,
        commentaire=depense.commentaire,
        valide=depense.valide,
        valide_par=depense.valide_par,
        valide_le=depense.valide_le,
        taux_execution=depense.taux_execution,
        created_at=depense.created_at,
        updated_at=depense.updated_at,
    )


@router.put(
    "/depenses/{depense_id}",
    response_model=DonneesDepensesRead,
    summary="Modifier une dépense",
    description="Modifie une ligne de dépense existante.",
)
async def update_depense(
    depense_id: int,
    data: DonneesDepensesUpdate,
    current_user: CurrentEditor,
    db: Session = Depends(get_db),
):
    """
    Update an expense entry.
    """
    depense = db.query(DonneesDepenses).filter(DonneesDepenses.id == depense_id).first()

    if not depense:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Dépense non trouvée"
        )

    # Check exercice not closed
    exercice = db.query(Exercice).filter(Exercice.id == depense.exercice_id).first()
    if exercice and exercice.cloture:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Impossible de modifier un exercice clôturé",
        )

    # Update fields
    update_data = data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(depense, field, value)

    db.commit()
    db.refresh(depense)

    return DonneesDepensesRead(
        id=depense.id,
        commune_id=depense.commune_id,
        exercice_id=depense.exercice_id,
        compte_code=depense.compte_code,
        budget_primitif=depense.budget_primitif,
        budget_additionnel=depense.budget_additionnel,
        modifications=depense.modifications,
        previsions_definitives=depense.previsions_definitives or depense.previsions_calculees,
        engagement=depense.engagement,
        mandat_admis=depense.mandat_admis,
        paiement=depense.paiement,
        reste_a_payer=depense.reste_a_payer,
        programme=depense.programme,
        commentaire=depense.commentaire,
        valide=depense.valide,
        valide_par=depense.valide_par,
        valide_le=depense.valide_le,
        taux_execution=depense.taux_execution,
        created_at=depense.created_at,
        updated_at=depense.updated_at,
    )


@router.delete(
    "/depenses/{depense_id}",
    response_model=Message,
    summary="Supprimer une dépense",
    description="Supprime une ligne de dépense.",
)
async def delete_depense(
    depense_id: int,
    current_user: CurrentEditor,
    db: Session = Depends(get_db),
):
    """
    Delete an expense entry.
    """
    depense = db.query(DonneesDepenses).filter(DonneesDepenses.id == depense_id).first()

    if not depense:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Dépense non trouvée"
        )

    # Check exercice not closed
    exercice = db.query(Exercice).filter(Exercice.id == depense.exercice_id).first()
    if exercice and exercice.cloture:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Impossible de supprimer dans un exercice clôturé",
        )

    db.delete(depense)
    db.commit()

    return Message(message="Dépense supprimée")


@router.put(
    "/depenses/{depense_id}/valider",
    response_model=DonneesDepensesRead,
    summary="Valider une dépense",
    description="Valide ou invalide une ligne de dépense.",
)
async def validate_depense(
    depense_id: int,
    data: DonneesDepensesValidation,
    current_user: CurrentEditor,
    db: Session = Depends(get_db),
):
    """
    Validate or invalidate an expense entry.
    """
    depense = db.query(DonneesDepenses).filter(DonneesDepenses.id == depense_id).first()

    if not depense:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Dépense non trouvée"
        )

    depense.valide = data.valide
    if data.valide:
        depense.valide_par = current_user.id
        depense.valide_le = datetime.now()
    else:
        depense.valide_par = None
        depense.valide_le = None

    if data.commentaire:
        depense.commentaire = data.commentaire

    db.commit()
    db.refresh(depense)

    return DonneesDepensesRead(
        id=depense.id,
        commune_id=depense.commune_id,
        exercice_id=depense.exercice_id,
        compte_code=depense.compte_code,
        budget_primitif=depense.budget_primitif,
        budget_additionnel=depense.budget_additionnel,
        modifications=depense.modifications,
        previsions_definitives=depense.previsions_definitives or depense.previsions_calculees,
        engagement=depense.engagement,
        mandat_admis=depense.mandat_admis,
        paiement=depense.paiement,
        reste_a_payer=depense.reste_a_payer,
        programme=depense.programme,
        commentaire=depense.commentaire,
        valide=depense.valide,
        valide_par=depense.valide_par,
        valide_le=depense.valide_le,
        taux_execution=depense.taux_execution,
        created_at=depense.created_at,
        updated_at=depense.updated_at,
    )
