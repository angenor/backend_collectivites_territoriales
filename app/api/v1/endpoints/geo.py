"""
Geographic API endpoints.
Provinces, Regions, Communes - Madagascar administrative hierarchy.
"""

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session, joinedload

from app.api.deps import DbSession, get_db
from app.models.geographie import Commune, Province, Region
from app.models.enums import TypeCommune
from sqlalchemy import func

from app.schemas.geographie import (
    CommuneDetail,
    CommuneList,
    CommuneSearch,
    CommuneWithStats,
    HierarchieGeographique,
    ProvinceList,
    ProvinceWithRegions,
    ProvinceWithStats,
    RegionDetail,
    RegionList,
    RegionWithProvince,
    RegionWithStats,
)

router = APIRouter(prefix="/geo", tags=["Géographie"])


# =====================
# Province Endpoints
# =====================

@router.get(
    "/provinces",
    response_model=list[ProvinceWithStats],
    summary="Liste des provinces",
    description="Retourne la liste des 6 provinces de Madagascar avec statistiques."
)
async def list_provinces(
    db: Session = Depends(get_db),
):
    """
    Get list of all provinces with statistics.

    Returns the 6 provinces of Madagascar ordered by name,
    with nb_regions and nb_communes counts.
    """
    provinces = db.query(Province).options(
        joinedload(Province.regions).joinedload(Region.communes)
    ).order_by(Province.nom).all()

    return [
        ProvinceWithStats(
            id=p.id,
            code=p.code,
            nom=p.nom,
            nb_regions=len(p.regions),
            nb_communes=sum(len(r.communes) for r in p.regions)
        )
        for p in provinces
    ]


@router.get(
    "/provinces/{province_id}",
    response_model=ProvinceWithRegions,
    summary="Détail d'une province",
    description="Retourne une province avec ses régions."
)
async def get_province(
    province_id: int,
    db: Session = Depends(get_db),
):
    """
    Get a province by ID with its regions.
    """
    province = db.query(Province).options(
        joinedload(Province.regions)
    ).filter(Province.id == province_id).first()

    if not province:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Province non trouvée"
        )

    return province


# =====================
# Region Endpoints
# =====================

@router.get(
    "/regions",
    response_model=list[RegionWithStats],
    summary="Liste des régions",
    description="Retourne la liste des 22 régions de Madagascar avec statistiques, filtre optionnel par province."
)
async def list_regions(
    province_id: Optional[int] = Query(
        None,
        description="Filtrer par province"
    ),
    db: Session = Depends(get_db),
):
    """
    Get list of all regions with statistics.

    Optionally filter by province_id.
    Returns regions with nb_communes count and province_nom.
    """
    query = db.query(Region).options(
        joinedload(Region.province),
        joinedload(Region.communes)
    )

    if province_id:
        query = query.filter(Region.province_id == province_id)

    regions = query.order_by(Region.nom).all()

    return [
        RegionWithStats(
            id=r.id,
            code=r.code,
            nom=r.nom,
            province_id=r.province_id,
            nb_communes=len(r.communes),
            province_nom=r.province.nom if r.province else None
        )
        for r in regions
    ]


@router.get(
    "/regions/{region_id}",
    response_model=RegionDetail,
    summary="Détail d'une région",
    description="Retourne une région avec sa province et ses communes."
)
async def get_region(
    region_id: int,
    db: Session = Depends(get_db),
):
    """
    Get a region by ID with its province and communes.
    """
    region = db.query(Region).options(
        joinedload(Region.province),
        joinedload(Region.communes)
    ).filter(Region.id == region_id).first()

    if not region:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Région non trouvée"
        )

    return region


# =====================
# Commune Endpoints
# =====================

