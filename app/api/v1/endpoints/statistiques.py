"""
Public Statistics API endpoints.
Aggregate statistics for public display.
"""

from datetime import date, timedelta
from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.models.annexes import StatistiqueVisite
from app.models.comptabilite import DonneesDepenses, DonneesRecettes, Exercice
from app.models.documents import Document
from app.models.geographie import Commune, Province, Region
from app.models.projets_miniers import ProjetMinier, RevenuMinier

router = APIRouter(prefix="/statistiques", tags=["Statistiques"])


@router.get(
    "/global",
    response_model=dict,
    summary="Statistiques globales",
    description="Retourne les statistiques globales de la plateforme.",
)
async def global_stats(
    db: Session = Depends(get_db),
):
    """
    Get global platform statistics.
    """
    # Geographic counts
    nb_provinces = db.query(func.count(Province.id)).scalar()
    nb_regions = db.query(func.count(Region.id)).scalar()
    nb_communes = db.query(func.count(Commune.id)).scalar()

    # Fiscal years
    nb_exercices = db.query(func.count(Exercice.id)).scalar()
    exercices_publies = db.query(func.count(Exercice.id)).filter(
        Exercice.cloture == True
    ).scalar()

    # Financial data
    total_recettes = db.query(func.sum(DonneesRecettes.recouvrement)).scalar() or 0
    total_depenses = db.query(func.sum(DonneesDepenses.paiement)).scalar() or 0

    # Mining revenues
    total_revenus_miniers = db.query(func.sum(RevenuMinier.montant_recu)).scalar() or 0
    nb_projets_miniers = db.query(func.count(ProjetMinier.id)).scalar()

    # Documents
    nb_documents_publics = db.query(func.count(Document.id)).filter(
        Document.public == True
    ).scalar()

    return {
        "geographie": {
            "provinces": nb_provinces,
            "regions": nb_regions,
            "communes": nb_communes,
        },
        "exercices": {
            "total": nb_exercices,
            "publies": exercices_publies,
        },
        "finances": {
            "total_recettes": float(total_recettes),
            "total_depenses": float(total_depenses),
            "solde": float(total_recettes - total_depenses),
        },
        "revenus_miniers": {
            "total": float(total_revenus_miniers),
            "nb_projets": nb_projets_miniers,
        },
        "documents": {
            "publics": nb_documents_publics,
        },
    }


@router.get(
    "/exercice/{annee}",
    response_model=dict,
    summary="Statistiques par exercice",
    description="Retourne les statistiques pour un exercice donné.",
)
async def exercice_stats(
    annee: int,
    db: Session = Depends(get_db),
):
    """
    Get statistics for a specific fiscal year.
    """
    exercice = db.query(Exercice).filter(Exercice.annee == annee).first()

    if not exercice:
        return {
            "annee": annee,
            "existe": False,
            "message": "Exercice non trouvé",
        }

    # Get communes with data for this exercise
    communes_avec_recettes = db.query(func.count(func.distinct(DonneesRecettes.commune_id))).filter(
        DonneesRecettes.exercice_id == exercice.id
    ).scalar()

    communes_avec_depenses = db.query(func.count(func.distinct(DonneesDepenses.commune_id))).filter(
        DonneesDepenses.exercice_id == exercice.id
    ).scalar()

    # Totals
    total_recettes = db.query(func.sum(DonneesRecettes.recouvrement)).filter(
        DonneesRecettes.exercice_id == exercice.id
    ).scalar() or 0

    total_depenses = db.query(func.sum(DonneesDepenses.paiement)).filter(
        DonneesDepenses.exercice_id == exercice.id
    ).scalar() or 0

    # Mining revenues for this year
    revenus_miniers = db.query(func.sum(RevenuMinier.montant_recu)).filter(
        RevenuMinier.exercice_id == exercice.id
    ).scalar() or 0

    return {
        "annee": annee,
        "existe": True,
        "publie": exercice.cloture,
        "cloture": exercice.cloture,
        "communes_avec_donnees": {
            "recettes": communes_avec_recettes,
            "depenses": communes_avec_depenses,
        },
        "totaux": {
            "recettes": float(total_recettes),
            "depenses": float(total_depenses),
            "solde": float(total_recettes - total_depenses),
            "revenus_miniers": float(revenus_miniers),
        },
    }


