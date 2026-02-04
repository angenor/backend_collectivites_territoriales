"""
Mining revenues API endpoints.
Public access to mining revenue data (ristournes, redevances).
"""

from decimal import Decimal
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import func
from sqlalchemy.orm import Session, joinedload

from app.api.deps import DbSession, get_db
from app.models.comptabilite import CompteAdministratif, Exercice
from app.models.geographie import Commune, Region
from app.models.projets_miniers import ProjetMinier, RevenuMinier
from app.models.enums import TypeRevenuMinier
from app.schemas.projets_miniers import (
    RevenuMinierList,
    RevenuMinierWithDetails,
    StatistiquesRevenusMiniers,
)

router = APIRouter(prefix="/revenus", tags=["Revenus Miniers"])


@router.get(
    "",
    response_model=list[RevenuMinierWithDetails],
    summary="Liste des revenus miniers",
    description="Retourne la liste des revenus miniers avec filtres optionnels."
)
async def list_revenus_miniers(
    commune_id: Optional[int] = Query(
        None,
        description="Filtrer par commune"
    ),
    exercice_annee: Optional[int] = Query(
        None,
        description="Filtrer par année d'exercice"
    ),
    type_revenu: Optional[TypeRevenuMinier] = Query(
        None,
        description="Filtrer par type de revenu"
    ),
    projet_id: Optional[int] = Query(
        None,
        description="Filtrer par projet minier"
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
    Get list of mining revenues with optional filters.

    - **commune_id**: Filter by commune
    - **exercice_annee**: Filter by fiscal year
    - **type_revenu**: Filter by revenue type (ristourne, redevance, etc.)
    - **projet_id**: Filter by mining project
    - **limit**: Max results (default 100, max 500)
    - **offset**: Skip results for pagination
    """
    query = db.query(RevenuMinier).options(
        joinedload(RevenuMinier.commune),
        joinedload(RevenuMinier.exercice),
        joinedload(RevenuMinier.projet),
        joinedload(RevenuMinier.compte),
        joinedload(RevenuMinier.compte_administratif)
    )

    if commune_id:
        query = query.filter(RevenuMinier.commune_id == commune_id)

    if exercice_annee:
        query = query.join(Exercice).filter(Exercice.annee == exercice_annee)

    if type_revenu:
        query = query.filter(RevenuMinier.type_revenu == type_revenu)

    if projet_id:
        query = query.filter(RevenuMinier.projet_id == projet_id)

    revenus = query.order_by(
        RevenuMinier.created_at.desc()
    ).offset(offset).limit(limit).all()

    return [
        RevenuMinierWithDetails(
            id=r.id,
            commune_id=r.commune_id,
            exercice_id=r.exercice_id,
            projet_id=r.projet_id,
            type_revenu=r.type_revenu,
            montant_prevu=r.montant_prevu,
            montant_recu=r.montant_recu,
            date_reception=r.date_reception,
            reference_paiement=r.reference_paiement,
            compte_code=r.compte_code,
            compte_administratif_id=r.compte_administratif_id,
            commentaire=r.commentaire,
            ecart=r.ecart,
            taux_realisation=r.taux_realisation,
            created_at=r.created_at,
            updated_at=r.updated_at,
            commune_nom=r.commune.nom,
            exercice_annee=r.exercice.annee,
            projet_nom=r.projet.nom,
            compte_intitule=r.compte.intitule if r.compte else None,
            compte_administratif_label=f"{r.commune.nom} - {r.exercice.annee}"
        )
        for r in revenus
    ]


@router.get(
    "/statistiques",
    response_model=StatistiquesRevenusMiniers,
    summary="Statistiques des revenus miniers",
    description="Retourne les statistiques agrégées des revenus miniers."
)
async def get_statistiques_revenus(
    commune_id: int = Query(..., description="ID de la commune"),
    exercice_annee: int = Query(..., description="Année de l'exercice"),
    db: Session = Depends(get_db),
):
    """
    Get aggregated mining revenue statistics for a commune/year.
    """
    # Verify commune exists
    commune = db.query(Commune).filter(Commune.id == commune_id).first()
    if not commune:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Commune non trouvée"
        )

    # Verify exercice exists
    exercice = db.query(Exercice).filter(Exercice.annee == exercice_annee).first()
    if not exercice:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Exercice {exercice_annee} non trouvé"
        )

    # Get ristournes totals
    ristournes = db.query(
        func.sum(RevenuMinier.montant_prevu).label("prevu"),
        func.sum(RevenuMinier.montant_recu).label("recu")
    ).filter(
        RevenuMinier.commune_id == commune_id,
        RevenuMinier.exercice_id == exercice.id,
        RevenuMinier.type_revenu == TypeRevenuMinier.RISTOURNE
    ).first()

    # Get redevances totals
    redevances = db.query(
        func.sum(RevenuMinier.montant_prevu).label("prevu"),
        func.sum(RevenuMinier.montant_recu).label("recu")
    ).filter(
        RevenuMinier.commune_id == commune_id,
        RevenuMinier.exercice_id == exercice.id,
        RevenuMinier.type_revenu == TypeRevenuMinier.REDEVANCE
    ).first()

    ristournes_prev = ristournes.prevu or Decimal("0.00")
    ristournes_recu = ristournes.recu or Decimal("0.00")
    redevances_prev = redevances.prevu or Decimal("0.00")
    redevances_recu = redevances.recu or Decimal("0.00")

    total_prevu = ristournes_prev + redevances_prev
    total_recu = ristournes_recu + redevances_recu
    ecart = total_recu - total_prevu
    taux = (total_recu / total_prevu * 100) if total_prevu > 0 else None

    return StatistiquesRevenusMiniers(
        commune_id=commune_id,
        exercice_annee=exercice_annee,
        ristournes_prevues=ristournes_prev,
        ristournes_recues=ristournes_recu,
        redevances_prevues=redevances_prev,
        redevances_recues=redevances_recu,
        total_prevu=total_prevu,
        total_recu=total_recu,
        ecart_total=ecart,
        taux_realisation=taux
    )


@router.get(
    "/statistiques/global",
    response_model=dict,
    summary="Statistiques globales",
    description="Retourne les statistiques globales des revenus miniers pour un exercice."
)
async def get_statistiques_globales(
    exercice_annee: int = Query(..., description="Année de l'exercice"),
    region_id: Optional[int] = Query(
        None,
        description="Filtrer par région"
    ),
    db: Session = Depends(get_db),
):
    """
    Get global mining revenue statistics for a fiscal year.

    Optionally filter by region.
    """
    # Verify exercice exists
    exercice = db.query(Exercice).filter(Exercice.annee == exercice_annee).first()
    if not exercice:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Exercice {exercice_annee} non trouvé"
        )

    query = db.query(
        func.count(RevenuMinier.id).label("nb_revenus"),
        func.count(func.distinct(RevenuMinier.commune_id)).label("nb_communes"),
        func.sum(RevenuMinier.montant_prevu).label("total_prevu"),
        func.sum(RevenuMinier.montant_recu).label("total_recu")
    ).filter(
        RevenuMinier.exercice_id == exercice.id
    )

    if region_id:
        query = query.join(Commune).filter(Commune.region_id == region_id)

    stats = query.first()

    total_prevu = stats.total_prevu or Decimal("0.00")
    total_recu = stats.total_recu or Decimal("0.00")
    taux = (total_recu / total_prevu * 100) if total_prevu > 0 else None

    # Get breakdown by type
    by_type = db.query(
        RevenuMinier.type_revenu,
        func.sum(RevenuMinier.montant_prevu).label("prevu"),
        func.sum(RevenuMinier.montant_recu).label("recu")
    ).filter(
        RevenuMinier.exercice_id == exercice.id
    )

    if region_id:
        by_type = by_type.join(Commune).filter(Commune.region_id == region_id)

    by_type = by_type.group_by(RevenuMinier.type_revenu).all()

    par_type = {
        t.type_revenu.value: {
            "prevu": float(t.prevu or 0),
            "recu": float(t.recu or 0)
        }
        for t in by_type
    }

    return {
        "exercice_annee": exercice_annee,
        "region_id": region_id,
        "nb_revenus": stats.nb_revenus or 0,
        "nb_communes": stats.nb_communes or 0,
        "total_prevu": float(total_prevu),
        "total_recu": float(total_recu),
        "ecart": float(total_recu - total_prevu),
        "taux_realisation": float(taux) if taux else None,
        "par_type": par_type
    }


@router.get(
    "/by-commune/{commune_id}",
    response_model=list[RevenuMinierList],
    summary="Revenus d'une commune",
    description="Retourne tous les revenus miniers d'une commune."
)
async def get_revenus_by_commune(
    commune_id: int,
    exercice_annee: Optional[int] = Query(
        None,
        description="Filtrer par année d'exercice"
    ),
    db: Session = Depends(get_db),
):
    """
    Get all mining revenues for a specific commune.
    """
    commune = db.query(Commune).filter(Commune.id == commune_id).first()
    if not commune:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Commune non trouvée"
        )

    query = db.query(RevenuMinier).filter(
        RevenuMinier.commune_id == commune_id
    )

    if exercice_annee:
        exercice = db.query(Exercice).filter(Exercice.annee == exercice_annee).first()
        if exercice:
            query = query.filter(RevenuMinier.exercice_id == exercice.id)

    revenus = query.order_by(RevenuMinier.date_reception.desc()).all()

    return revenus
