"""
Endpoints pour la géographie
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.database import get_db
from app.schemas.geographie import Region, Departement, Commune, CommuneDetail
from app.services.commune_service import CommuneService

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
