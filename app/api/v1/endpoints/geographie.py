"""
Endpoints pour la géographie
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import UUID

from app.database import get_db
from app.schemas.geographie import (
    Region, RegionCreate, RegionUpdate,
    Departement, DepartementCreate, DepartementUpdate, DepartementDetail,
    Commune, CommuneCreate, CommuneUpdate, CommuneDetail
)
from app.services.commune_service import CommuneService
from app.api.deps import get_current_active_user
from app.models.geographie import (
    Region as RegionModel,
    Departement as DepartementModel,
    Commune as CommuneModel
)

router = APIRouter()


# ============================================================================
# CRUD RÉGIONS
# ============================================================================

@router.get("/regions", response_model=List[Region], summary="Liste des régions")
def get_all_regions(
    skip: int = 0,
    limit: int = 100,
    actif_only: bool = True,
    db: Session = Depends(get_db)
):
    """
    Récupère toutes les régions de Madagascar

    - **skip**: Nombre d'éléments à ignorer (pagination)
    - **limit**: Nombre maximum d'éléments à retourner
    - **actif_only**: Si True, retourne uniquement les régions actives
    """
    query = db.query(RegionModel)

    if actif_only:
        query = query.filter(RegionModel.actif == True)

    regions = query.order_by(RegionModel.nom).offset(skip).limit(limit).all()
    return regions


@router.get("/regions/{region_id}", response_model=Region, summary="Détails d'une région")
def get_region(
    region_id: UUID,
    db: Session = Depends(get_db)
):
    """Récupère une région spécifique par son ID."""
    region = db.query(RegionModel).filter(RegionModel.id == region_id).first()

    if not region:
        raise HTTPException(
            status_code=404,
            detail=f"Région avec l'ID {region_id} introuvable"
        )

    return region


@router.post("/regions", response_model=Region, status_code=201, summary="Créer une région")
def create_region(
    region_data: RegionCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """Crée une nouvelle région (nécessite d'être authentifié)."""
    # Vérifier que le code n'existe pas déjà
    existing = db.query(RegionModel).filter(RegionModel.code == region_data.code.upper()).first()
    if existing:
        raise HTTPException(
            status_code=400,
            detail=f"Une région avec le code '{region_data.code}' existe déjà"
        )

    # Créer la nouvelle région
    db_region = RegionModel(
        code=region_data.code.upper(),
        nom=region_data.nom,
        description=region_data.description,
        actif=region_data.actif
    )

    db.add(db_region)
    db.commit()
    db.refresh(db_region)

    return db_region


@router.put("/regions/{region_id}", response_model=Region, summary="Modifier une région")
def update_region(
    region_id: UUID,
    region_data: RegionUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """Met à jour une région existante (nécessite d'être authentifié)."""
    region = db.query(RegionModel).filter(RegionModel.id == region_id).first()

    if not region:
        raise HTTPException(
            status_code=404,
            detail=f"Région avec l'ID {region_id} introuvable"
        )

    # Mettre à jour les champs fournis
    update_data = region_data.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(region, field, value)

    db.commit()
    db.refresh(region)

    return region


@router.delete("/regions/{region_id}", summary="Supprimer une région")
def delete_region(
    region_id: UUID,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """Désactive une région (soft delete - nécessite d'être authentifié)."""
    region = db.query(RegionModel).filter(RegionModel.id == region_id).first()

    if not region:
        raise HTTPException(
            status_code=404,
            detail=f"Région avec l'ID {region_id} introuvable"
        )

    # Soft delete : désactiver la région au lieu de la supprimer
    region.actif = False
    db.commit()

    return {"message": f"Région '{region.nom}' désactivée avec succès"}


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


# ============================================================================
# CRUD COMMUNES
# ============================================================================

@router.get("/communes", response_model=List[CommuneDetail], summary="Liste des communes")
def get_all_communes(
    skip: int = 0,
    limit: int = 100,
    actif_only: bool = True,
    region_code: Optional[str] = Query(None),
    departement_id: Optional[UUID] = Query(None),
    search_term: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """
    Récupère la liste de toutes les communes avec filtres optionnels.

    - **skip**: Nombre d'éléments à ignorer (pagination)
    - **limit**: Nombre maximum d'éléments à retourner
    - **actif_only**: Si True, retourne uniquement les communes actives
    - **region_code**: Filtrer par code de région
    - **departement_id**: Filtrer par ID de département
    - **search_term**: Recherche dans le nom de la commune
    """
    query = db.query(CommuneModel)

    if actif_only:
        query = query.filter(CommuneModel.actif == True)

    if departement_id:
        query = query.filter(CommuneModel.departement_id == departement_id)

    if search_term:
        query = query.filter(CommuneModel.nom.ilike(f"%{search_term}%"))

    communes = query.order_by(CommuneModel.nom).offset(skip).limit(limit).all()
    return communes


@router.get("/communes/{commune_id}", response_model=CommuneDetail, summary="Détails d'une commune")
def get_commune(
    commune_id: UUID,
    db: Session = Depends(get_db)
):
    """Récupère une commune spécifique par son ID avec sa hiérarchie."""
    commune = db.query(CommuneModel).filter(CommuneModel.id == commune_id).first()

    if not commune:
        raise HTTPException(
            status_code=404,
            detail=f"Commune avec l'ID {commune_id} introuvable"
        )

    return commune


@router.post("/communes", response_model=CommuneDetail, status_code=201, summary="Créer une commune")
def create_commune(
    commune_data: CommuneCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """Crée une nouvelle commune (nécessite d'être authentifié)."""
    # Vérifier que le code n'existe pas déjà
    existing = db.query(CommuneModel).filter(CommuneModel.code == commune_data.code.upper()).first()
    if existing:
        raise HTTPException(
            status_code=400,
            detail=f"Une commune avec le code '{commune_data.code}' existe déjà"
        )

    # Vérifier que le département existe
    departement = db.query(DepartementModel).filter(DepartementModel.id == commune_data.departement_id).first()
    if not departement:
        raise HTTPException(
            status_code=404,
            detail="Département introuvable"
        )

    # Vérifier que la région existe
    region = db.query(RegionModel).filter(RegionModel.id == commune_data.region_id).first()
    if not region:
        raise HTTPException(
            status_code=404,
            detail="Région introuvable"
        )

    # Créer la nouvelle commune
    db_commune = CommuneModel(
        code=commune_data.code.upper(),
        nom=commune_data.nom,
        departement_id=commune_data.departement_id,
        region_id=commune_data.region_id,
        population=commune_data.population,
        superficie=commune_data.superficie,
        description=commune_data.description,
        actif=commune_data.actif
    )

    db.add(db_commune)
    db.commit()
    db.refresh(db_commune)

    return db_commune


@router.put("/communes/{commune_id}", response_model=CommuneDetail, summary="Modifier une commune")
def update_commune(
    commune_id: UUID,
    commune_data: CommuneUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """Met à jour une commune existante (nécessite d'être authentifié)."""
    commune = db.query(CommuneModel).filter(CommuneModel.id == commune_id).first()

    if not commune:
        raise HTTPException(
            status_code=404,
            detail=f"Commune avec l'ID {commune_id} introuvable"
        )

    # Mettre à jour les champs fournis
    update_data = commune_data.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(commune, field, value)

    db.commit()
    db.refresh(commune)

    return commune


@router.delete("/communes/{commune_id}", summary="Supprimer une commune")
def delete_commune(
    commune_id: UUID,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """Désactive une commune (soft delete - nécessite d'être authentifié)."""
    commune = db.query(CommuneModel).filter(CommuneModel.id == commune_id).first()

    if not commune:
        raise HTTPException(
            status_code=404,
            detail=f"Commune avec l'ID {commune_id} introuvable"
        )

    # Soft delete : désactiver la commune au lieu de la supprimer
    commune.actif = False
    db.commit()

    return {"message": f"Commune '{commune.nom}' désactivée avec succès"}
