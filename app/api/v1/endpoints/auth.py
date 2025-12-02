"""
Authentication API endpoints.
Login, registration, token refresh, logout.
"""

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.api.deps import (
    CurrentActiveUser,
    CurrentAdmin,
    DbSession,
    get_db,
)
from app.schemas.auth import (
    PasswordChange,
    PasswordReset,
    PasswordResetConfirm,
    RefreshTokenRequest,
    SessionList,
    Token,
    UserLogin,
    UserLoginResponse,
    UserRead,
    UserRegister,
)
from app.services.auth import AuthService
from app.core.security import (
    generate_password_reset_token,
    verify_password_reset_token,
)

router = APIRouter(prefix="/auth", tags=["Authentification"])


def get_client_info(request: Request) -> tuple[Optional[str], Optional[str]]:
    """Extract client IP and user agent from request."""
    ip_address = request.client.host if request.client else None
    user_agent = request.headers.get("user-agent")
    return ip_address, user_agent


# =====================
# Public Endpoints
# =====================

@router.post(
    "/login",
    response_model=Token,
    summary="Connexion utilisateur",
    description="Authentifie un utilisateur et retourne les tokens JWT."
)
async def login(
    request: Request,
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    """
    OAuth2 compatible login endpoint.

    - **username**: Email de l'utilisateur
    - **password**: Mot de passe

    Returns JWT access and refresh tokens.
    """
    auth_service = AuthService(db)

    user = auth_service.authenticate_user(form_data.username, form_data.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou mot de passe incorrect",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user.actif:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Compte utilisateur désactivé",
        )

    ip_address, user_agent = get_client_info(request)
    return auth_service.create_tokens(user, ip_address, user_agent)


@router.post(
    "/login/json",
    response_model=UserLoginResponse,
    summary="Connexion utilisateur (JSON)",
    description="Authentifie un utilisateur via JSON et retourne les tokens avec les infos utilisateur."
)
async def login_json(
    request: Request,
    credentials: UserLogin,
    db: Session = Depends(get_db),
):
    """
    JSON login endpoint (alternative to OAuth2 form).

    Returns JWT tokens and user information.
    """
    auth_service = AuthService(db)

    user = auth_service.authenticate_user(credentials.email, credentials.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou mot de passe incorrect",
        )

    if not user.actif:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Compte utilisateur désactivé",
        )

    ip_address, user_agent = get_client_info(request)
    token = auth_service.create_tokens(user, ip_address, user_agent)

    return UserLoginResponse(
        token=token,
        user=UserRead(
            id=user.id,
            email=user.email,
            nom=user.nom,
            prenom=user.prenom,
            role=user.role,
            commune_id=user.commune_id,
            actif=user.actif,
            email_verifie=user.email_verifie,
            derniere_connexion=user.derniere_connexion,
            created_at=user.created_at,
            updated_at=user.updated_at,
            nom_complet=user.nom_complet,
            is_admin=user.is_admin,
            is_editor=user.is_editor,
        )
    )


@router.post(
    "/refresh",
    response_model=Token,
    summary="Rafraîchir le token",
    description="Génère de nouveaux tokens à partir du refresh token."
)
async def refresh_token(
    request: Request,
    token_request: RefreshTokenRequest,
    db: Session = Depends(get_db),
):
    """
    Refresh access token using refresh token.

    The old refresh token is invalidated and a new one is issued.
    """
    auth_service = AuthService(db)
    ip_address, user_agent = get_client_info(request)

    new_token = auth_service.refresh_tokens(
        token_request.refresh_token,
        ip_address,
        user_agent
    )

    if not new_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token de rafraîchissement invalide ou expiré",
        )

    return new_token


@router.post(
    "/password-reset",
    summary="Demande de réinitialisation",
    description="Envoie un email de réinitialisation de mot de passe."
)
async def request_password_reset(
    reset_request: PasswordReset,
    db: Session = Depends(get_db),
):
    """
    Request a password reset email.

    Always returns success to prevent email enumeration.
    """
    auth_service = AuthService(db)
    user = auth_service.get_user_by_email(reset_request.email)

    if user:
        # Generate reset token
        token = generate_password_reset_token(user.email)
        # TODO: Send email with reset link
        # In production, send email here
        pass

    # Always return success to prevent email enumeration
    return {"message": "Si cet email existe, un lien de réinitialisation a été envoyé"}


