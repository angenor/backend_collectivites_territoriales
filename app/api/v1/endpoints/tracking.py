"""
Public Tracking API endpoints.
Track page visits and document downloads.
"""

from datetime import date, datetime
from typing import Optional

from fastapi import APIRouter, Body, Depends, Header, Query, Request, status
from pydantic import BaseModel, Field
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.models.annexes import StatistiqueVisite
from app.models.documents import Document
from app.schemas.base import Message


class VisitEntry(BaseModel):
    """Single visit entry for batch tracking."""
    page: str = Field(..., max_length=255)
    commune_id: Optional[int] = None


class BatchVisitRequest(BaseModel):
    """Batch visit request."""
    visits: list[VisitEntry] = Field(..., max_length=100)

router = APIRouter(prefix="/tracking", tags=["Tracking"])


def anonymize_ip(ip: str) -> str:
    """Anonymize IP address by removing last octet (IPv4) or last 80 bits (IPv6)."""
    if not ip:
        return ""
    if ":" in ip:  # IPv6
        parts = ip.split(":")
        if len(parts) > 4:
            return ":".join(parts[:4]) + "::0"
        return ip
    else:  # IPv4
        parts = ip.split(".")
        if len(parts) == 4:
            return ".".join(parts[:3]) + ".0"
        return ip


@router.post(
    "/visit",
    response_model=Message,
    status_code=status.HTTP_201_CREATED,
    summary="Enregistrer une visite",
    description="Enregistre une visite de page.",
)
async def track_visit(
    request: Request,
    page: str = Query(..., max_length=255, description="Chemin de la page"),
    commune_id: Optional[int] = Query(None, description="ID de la commune consultée"),
    user_agent: Optional[str] = Header(None),
    db: Session = Depends(get_db),
):
    """
    Track a page visit.

    Creates or increments the visit counter for the page/commune/date combination.
    """
    today = date.today()
    client_ip = request.client.host if request.client else None
    anonymized_ip = anonymize_ip(client_ip) if client_ip else None

    # Check if we already have a record for this page/commune/date
    existing = db.query(StatistiqueVisite).filter(
        StatistiqueVisite.date_visite == today,
        StatistiqueVisite.page == page,
        StatistiqueVisite.commune_id == commune_id,
    ).first()

    if existing:
        existing.nb_visites += 1
        db.commit()
    else:
        visite = StatistiqueVisite(
            date_visite=today,
            page=page,
            commune_id=commune_id,
            nb_visites=1,
            nb_telechargements=0,
            ip_address=anonymized_ip,
            user_agent=user_agent[:500] if user_agent else None,
        )
        db.add(visite)
        db.commit()

    return Message(message="Visite enregistrée")


@router.post(
    "/download/{document_id}",
    response_model=Message,
    summary="Enregistrer un téléchargement",
    description="Enregistre le téléchargement d'un document.",
)
async def track_download(
    request: Request,
    document_id: int,
    user_agent: Optional[str] = Header(None),
    db: Session = Depends(get_db),
):
    """
    Track a document download.

    Increments the download counter on the document and records in statistics.
    """
    # Get the document
    document = db.query(Document).filter(Document.id == document_id).first()

    if not document:
        return Message(message="Document non trouvé")

    # Increment document download counter
    document.nb_telechargements = (document.nb_telechargements or 0) + 1

    # Record in statistics
    today = date.today()
    client_ip = request.client.host if request.client else None
    anonymized_ip = anonymize_ip(client_ip) if client_ip else None

    # Find or create statistics entry for document page
    page = f"/documents/{document_id}"
    existing = db.query(StatistiqueVisite).filter(
        StatistiqueVisite.date_visite == today,
        StatistiqueVisite.page == page,
        StatistiqueVisite.commune_id == document.commune_id,
    ).first()

    if existing:
        existing.nb_telechargements += 1
    else:
        visite = StatistiqueVisite(
            date_visite=today,
            page=page,
            commune_id=document.commune_id,
            nb_visites=0,
            nb_telechargements=1,
            ip_address=anonymized_ip,
            user_agent=user_agent[:500] if user_agent else None,
        )
        db.add(visite)

    db.commit()

    return Message(message="Téléchargement enregistré")


@router.post(
    "/batch",
    response_model=Message,
    summary="Enregistrer plusieurs visites",
    description="Enregistre plusieurs visites en une seule requête.",
)
async def track_batch(
    request: Request,
    batch: BatchVisitRequest = Body(...),
    user_agent: Optional[str] = Header(None),
    db: Session = Depends(get_db),
):
    """
    Track multiple page visits in a single request.

    Useful for client-side analytics batching.
    """
    today = date.today()
    client_ip = request.client.host if request.client else None
    anonymized_ip = anonymize_ip(client_ip) if client_ip else None

    count = 0
    for visit in batch.visits:
        page = visit.page[:255]
        commune_id = visit.commune_id

        if not page:
            continue

        existing = db.query(StatistiqueVisite).filter(
            StatistiqueVisite.date_visite == today,
            StatistiqueVisite.page == page,
            StatistiqueVisite.commune_id == commune_id,
        ).first()

        if existing:
            existing.nb_visites += 1
        else:
            visite = StatistiqueVisite(
                date_visite=today,
                page=page,
                commune_id=commune_id,
                nb_visites=1,
                nb_telechargements=0,
                ip_address=anonymized_ip,
                user_agent=user_agent[:500] if user_agent else None,
            )
            db.add(visite)

        count += 1

    db.commit()

    return Message(message=f"{count} visite(s) enregistrée(s)")
