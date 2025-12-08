"""
Admin API endpoints for plan comptable management.
CRUD operations for budget categories (admin/editor only).
"""

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.api.deps import CurrentEditor, get_db
from app.models.comptabilite import PlanComptable
from app.models.enums import SectionBudgetaire, TypeMouvement
from app.schemas.comptabilite import (
    PlanComptableCreate,
    PlanComptableRead,
    PlanComptableUpdate,
)
from app.schemas.base import Message

router = APIRouter(prefix="/plan-comptable", tags=["Admin - Plan Comptable"])


@router.get(
    "",
    response_model=dict,
    summary="Liste du plan comptable",
    description="Retourne la liste paginée des rubriques du plan comptable.",
)
async def list_plan_comptable(
    current_user: CurrentEditor,
    type_mouvement: Optional[str] = Query(None, description="Filtrer par type (recette/depense)"),
    section: Optional[str] = Query(None, description="Filtrer par section (fonctionnement/investissement)"),
    niveau: Optional[int] = Query(None, ge=1, le=3, description="Filtrer par niveau"),
    actif: Optional[bool] = Query(None, description="Filtrer par statut actif"),
    search: Optional[str] = Query(None, min_length=1, max_length=100, description="Recherche par code/intitulé"),
    page: int = Query(1, ge=1, description="Numéro de page"),
    limit: int = Query(100, ge=1, le=500, description="Nombre de résultats par page"),
    db: Session = Depends(get_db),
):
    """
    Get paginated list of plan comptable entries.
    """
    query = db.query(PlanComptable)

    if type_mouvement:
        try:
            tm = TypeMouvement(type_mouvement)
            query = query.filter(PlanComptable.type_mouvement == tm)
        except ValueError:
            pass

    if section:
        try:
            sec = SectionBudgetaire(section)
            query = query.filter(PlanComptable.section == sec)
        except ValueError:
            pass

    if niveau is not None:
        query = query.filter(PlanComptable.niveau == niveau)

    if actif is not None:
        query = query.filter(PlanComptable.actif == actif)

    if search:
        search_pattern = f"%{search}%"
        query = query.filter(
            (PlanComptable.code.ilike(search_pattern))
            | (PlanComptable.intitule.ilike(search_pattern))
        )

    # Get total count
    total = query.count()

    # Calculate offset from page
    offset = (page - 1) * limit

    # Get paginated results, ordered by type, section, then code
    rubriques = (
        query
        .order_by(
            PlanComptable.type_mouvement,
            PlanComptable.section,
            PlanComptable.ordre_affichage.nullslast(),
            PlanComptable.code
        )
        .offset(offset)
        .limit(limit)
        .all()
    )

    items = []
    for r in rubriques:
        items.append({
            "id": r.id,
            "code": r.code,
            "intitule": r.intitule,
            "niveau": r.niveau,
            "type_mouvement": r.type_mouvement.value if hasattr(r.type_mouvement, 'value') else str(r.type_mouvement),
            "section": r.section.value if hasattr(r.section, 'value') else str(r.section),
            "parent_code": r.parent_code,
            "est_sommable": r.est_sommable,
            "ordre_affichage": r.ordre_affichage,
            "actif": r.actif,
        })

    return {
        "items": items,
        "total": total,
        "page": page,
        "limit": limit,
        "pages": (total + limit - 1) // limit if limit > 0 else 0,
    }


@router.get(
    "/{code}",
    response_model=dict,
    summary="Détail d'une rubrique",
    description="Retourne les détails d'une rubrique du plan comptable.",
)
async def get_rubrique(
    code: str,
    current_user: CurrentEditor,
    db: Session = Depends(get_db),
):
    """
    Get a plan comptable entry by code.
    """
    rubrique = db.query(PlanComptable).filter(PlanComptable.code == code).first()

    if not rubrique:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Rubrique non trouvée"
        )

    return {
        "id": rubrique.id,
        "code": rubrique.code,
        "intitule": rubrique.intitule,
        "niveau": rubrique.niveau,
        "type_mouvement": rubrique.type_mouvement.value if hasattr(rubrique.type_mouvement, 'value') else str(rubrique.type_mouvement),
        "section": rubrique.section.value if hasattr(rubrique.section, 'value') else str(rubrique.section),
        "parent_code": rubrique.parent_code,
        "est_sommable": rubrique.est_sommable,
        "ordre_affichage": rubrique.ordre_affichage,
        "actif": rubrique.actif,
    }


