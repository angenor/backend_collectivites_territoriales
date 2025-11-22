"""
Dependencies pour l'authentification et base de données
"""

from typing import Generator
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from uuid import UUID

from app.database import get_db
from app.core.security import verify_token
from app.services.auth_service import AuthService
from app.models.utilisateurs import Utilisateur

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


def get_current_user(
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
) -> Utilisateur:
    """
    Récupère l'utilisateur courant à partir du token JWT

    Raises:
        HTTPException: 401 si le token est invalide ou l'utilisateur n'existe pas
    """
    user_id_str = verify_token(token)
    if not user_id_str:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Impossible de valider les identifiants",
            headers={"WWW-Authenticate": "Bearer"},
        )

    try:
        user_id = UUID(user_id_str)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token invalide",
        )

    utilisateur = AuthService.get_current_user(db, user_id)
    if not utilisateur:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Utilisateur non trouvé"
        )

    return utilisateur


def get_current_active_user(
    current_user: Utilisateur = Depends(get_current_user),
) -> Utilisateur:
    """
    Vérifie que l'utilisateur est actif

    Raises:
        HTTPException: 400 si l'utilisateur est inactif
    """
    if not current_user.actif:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Utilisateur inactif"
        )
    return current_user
