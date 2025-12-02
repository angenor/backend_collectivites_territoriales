"""
Admin Newsletter API endpoints.
Manage newsletter subscribers.
"""

from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import EmailStr
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.api.deps import CurrentAdmin, get_db
from app.models.annexes import NewsletterAbonne
from app.schemas.base import Message
from app.schemas.documents import NewsletterAbonneRead

router = APIRouter(prefix="/newsletter", tags=["Admin - Newsletter"])


@router.get(
    "",
    response_model=list[NewsletterAbonneRead],
    summary="Liste des abonnés",
    description="Liste tous les abonnés à la newsletter avec filtres.",
)
async def list_subscribers(
    actif: Optional[bool] = Query(None, description="Filtrer par statut actif"),
    search: Optional[str] = Query(None, min_length=2, max_length=100, description="Rechercher par email ou nom"),
    limit: int = Query(50, ge=1, le=500),
    offset: int = Query(0, ge=0),
    current_user: CurrentAdmin = None,
    db: Session = Depends(get_db),
):
    """
    List all newsletter subscribers with optional filters.
    """
    query = db.query(NewsletterAbonne)

    if actif is not None:
        query = query.filter(NewsletterAbonne.actif == actif)

    if search:
        search_term = f"%{search}%"
        query = query.filter(
            (NewsletterAbonne.email.ilike(search_term)) |
            (NewsletterAbonne.nom.ilike(search_term))
        )

    subscribers = query.order_by(NewsletterAbonne.date_inscription.desc()).offset(offset).limit(limit).all()

    return subscribers


@router.get(
    "/count",
    response_model=dict,
    summary="Statistiques des abonnés",
    description="Retourne les statistiques des abonnés à la newsletter.",
)
async def count_subscribers(
    current_user: CurrentAdmin = None,
    db: Session = Depends(get_db),
):
    """
    Get subscriber statistics.
    """
    total = db.query(func.count(NewsletterAbonne.id)).scalar()
    actifs = db.query(func.count(NewsletterAbonne.id)).filter(NewsletterAbonne.actif == True).scalar()
    inactifs = db.query(func.count(NewsletterAbonne.id)).filter(NewsletterAbonne.actif == False).scalar()

    # Get subscriptions by month (last 12 months)
    last_year = datetime.utcnow().replace(year=datetime.utcnow().year - 1)
    monthly = db.query(
        func.date_trunc('month', NewsletterAbonne.date_inscription).label('mois'),
        func.count(NewsletterAbonne.id).label('count')
    ).filter(
        NewsletterAbonne.date_inscription >= last_year
    ).group_by(
        func.date_trunc('month', NewsletterAbonne.date_inscription)
    ).order_by('mois').all()

    return {
        "total": total,
        "actifs": actifs,
        "inactifs": inactifs,
        "evolution_mensuelle": [
            {"mois": m.isoformat() if m else None, "inscriptions": c}
            for m, c in monthly
        ],
    }


@router.get(
    "/{subscriber_id}",
    response_model=NewsletterAbonneRead,
    summary="Détails d'un abonné",
    description="Retourne les détails d'un abonné.",
)
async def get_subscriber(
    subscriber_id: int,
    current_user: CurrentAdmin = None,
    db: Session = Depends(get_db),
):
    """
    Get subscriber details.
    """
    subscriber = db.query(NewsletterAbonne).filter(NewsletterAbonne.id == subscriber_id).first()

    if not subscriber:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Abonné non trouvé.",
        )

    return subscriber


@router.delete(
    "/{subscriber_id}",
    response_model=Message,
    summary="Supprimer un abonné",
    description="Supprime définitivement un abonné.",
)
async def delete_subscriber(
    subscriber_id: int,
    current_user: CurrentAdmin = None,
    db: Session = Depends(get_db),
):
    """
    Delete a subscriber permanently.
    """
    subscriber = db.query(NewsletterAbonne).filter(NewsletterAbonne.id == subscriber_id).first()

    if not subscriber:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Abonné non trouvé.",
        )

    db.delete(subscriber)
    db.commit()

    return Message(message="Abonné supprimé avec succès.")


@router.put(
    "/{subscriber_id}/activate",
    response_model=NewsletterAbonneRead,
    summary="Activer un abonné",
    description="Réactive un abonné désinscrit.",
)
async def activate_subscriber(
    subscriber_id: int,
    current_user: CurrentAdmin = None,
    db: Session = Depends(get_db),
):
    """
    Activate a subscriber.
    """
    subscriber = db.query(NewsletterAbonne).filter(NewsletterAbonne.id == subscriber_id).first()

    if not subscriber:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Abonné non trouvé.",
        )

    subscriber.actif = True
    subscriber.date_desinscription = None
    db.commit()
    db.refresh(subscriber)

    return subscriber


@router.put(
    "/{subscriber_id}/deactivate",
    response_model=NewsletterAbonneRead,
    summary="Désactiver un abonné",
    description="Désactive un abonné.",
)
async def deactivate_subscriber(
    subscriber_id: int,
    current_user: CurrentAdmin = None,
    db: Session = Depends(get_db),
):
    """
    Deactivate a subscriber.
    """
    subscriber = db.query(NewsletterAbonne).filter(NewsletterAbonne.id == subscriber_id).first()

    if not subscriber:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Abonné non trouvé.",
        )

    subscriber.desinscire()
    db.commit()
    db.refresh(subscriber)

    return subscriber


@router.post(
    "/export",
    response_model=dict,
    summary="Exporter les abonnés",
    description="Exporte la liste des abonnés actifs.",
)
async def export_subscribers(
    actif_only: bool = Query(True, description="Exporter uniquement les abonnés actifs"),
    current_user: CurrentAdmin = None,
    db: Session = Depends(get_db),
):
    """
    Export subscriber list as CSV data.
    """
    query = db.query(NewsletterAbonne)

    if actif_only:
        query = query.filter(NewsletterAbonne.actif == True)

    subscribers = query.order_by(NewsletterAbonne.email).all()

    data = [
        {
            "email": s.email,
            "nom": s.nom or "",
            "date_inscription": s.date_inscription.isoformat() if s.date_inscription else "",
            "actif": s.actif,
        }
        for s in subscribers
    ]

    return {
        "count": len(data),
        "data": data,
    }
