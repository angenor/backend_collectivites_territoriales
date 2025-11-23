"""
Endpoints pour la géographie
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import UUID

from app.database import get_db
from app.schemas.geographie import (
    Region,
    Departement, DepartementCreate, DepartementUpdate, DepartementDetail,
    Commune, CommuneDetail
)
from app.services.commune_service import CommuneService
from app.api.deps import get_current_active_user
from app.models.geographie import Departement as DepartementModel

router = APIRouter()


@router.get("/regions", response_model=List[Region], summary="Liste des régions")
def get_regions(db: Session = Depends(get_db)):
    """Récupère toutes les régions de Madagascar"""
    return CommuneService.get_all_regions(db)


@router.get(
    "/regions/{region_code}/departements",
    response_model=List[Departement],
    summary="Départements d'une région"
)
def get_departements_by_region(region_code: str, db: Session = Depends(get_db)):
    """Récupère tous les départements d'une région"""
    departements = CommuneService.get_departements_by_region(db, region_code)
    if not departements:
        raise HTTPException(status_code=404, detail="Région non trouvée ou sans départements")
    return departements


# ============================================================================
# CRUD DÉPARTEMENTS
# ============================================================================

@router.get("/departements", response_model=List[DepartementDetail], summary="Liste des départements")
def get_all_departements(
    skip: int = 0,
    limit: int = 100,
    actif_only: bool = True,
    db: Session = Depends(get_db)
):
    """
    Récupère la liste de tous les départements avec leur région.

    - **skip**: Nombre d'éléments à ignorer (pagination)
    - **limit**: Nombre maximum d'éléments à retourner
    - **actif_only**: Si True, retourne uniquement les départements actifs
    """
    query = db.query(DepartementModel)

    if actif_only:
        query = query.filter(DepartementModel.actif == True)

    departements = query.order_by(DepartementModel.nom).offset(skip).limit(limit).all()
    return departements


@router.get("/departements/{departement_id}", response_model=DepartementDetail, summary="Détails d'un département")
def get_departement(
    departement_id: UUID,
    db: Session = Depends(get_db)
):
    """
    Récupère un département spécifique par son ID avec sa région.

    - **departement_id**: UUID du département
    """
    departement = db.query(DepartementModel).filter(DepartementModel.id == departement_id).first()

    if not departement:
        raise HTTPException(
            status_code=404,
            detail=f"Département avec l'ID {departement_id} introuvable"
        )

    return departement


@router.post("/departements", response_model=DepartementDetail, status_code=201, summary="Créer un département")
def create_departement(
    departement_data: DepartementCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """
    Crée un nouveau département (nécessite d'être authentifié).

    - **departement_data**: Données du département à créer
    """
    # Vérifier que le code n'existe pas déjà
    existing = db.query(DepartementModel).filter(DepartementModel.code == departement_data.code.upper()).first()
    if existing:
        raise HTTPException(
            status_code=400,
            detail=f"Un département avec le code '{departement_data.code}' existe déjà"
        )

    # Créer le nouveau département
    db_departement = DepartementModel(
        code=departement_data.code.upper(),
        nom=departement_data.nom,
        region_id=departement_data.region_id,
        description=departement_data.description,
        actif=departement_data.actif
    )

    db.add(db_departement)
    db.commit()
    db.refresh(db_departement)

    return db_departement


@router.put("/departements/{departement_id}", response_model=DepartementDetail, summary="Modifier un département")
def update_departement(
    departement_id: UUID,
    departement_data: DepartementUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """
    Met à jour un département existant (nécessite d'être authentifié).

    - **departement_id**: UUID du département à modifier
    - **departement_data**: Nouvelles données du département
    """
    departement = db.query(DepartementModel).filter(DepartementModel.id == departement_id).first()

    if not departement:
        raise HTTPException(
            status_code=404,
            detail=f"Département avec l'ID {departement_id} introuvable"
        )

    # Mettre à jour les champs fournis
    update_data = departement_data.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(departement, field, value)

    db.commit()
    db.refresh(departement)

    return departement


@router.delete("/departements/{departement_id}", summary="Supprimer un département")
def delete_departement(
    departement_id: UUID,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """
    Désactive un département (soft delete - nécessite d'être authentifié).

    - **departement_id**: UUID du département à désactiver
    """
    departement = db.query(DepartementModel).filter(DepartementModel.id == departement_id).first()

    if not departement:
        raise HTTPException(
            status_code=404,
            detail=f"Département avec l'ID {departement_id} introuvable"
        )

    # Soft delete : désactiver le département au lieu de le supprimer
    departement.actif = False
    db.commit()

    return {"message": f"Département '{departement.nom}' désactivé avec succès"}


@router.get(
    "/departements/{departement_code}/communes",
    response_model=List[Commune],
    summary="Communes d'un département"
)
def get_communes_by_departement(departement_code: str, db: Session = Depends(get_db)):
    """Récupère toutes les communes d'un département"""
    communes = CommuneService.get_communes_by_departement(db, departement_code)
    if not communes:
        raise HTTPException(status_code=404, detail="Département non trouvé ou sans communes")
    return communes


@router.get(
    "/communes/{commune_code}",
    response_model=CommuneDetail,
    summary="Détails d'une commune"
)
def get_commune_detail(commune_code: str, db: Session = Depends(get_db)):
    """Récupère les détails d'une commune avec sa hiérarchie"""
    commune = CommuneService.get_commune_with_hierarchy(db, commune_code)
    if not commune:
        raise HTTPException(status_code=404, detail="Commune non trouvée")
    return commune


@router.get("/communes", response_model=List[Commune], summary="Recherche de communes")
def search_communes(
    region_code: Optional[str] = Query(None),
    search_term: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """Recherche de communes avec filtres"""
    return CommuneService.search_communes(db, region_code, search_term)