@router.get(
    "/region/{region_id}",
    response_model=dict,
    summary="Statistiques par région",
    description="Retourne les statistiques agrégées pour une région.",
)
async def region_stats(
    region_id: int,
    annee: Optional[int] = Query(None, description="Année d'exercice (optionnel)"),
    db: Session = Depends(get_db),
):
    """
    Get aggregated statistics for a region.
    """
    region = db.query(Region).filter(Region.id == region_id).first()

    if not region:
        return {"region_id": region_id, "existe": False}

    # Get commune IDs in this region
    commune_ids = [c.id for c in region.communes]

    # Base query filters
    recettes_query = db.query(func.sum(DonneesRecettes.recouvrement)).filter(
        DonneesRecettes.commune_id.in_(commune_ids)
    )
    depenses_query = db.query(func.sum(DonneesDepenses.paiement)).filter(
        DonneesDepenses.commune_id.in_(commune_ids)
    )

    if annee:
        exercice = db.query(Exercice).filter(Exercice.annee == annee).first()
        if exercice:
            recettes_query = recettes_query.filter(DonneesRecettes.exercice_id == exercice.id)
            depenses_query = depenses_query.filter(DonneesDepenses.exercice_id == exercice.id)

    total_recettes = recettes_query.scalar() or 0
    total_depenses = depenses_query.scalar() or 0

    return {
        "region_id": region_id,
        "region_nom": region.nom,
        "province_nom": region.province.nom if region.province else None,
        "nb_communes": len(commune_ids),
        "annee": annee,
        "totaux": {
            "recettes": float(total_recettes),
            "depenses": float(total_depenses),
            "solde": float(total_recettes - total_depenses),
        },
    }


@router.get(
    "/evolution",
    response_model=dict,
    summary="Évolution pluriannuelle",
    description="Retourne l'évolution des finances sur plusieurs exercices.",
)
async def evolution_stats(
    commune_id: Optional[int] = Query(None, description="ID de la commune (optionnel)"),
    region_id: Optional[int] = Query(None, description="ID de la région (optionnel)"),
    db: Session = Depends(get_db),
):
    """
    Get multi-year evolution statistics.
    """
    # Get all published exercises
    exercices = db.query(Exercice).filter(
        Exercice.cloture == True
    ).order_by(Exercice.annee).all()

    evolution = []

    for exercice in exercices:
        recettes_query = db.query(func.sum(DonneesRecettes.recouvrement)).filter(
            DonneesRecettes.exercice_id == exercice.id
        )
        depenses_query = db.query(func.sum(DonneesDepenses.paiement)).filter(
            DonneesDepenses.exercice_id == exercice.id
        )

        if commune_id:
            recettes_query = recettes_query.filter(DonneesRecettes.commune_id == commune_id)
            depenses_query = depenses_query.filter(DonneesDepenses.commune_id == commune_id)
        elif region_id:
            region = db.query(Region).filter(Region.id == region_id).first()
            if region:
                commune_ids = [c.id for c in region.communes]
                recettes_query = recettes_query.filter(DonneesRecettes.commune_id.in_(commune_ids))
                depenses_query = depenses_query.filter(DonneesDepenses.commune_id.in_(commune_ids))

        total_recettes = recettes_query.scalar() or 0
        total_depenses = depenses_query.scalar() or 0

        evolution.append({
            "annee": exercice.annee,
            "recettes": float(total_recettes),
            "depenses": float(total_depenses),
            "solde": float(total_recettes - total_depenses),
        })

    return {
        "commune_id": commune_id,
        "region_id": region_id,
        "evolution": evolution,
    }


@router.get(
    "/visites",
    response_model=dict,
    summary="Statistiques de visite publiques",
    description="Retourne un résumé des visites du site (derniers 30 jours).",
)
async def public_visit_stats(
    db: Session = Depends(get_db),
):
    """
    Get public visit statistics summary.
    """
    today = date.today()
    thirty_days_ago = today - timedelta(days=30)

    # Total visits in last 30 days
    total_visites = db.query(func.sum(StatistiqueVisite.nb_visites)).filter(
        StatistiqueVisite.date_visite >= thirty_days_ago
    ).scalar() or 0

    # Total downloads
    total_telechargements = db.query(func.sum(StatistiqueVisite.nb_telechargements)).filter(
        StatistiqueVisite.date_visite >= thirty_days_ago
    ).scalar() or 0

    # Most visited communes (top 5)
    top_communes = db.query(
        Commune.nom,
        func.sum(StatistiqueVisite.nb_visites).label('visites')
    ).join(
        StatistiqueVisite,
        StatistiqueVisite.commune_id == Commune.id
    ).filter(
        StatistiqueVisite.date_visite >= thirty_days_ago
    ).group_by(
        Commune.id, Commune.nom
    ).order_by(
        func.sum(StatistiqueVisite.nb_visites).desc()
    ).limit(5).all()

    return {
        "periode": {
            "debut": thirty_days_ago.isoformat(),
            "fin": today.isoformat(),
        },
        "totaux": {
            "visites": total_visites,
            "telechargements": total_telechargements,
        },
        "top_communes": [
            {"nom": nom, "visites": visites}
            for nom, visites in top_communes
        ],
    }
