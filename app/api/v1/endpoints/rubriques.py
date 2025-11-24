"""
Endpoints pour les rubriques budgétaires
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import UUID

from app.database import get_db
from app.schemas.revenus import Rubrique, RubriqueCreate, RubriqueUpdate
from app.api.deps import get_current_active_user
from app.models.revenus import Rubrique as RubriqueModel
from app.models.utilisateurs import Utilisateur

router = APIRouter()


@router.get("/", response_model=List[Rubrique], summary="Liste des rubriques")
def get_all_rubriques(
    skip: int = 0,
    limit: int = 500,
    actif_only: bool = True,
    categorie_id: Optional[UUID] = Query(None),
    niveau: Optional[int] = Query(None),
    db: Session = Depends(get_db)
):
    """
    Récupère la liste de toutes les rubriques budgétaires.

    - **skip**: Nombre d'éléments à ignorer (pagination)
    - **limit**: Nombre maximum d'éléments à retourner
    - **actif_only**: Si True, retourne uniquement les rubriques actives
    - **categorie_id**: Filtrer par catégorie
    - **niveau**: Filtrer par niveau hiérarchique
    """
    query = db.query(RubriqueModel)

    if actif_only:
        query = query.filter(RubriqueModel.actif == True)

    if categorie_id:
        query = query.filter(RubriqueModel.categorie_id == categorie_id)

    if niveau is not None:
        query = query.filter(RubriqueModel.niveau == niveau)

    rubriques = query.order_by(RubriqueModel.ordre, RubriqueModel.code).offset(skip).limit(limit).all()
    return rubriques


@router.get("/{rubrique_id}", response_model=Rubrique, summary="Détails d'une rubrique")
def get_rubrique(
    rubrique_id: UUID,
    db: Session = Depends(get_db)
):
    """Récupère une rubrique spécifique par son ID."""
    rubrique = db.query(RubriqueModel).filter(RubriqueModel.id == rubrique_id).first()

    if not rubrique:
        raise HTTPException(
            status_code=404,
            detail=f"Rubrique avec l'ID {rubrique_id} introuvable"
        )

    return rubrique


@router.post("/", response_model=Rubrique, status_code=201, summary="Créer une rubrique")
def create_rubrique(
    rubrique_data: RubriqueCreate,
    db: Session = Depends(get_db),
    current_user: Utilisateur = Depends(get_current_active_user)
):
    """Crée une nouvelle rubrique budgétaire (nécessite d'être authentifié)."""
    # Vérifier que le code n'existe pas déjà
    existing = db.query(RubriqueModel).filter(RubriqueModel.code == rubrique_data.code.upper()).first()
    if existing:
        raise HTTPException(
            status_code=400,
            detail=f"Une rubrique avec le code '{rubrique_data.code}' existe déjà"
        )

    # Créer la nouvelle rubrique
    db_rubrique = RubriqueModel(
        code=rubrique_data.code.upper(),
        nom=rubrique_data.nom,
        categorie_id=rubrique_data.categorie_id,
        parent_id=rubrique_data.parent_id,
        niveau=rubrique_data.niveau,
        ordre=rubrique_data.ordre,
        type=rubrique_data.type,
        formule=rubrique_data.formule,
        est_calculee=rubrique_data.est_calculee,
        afficher_total=rubrique_data.afficher_total,
        description=rubrique_data.description,
        actif=rubrique_data.actif
    )

    db.add(db_rubrique)
    db.commit()
    db.refresh(db_rubrique)

    return db_rubrique


@router.put("/{rubrique_id}", response_model=Rubrique, summary="Modifier une rubrique")
def update_rubrique(
    rubrique_id: UUID,
    rubrique_data: RubriqueUpdate,
    db: Session = Depends(get_db),
    current_user: Utilisateur = Depends(get_current_active_user)
):
    """Met à jour une rubrique existante (nécessite d'être authentifié)."""
    rubrique = db.query(RubriqueModel).filter(RubriqueModel.id == rubrique_id).first()

    if not rubrique:
        raise HTTPException(
            status_code=404,
            detail=f"Rubrique avec l'ID {rubrique_id} introuvable"
        )

    # Mettre à jour les champs fournis
    update_data = rubrique_data.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(rubrique, field, value)

    db.commit()
    db.refresh(rubrique)

    return rubrique


@router.delete("/{rubrique_id}", summary="Supprimer une rubrique")
def delete_rubrique(
    rubrique_id: UUID,
    db: Session = Depends(get_db),
    current_user: Utilisateur = Depends(get_current_active_user)
):
    """Désactive une rubrique (soft delete - nécessite d'être authentifié)."""
    rubrique = db.query(RubriqueModel).filter(RubriqueModel.id == rubrique_id).first()

    if not rubrique:
        raise HTTPException(
            status_code=404,
            detail=f"Rubrique avec l'ID {rubrique_id} introuvable"
        )

    # Soft delete : désactiver la rubrique au lieu de la supprimer
    rubrique.actif = False
    db.commit()

    return {"message": f"Rubrique '{rubrique.nom}' désactivée avec succès"}