@router.post(
    "/password-reset/confirm",
    summary="Confirmer la réinitialisation",
    description="Réinitialise le mot de passe avec le token."
)
async def confirm_password_reset(
    reset_confirm: PasswordResetConfirm,
    db: Session = Depends(get_db),
):
    """
    Reset password using reset token.
    """
    email = verify_password_reset_token(reset_confirm.token)

    if not email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Token de réinitialisation invalide ou expiré",
        )

    auth_service = AuthService(db)
    success = auth_service.reset_password(email, reset_confirm.new_password)

    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Utilisateur non trouvé",
        )

    return {"message": "Mot de passe réinitialisé avec succès"}


# =====================
# Authenticated Endpoints
# =====================

@router.get(
    "/me",
    response_model=UserRead,
    summary="Profil utilisateur",
    description="Retourne les informations de l'utilisateur connecté."
)
async def get_current_user_info(
    current_user: CurrentActiveUser,
):
    """
    Get current authenticated user's profile.
    """
    return UserRead(
        id=current_user.id,
        email=current_user.email,
        nom=current_user.nom,
        prenom=current_user.prenom,
        role=current_user.role,
        commune_id=current_user.commune_id,
        actif=current_user.actif,
        email_verifie=current_user.email_verifie,
        derniere_connexion=current_user.derniere_connexion,
        created_at=current_user.created_at,
        updated_at=current_user.updated_at,
        nom_complet=current_user.nom_complet,
        is_admin=current_user.is_admin,
        is_editor=current_user.is_editor,
    )


@router.post(
    "/logout",
    summary="Déconnexion",
    description="Invalide le refresh token actuel."
)
async def logout(
    token_request: RefreshTokenRequest,
    current_user: CurrentActiveUser,
    db: Session = Depends(get_db),
):
    """
    Logout current session by invalidating refresh token.
    """
    auth_service = AuthService(db)
    auth_service.logout(token_request.refresh_token)
    return {"message": "Déconnexion réussie"}


@router.post(
    "/logout-all",
    summary="Déconnexion de tous les appareils",
    description="Invalide toutes les sessions de l'utilisateur."
)
async def logout_all(
    current_user: CurrentActiveUser,
    db: Session = Depends(get_db),
):
    """
    Logout from all devices by invalidating all refresh tokens.
    """
    auth_service = AuthService(db)
    count = auth_service.logout_all(current_user.id)
    return {"message": f"{count} session(s) invalidée(s)"}


@router.post(
    "/password",
    summary="Changer le mot de passe",
    description="Change le mot de passe de l'utilisateur connecté."
)
async def change_password(
    password_data: PasswordChange,
    current_user: CurrentActiveUser,
    db: Session = Depends(get_db),
):
    """
    Change current user's password.
    """
    auth_service = AuthService(db)

    try:
        auth_service.update_password(
            current_user,
            password_data.current_password,
            password_data.new_password
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )

    return {"message": "Mot de passe modifié avec succès"}


@router.get(
    "/sessions",
    response_model=list[SessionList],
    summary="Lister les sessions",
    description="Liste toutes les sessions actives de l'utilisateur."
)
async def list_sessions(
    current_user: CurrentActiveUser,
    db: Session = Depends(get_db),
):
    """
    List all active sessions for current user.
    """
    auth_service = AuthService(db)
    sessions = auth_service.get_user_sessions(current_user.id)

    return [
        SessionList(
            id=session.id,
            ip_address=session.ip_address,
            created_at=session.created_at,
            is_current=False,  # Would need current token to determine
        )
        for session in sessions
    ]


# =====================
# Admin Endpoints
# =====================

@router.post(
    "/register",
    response_model=UserRead,
    status_code=status.HTTP_201_CREATED,
    summary="Inscription (Admin)",
    description="Crée un nouveau compte utilisateur. Réservé aux administrateurs."
)
async def register_user(
    user_data: UserRegister,
    current_admin: CurrentAdmin,
    db: Session = Depends(get_db),
):
    """
    Register a new user (admin only).

    Available roles:
    - admin: Full access
    - editeur: Can edit data
    - lecteur: Read-only access
    - commune: Limited to assigned commune
    """
    auth_service = AuthService(db)

    try:
        user = auth_service.create_user(user_data, created_by=current_admin)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )

    return UserRead(
        id=user.id,
        email=user.email,
        nom=user.nom,
        prenom=user.prenom,
        role=user.role,
        commune_id=user.commune_id,
        actif=user.actif,
        email_verifie=user.email_verifie,
        derniere_connexion=user.derniere_connexion,
        created_at=user.created_at,
        updated_at=user.updated_at,
        nom_complet=user.nom_complet,
        is_admin=user.is_admin,
        is_editor=user.is_editor,
    )
