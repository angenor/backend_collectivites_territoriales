"""
Mining projects API endpoints.
Public access to mining projects and companies data.
"""

from decimal import Decimal
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import func
from sqlalchemy.orm import Session, joinedload

from app.api.deps import DbSession, get_db
from app.models.comptabilite import Exercice
from app.models.geographie import Commune
from app.models.projets_miniers import (
    ProjetCommune,
    ProjetMinier,
    RevenuMinier,
    SocieteMiniere,
)
from app.models.enums import StatutProjetMinier
from app.schemas.projets_miniers import (
    ProjetCommuneRead,
    ProjetMinierList,
    ProjetMinierWithCommunes,
    ProjetMinierWithSociete,
    ResumeProjetMinier,
    SocieteMiniereList,
    SocieteMiniereRead,
    SocieteMiniereWithProjets,
)

router = APIRouter(prefix="/projets", tags=["Projets Miniers"])


# =====================
# Mining Projects Endpoints
# =====================

@router.get(
    "",
    response_model=list[ProjetMinierList],
    summary="Liste des projets miniers",
    description="Retourne la liste des projets miniers avec filtres optionnels."
)
async def list_projets(
    societe_id: Optional[int] = Query(
        None,
        description="Filtrer par société"
    ),
    statut: Optional[StatutProjetMinier] = Query(
        None,
        description="Filtrer par statut"
    ),
    type_minerai: Optional[str] = Query(
        None,
        max_length=100,
        description="Filtrer par type de minerai"
    ),
    search: Optional[str] = Query(
        None,
        min_length=2,
        max_length=100,
        description="Recherche par nom"
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
    Get list of mining projects with optional filters.

    - **societe_id**: Filter by mining company
    - **statut**: Filter by project status (exploration, exploitation, etc.)
    - **type_minerai**: Filter by mineral type
    - **search**: Search by project name
    - **limit**: Max results (default 100, max 500)
    - **offset**: Skip results for pagination
    """
    query = db.query(ProjetMinier)

    if societe_id:
        query = query.filter(ProjetMinier.societe_id == societe_id)

    if statut:
        query = query.filter(ProjetMinier.statut == statut)

    if type_minerai:
        query = query.filter(ProjetMinier.type_minerai.ilike(f"%{type_minerai}%"))

    if search:
        query = query.filter(ProjetMinier.nom.ilike(f"%{search}%"))

    projets = query.order_by(ProjetMinier.nom).offset(offset).limit(limit).all()
    return projets


@router.get(
    "/types-minerai",
    response_model=list[str],
    summary="Types de minerais",
    description="Retourne la liste des types de minerais distincts."
)
async def list_types_minerai(
    db: Session = Depends(get_db),
):
    """
    Get list of distinct mineral types.
    """
    types = db.query(ProjetMinier.type_minerai).filter(
        ProjetMinier.type_minerai.isnot(None)
    ).distinct().order_by(ProjetMinier.type_minerai).all()

    return [t[0] for t in types if t[0]]


@router.get(
    "/{projet_id}",
    response_model=ProjetMinierWithCommunes,
    summary="Détail d'un projet",
    description="Retourne les détails complets d'un projet minier."
)
async def get_projet(
    projet_id: int,
    db: Session = Depends(get_db),
):
    """
    Get a mining project by ID with full details.

    Includes company info and impacted communes.
    """
    projet = db.query(ProjetMinier).options(
        joinedload(ProjetMinier.societe),
        joinedload(ProjetMinier.projets_communes).joinedload(ProjetCommune.commune)
    ).filter(ProjetMinier.id == projet_id).first()

    if not projet:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Projet non trouvé"
        )

    # Build communes list
    communes = [
        ProjetCommuneRead(
            id=pc.id,
            projet_id=pc.projet_id,
            commune_id=pc.commune_id,
            pourcentage_territoire=pc.pourcentage_territoire,
            date_debut=pc.date_debut,
            date_fin=pc.date_fin,
            commune_nom=pc.commune.nom if pc.commune else None,
            commune_code=pc.commune.code if pc.commune else None
        )
        for pc in projet.projets_communes
    ]

    return ProjetMinierWithCommunes(
        id=projet.id,
        nom=projet.nom,
        societe_id=projet.societe_id,
        type_minerai=projet.type_minerai,
        statut=projet.statut,
        date_debut_exploitation=projet.date_debut_exploitation,
        surface_ha=projet.surface_ha,
        description=projet.description,
        created_at=projet.created_at,
        updated_at=projet.updated_at,
        societe=projet.societe,
        communes=communes
    )


@router.get(
    "/{projet_id}/resume",
    response_model=ResumeProjetMinier,
    summary="Résumé d'un projet",
    description="Retourne un résumé du projet minier avec statistiques."
)
async def get_projet_resume(
    projet_id: int,
    exercice_annee: Optional[int] = Query(
        None,
        description="Année pour les revenus"
    ),
    db: Session = Depends(get_db),
):
    """
    Get a summary of a mining project with statistics.
    """
    projet = db.query(ProjetMinier).options(
        joinedload(ProjetMinier.societe),
        joinedload(ProjetMinier.projets_communes)
    ).filter(ProjetMinier.id == projet_id).first()

    if not projet:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Projet non trouvé"
        )

    # Get total revenues for the year
    total_revenus = None
    if exercice_annee:
        exercice = db.query(Exercice).filter(Exercice.annee == exercice_annee).first()
        if exercice:
            total = db.query(func.sum(RevenuMinier.montant_recu)).filter(
                RevenuMinier.projet_id == projet_id,
                RevenuMinier.exercice_id == exercice.id
            ).scalar()
            total_revenus = total or Decimal("0.00")

    return ResumeProjetMinier(
        projet_id=projet.id,
        projet_nom=projet.nom,
        societe_nom=projet.societe.nom,
        type_minerai=projet.type_minerai,
        statut=projet.statut,
        nb_communes_impactees=len(projet.projets_communes),
        surface_totale_ha=projet.surface_ha,
        total_revenus_annee=total_revenus
    )


@router.get(
    "/by-commune/{commune_id}",
    response_model=list[ProjetMinierWithSociete],
    summary="Projets d'une commune",
    description="Retourne les projets miniers impactant une commune."
)
async def get_projets_by_commune(
    commune_id: int,
    db: Session = Depends(get_db),
):
    """
    Get all mining projects affecting a specific commune.
    """
    commune = db.query(Commune).filter(Commune.id == commune_id).first()
    if not commune:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Commune non trouvée"
        )

    projet_ids = db.query(ProjetCommune.projet_id).filter(
        ProjetCommune.commune_id == commune_id
    ).all()

    if not projet_ids:
        return []

    projets = db.query(ProjetMinier).options(
        joinedload(ProjetMinier.societe)
    ).filter(
        ProjetMinier.id.in_([p[0] for p in projet_ids])
    ).order_by(ProjetMinier.nom).all()

    return projets


# =====================
# Mining Companies Endpoints
# =====================

@router.get(
    "/societes",
    response_model=list[SocieteMiniereList],
    summary="Liste des sociétés minières",
    description="Retourne la liste des sociétés minières."
)
async def list_societes(
    actif: Optional[bool] = Query(
        None,
        description="Filtrer par statut actif"
    ),
    search: Optional[str] = Query(
        None,
        min_length=2,
        max_length=100,
        description="Recherche par nom"
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
    Get list of mining companies with optional filters.

    - **actif**: Filter by active status
    - **search**: Search by company name
    - **limit**: Max results (default 100, max 500)
    - **offset**: Skip results for pagination
    """
    query = db.query(SocieteMiniere)

    if actif is not None:
        query = query.filter(SocieteMiniere.actif == actif)

    if search:
        query = query.filter(SocieteMiniere.nom.ilike(f"%{search}%"))

    societes = query.order_by(SocieteMiniere.nom).offset(offset).limit(limit).all()
    return societes


@router.get(
    "/societes/{societe_id}",
    response_model=SocieteMiniereWithProjets,
    summary="Détail d'une société",
    description="Retourne les détails d'une société minière avec ses projets."
)
async def get_societe(
    societe_id: int,
    db: Session = Depends(get_db),
):
    """
    Get a mining company by ID with its projects.
    """
    societe = db.query(SocieteMiniere).options(
        joinedload(SocieteMiniere.projets)
    ).filter(SocieteMiniere.id == societe_id).first()

    if not societe:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Société non trouvée"
        )

    return societe