@router.post(
    "",
    response_model=dict,
    status_code=status.HTTP_201_CREATED,
    summary="Créer une rubrique",
    description="Crée une nouvelle rubrique dans le plan comptable.",
)
async def create_rubrique(
    data: PlanComptableCreate,
    current_user: CurrentEditor,
    db: Session = Depends(get_db),
):
    """
    Create a new plan comptable entry.
    """
    # Check if code already exists
    existing = db.query(PlanComptable).filter(PlanComptable.code == data.code).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Le code {data.code} existe déjà"
        )

    # Validate parent_code if provided
    if data.parent_code:
        parent = db.query(PlanComptable).filter(PlanComptable.code == data.parent_code).first()
        if not parent:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"La rubrique parente {data.parent_code} n'existe pas"
            )

    rubrique = PlanComptable(
        code=data.code,
        intitule=data.intitule,
        niveau=data.niveau,
        type_mouvement=data.type_mouvement,
        section=data.section,
        parent_code=data.parent_code,
        est_sommable=data.est_sommable,
        ordre_affichage=data.ordre_affichage,
        actif=data.actif,
    )
    db.add(rubrique)
    db.commit()
    db.refresh(rubrique)

    return {
        "id": rubrique.id,
        "code": rubrique.code,
        "intitule": rubrique.intitule,
        "niveau": rubrique.niveau,
        "type_mouvement": rubrique.type_mouvement.value if hasattr(rubrique.type_mouvement, 'value') else str(rubrique.type_mouvement),
        "section": rubrique.section.value if hasattr(rubrique.section, 'value') else str(rubrique.section),
        "parent_code": rubrique.parent_code,
        "est_sommable": rubrique.est_sommable,
        "ordre_affichage": rubrique.ordre_affichage,
        "actif": rubrique.actif,
    }


@router.put(
    "/{code}",
    response_model=dict,
    summary="Modifier une rubrique",
    description="Modifie une rubrique existante du plan comptable.",
)
async def update_rubrique(
    code: str,
    data: PlanComptableUpdate,
    current_user: CurrentEditor,
    db: Session = Depends(get_db),
):
    """
    Update a plan comptable entry.
    """
    rubrique = db.query(PlanComptable).filter(PlanComptable.code == code).first()

    if not rubrique:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Rubrique non trouvée"
        )

    # Validate parent_code if provided
    if data.parent_code is not None and data.parent_code != rubrique.parent_code:
        if data.parent_code:
            parent = db.query(PlanComptable).filter(PlanComptable.code == data.parent_code).first()
            if not parent:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"La rubrique parente {data.parent_code} n'existe pas"
                )

    # Update fields
    update_data = data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(rubrique, field, value)

    db.commit()
    db.refresh(rubrique)

    return {
        "id": rubrique.id,
        "code": rubrique.code,
        "intitule": rubrique.intitule,
        "niveau": rubrique.niveau,
        "type_mouvement": rubrique.type_mouvement.value if hasattr(rubrique.type_mouvement, 'value') else str(rubrique.type_mouvement),
        "section": rubrique.section.value if hasattr(rubrique.section, 'value') else str(rubrique.section),
        "parent_code": rubrique.parent_code,
        "est_sommable": rubrique.est_sommable,
        "ordre_affichage": rubrique.ordre_affichage,
        "actif": rubrique.actif,
    }


@router.delete(
    "/{code}",
    response_model=Message,
    summary="Supprimer une rubrique",
    description="Supprime une rubrique du plan comptable.",
)
async def delete_rubrique(
    code: str,
    current_user: CurrentEditor,
    db: Session = Depends(get_db),
):
    """
    Delete a plan comptable entry.
    """
    rubrique = db.query(PlanComptable).filter(PlanComptable.code == code).first()

    if not rubrique:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Rubrique non trouvée"
        )

    # Check if this rubrique has children
    children = db.query(PlanComptable).filter(PlanComptable.parent_code == code).count()
    if children > 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Impossible de supprimer : cette rubrique a {children} sous-rubrique(s)"
        )

    db.delete(rubrique)
    db.commit()

    return Message(message="Rubrique supprimée avec succès")
