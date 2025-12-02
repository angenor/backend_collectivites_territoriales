"""
Public Newsletter API endpoints.
Handle newsletter subscriptions and unsubscriptions.
"""

import secrets
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import EmailStr
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.models.annexes import NewsletterAbonne
from app.schemas.base import Message
from app.schemas.documents import NewsletterAbonneCreate, NewsletterAbonneRead

router = APIRouter(prefix="/newsletter", tags=["Newsletter"])


@router.post(
    "/subscribe",
    response_model=NewsletterAbonneRead,
    status_code=status.HTTP_201_CREATED,
    summary="S'inscrire à la newsletter",
    description="Inscription à la newsletter avec email et nom optionnel.",
)
async def subscribe(
    email: EmailStr = Query(..., description="Adresse email"),
    nom: Optional[str] = Query(None, max_length=100, description="Nom (optionnel)"),
    db: Session = Depends(get_db),
):
    """
    Subscribe to the newsletter.

    If the email already exists but is inactive, it will be reactivated.
    """
    # Check if email already exists
    existing = db.query(NewsletterAbonne).filter(NewsletterAbonne.email == email).first()

    if existing:
        if existing.actif:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cette adresse email est déjà inscrite à la newsletter.",
            )
        # Reactivate
        existing.actif = True
        existing.nom = nom or existing.nom
        existing.date_desinscription = None
        existing.token_desinscription = secrets.token_urlsafe(32)
        db.commit()
        db.refresh(existing)
        return existing

    # Create new subscriber
    abonne = NewsletterAbonne(
        email=email,
        nom=nom,
        actif=True,
        token_desinscription=secrets.token_urlsafe(32),
    )
    db.add(abonne)
    db.commit()
    db.refresh(abonne)

    return abonne


@router.post(
    "/unsubscribe",
    response_model=Message,
    summary="Se désinscrire de la newsletter",
    description="Désinscription de la newsletter via token ou email.",
)
async def unsubscribe(
    token: Optional[str] = Query(None, description="Token de désinscription"),
    email: Optional[EmailStr] = Query(None, description="Adresse email"),
    db: Session = Depends(get_db),
):
    """
    Unsubscribe from the newsletter.

    Either token or email must be provided.
    Token is preferred for security.
    """
    if not token and not email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Veuillez fournir un token ou une adresse email.",
        )

    # Find subscriber
    if token:
        abonne = db.query(NewsletterAbonne).filter(
            NewsletterAbonne.token_desinscription == token
        ).first()
    else:
        abonne = db.query(NewsletterAbonne).filter(
            NewsletterAbonne.email == email
        ).first()

    if not abonne:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Abonné non trouvé.",
        )

    if not abonne.actif:
        return Message(message="Vous êtes déjà désinscrit de la newsletter.")

    # Deactivate
    abonne.desinscire()
    db.commit()

    return Message(message="Vous avez été désinscrit de la newsletter avec succès.")


@router.get(
    "/status",
    response_model=dict,
    summary="Vérifier le statut d'inscription",
    description="Vérifie si une adresse email est inscrite à la newsletter.",
)
async def check_status(
    email: EmailStr = Query(..., description="Adresse email"),
    db: Session = Depends(get_db),
):
    """
    Check newsletter subscription status.
    """
    abonne = db.query(NewsletterAbonne).filter(
        NewsletterAbonne.email == email
    ).first()

    if not abonne:
        return {"subscribed": False, "email": email}

    return {
        "subscribed": abonne.actif,
        "email": email,
        "date_inscription": abonne.date_inscription if abonne.actif else None,
    }