@router.get(
    "/communes",
    response_model=list[CommuneWithStats],
    summary="Liste des communes",
    description="Retourne la liste des communes avec statistiques, filtres optionnels par région ou type."
)
async def list_communes(
    region_id: Optional[int] = Query(
        None,
        description="Filtrer par région"
    ),
    type_commune: Optional[TypeCommune] = Query(
        None,
        description="Filtrer par type de commune"
    ),
    search: Optional[str] = Query(
        None,
        min_length=2,
        max_length=100,
        description="Recherche par nom (min 2 caractères)"
    ),
    limit: int = Query(
        100,
        ge=1,
        le=500,
        description="Nombre maximum de résultats"
    ),
    offset: int = Query(
        0,
        ge=0,
        description="Nombre de résultats à ignorer"
    ),
    db: Session = Depends(get_db),
):
    """
    Get list of communes with optional filters and stats.

    - **region_id**: Filter by region
    - **type_commune**: Filter by commune type (urbaine, rurale)
    - **search**: Search by name (case-insensitive)
    - **limit**: Max results (default 100, max 500)
    - **offset**: Skip results for pagination
    """
    query = db.query(Commune).options(
        joinedload(Commune.region).joinedload(Region.province)
    )

    if region_id:
        query = query.filter(Commune.region_id == region_id)

    if type_commune:
        query = query.filter(Commune.type_commune == type_commune)

    if search:
        query = query.filter(Commune.nom.ilike(f"%{search}%"))

    communes = query.order_by(Commune.nom).offset(offset).limit(limit).all()

    return [
        CommuneWithStats(
            id=c.id,
            code=c.code,
            nom=c.nom,
            type_commune=c.type_commune,
            region_id=c.region_id,
            region_nom=c.region.nom if c.region else None,
            province_nom=c.region.province.nom if c.region and c.region.province else None,
            nb_comptes_administratifs=0  # TODO: Add actual count when needed
        )
        for c in communes
    ]


@router.get(
    "/communes/search",
    response_model=list[CommuneSearch],
    summary="Recherche de communes",
    description="Recherche avancée de communes avec informations géographiques complètes."
)
async def search_communes(
    q: str = Query(
        ...,
        min_length=2,
        max_length=100,
        description="Terme de recherche"
    ),
    limit: int = Query(
        20,
        ge=1,
        le=100,
        description="Nombre maximum de résultats"
    ),
    db: Session = Depends(get_db),
):
    """
    Search communes with full geographic context.

    Returns communes matching the search term with their region and province names.
    """
    communes = db.query(Commune).options(
        joinedload(Commune.region).joinedload(Region.province)
    ).filter(
        Commune.nom.ilike(f"%{q}%")
    ).order_by(Commune.nom).limit(limit).all()

    return [
        CommuneSearch(
            id=c.id,
            code=c.code,
            nom=c.nom,
            type_commune=c.type_commune,
            region_nom=c.region.nom,
            province_nom=c.region.province.nom
        )
        for c in communes
    ]


@router.get(
    "/communes/{commune_id}",
    response_model=CommuneDetail,
    summary="Détail d'une commune",
    description="Retourne les détails complets d'une commune avec sa région et province."
)
async def get_commune(
    commune_id: int,
    db: Session = Depends(get_db),
):
    """
    Get a commune by ID with full geographic context.
    """
    commune = db.query(Commune).options(
        joinedload(Commune.region).joinedload(Region.province)
    ).filter(Commune.id == commune_id).first()

    if not commune:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Commune non trouvée"
        )

    return commune


# =====================
# Full Hierarchy Endpoint
# =====================

@router.get(
    "/hierarchy",
    response_model=HierarchieGeographique,
    summary="Hiérarchie géographique complète",
    description="Retourne l'arborescence complète: provinces → régions → communes."
)
async def get_full_hierarchy(
    db: Session = Depends(get_db),
):
    """
    Get the complete geographic hierarchy.

    Returns all provinces with their regions.
    Note: Communes are not included for performance reasons.
    Use /regions/{id} to get communes for a specific region.
    """
    provinces = db.query(Province).options(
        joinedload(Province.regions)
    ).order_by(Province.nom).all()

    return HierarchieGeographique(provinces=provinces)
