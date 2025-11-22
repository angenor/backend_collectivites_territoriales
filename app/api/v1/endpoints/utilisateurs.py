"""
Endpoints pour l'authentification et gestion des utilisateurs
"""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.utilisateurs import (
    Token, Utilisateur, UtilisateurCreate, UtilisateurDetail
)
from app.services.auth_service import AuthService
from app.api.deps import get_current_active_user
from app.models.utilisateurs import Utilisateur as UtilisateurModel

router = APIRouter()


@router.post("/login", response_model=Token, summary="Connexion")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """Authentification et génération de token JWT"""
    utilisateur = AuthService.authenticate_user(
        db, form_data.username, form_data.password
    )

    if not utilisateur:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Identifiants incorrects",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = AuthService.create_access_token_for_user(utilisateur)

    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/register", response_model=Utilisateur, status_code=201, summary="Inscription")
def register(user_data: UtilisateurCreate, db: Session = Depends(get_db)):
    """Créer un nouvel utilisateur"""
    try:
        return AuthService.create_user(db, user_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/me", response_model=UtilisateurDetail, summary="Profil utilisateur")
def get_current_user_profile(
    current_user: UtilisateurModel = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Récupère le profil de l'utilisateur connecté"""
    return current_user
