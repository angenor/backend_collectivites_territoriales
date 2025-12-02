"""
API Dependencies module.
Common dependencies for API endpoints including authentication.
"""

from typing import Annotated, Generator, Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.security import verify_access_token
from app.database import SessionLocal
from app.models.utilisateurs import Utilisateur
from app.models.enums import RoleUtilisateur


# OAuth2 scheme for token authentication
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/auth/login",
    auto_error=False
)

# OAuth2 scheme that requires authentication
oauth2_scheme_required = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/auth/login",
    auto_error=True
)


def get_db() -> Generator[Session, None, None]:
    """
    Dependency that provides a database session.
    Yields a session and ensures it's closed after use.

    Usage:
        @router.get("/items")
        def get_items(db: Session = Depends(get_db)):
            return db.query(Item).all()
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Type alias for database dependency
DbSession = Annotated[Session, Depends(get_db)]


def get_current_user(
    db: DbSession,
    token: Annotated[str, Depends(oauth2_scheme_required)]
) -> Utilisateur:
    """
    Get the current authenticated user from JWT token.

    Raises:
        HTTPException 401: If token is invalid or user not found
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Impossible de valider les identifiants",
        headers={"WWW-Authenticate": "Bearer"},
    )

    payload = verify_access_token(token)
    if payload is None:
        raise credentials_exception

    user_id: str = payload.get("sub")
    if user_id is None:
        raise credentials_exception

    user = db.query(Utilisateur).filter(Utilisateur.id == int(user_id)).first()
    if user is None:
        raise credentials_exception

    return user


def get_current_user_optional(
    db: DbSession,
    token: Annotated[Optional[str], Depends(oauth2_scheme)]
) -> Optional[Utilisateur]:
    """
    Get the current user if authenticated, None otherwise.
    Useful for endpoints that work both with and without auth.
    """
    if token is None:
        return None

    payload = verify_access_token(token)
    if payload is None:
        return None

    user_id: str = payload.get("sub")
    if user_id is None:
        return None

    return db.query(Utilisateur).filter(Utilisateur.id == int(user_id)).first()


def get_current_active_user(
    current_user: Annotated[Utilisateur, Depends(get_current_user)]
) -> Utilisateur:
    """
    Get the current authenticated user and verify they are active.

    Raises:
        HTTPException 403: If user is inactive
    """
    if not current_user.actif:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Utilisateur inactif"
        )
    return current_user


def get_current_admin(
    current_user: Annotated[Utilisateur, Depends(get_current_active_user)]
) -> Utilisateur:
    """
    Get the current user and verify they have admin role.

    Raises:
        HTTPException 403: If user is not an admin
    """
    if current_user.role != RoleUtilisateur.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Droits administrateur requis"
        )
    return current_user


def get_current_editor(
    current_user: Annotated[Utilisateur, Depends(get_current_active_user)]
) -> Utilisateur:
    """
    Get the current user and verify they have editor or admin role.

    Raises:
        HTTPException 403: If user is not an editor or admin
    """
    if current_user.role not in (RoleUtilisateur.ADMIN, RoleUtilisateur.EDITEUR):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Droits éditeur requis"
        )
    return current_user


def get_current_commune_user(
    current_user: Annotated[Utilisateur, Depends(get_current_active_user)]
) -> Utilisateur:
    """
    Get the current user and verify they have commune access.
    Allows admin, editor, and commune users.

    Raises:
        HTTPException 403: If user doesn't have commune access
    """
    allowed_roles = (
        RoleUtilisateur.ADMIN,
        RoleUtilisateur.EDITEUR,
        RoleUtilisateur.COMMUNE
    )
    if current_user.role not in allowed_roles:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Accès non autorisé"
        )
    return current_user


# Type aliases for common dependency patterns
CurrentUser = Annotated[Utilisateur, Depends(get_current_user)]
CurrentActiveUser = Annotated[Utilisateur, Depends(get_current_active_user)]
CurrentAdmin = Annotated[Utilisateur, Depends(get_current_admin)]
CurrentEditor = Annotated[Utilisateur, Depends(get_current_editor)]
OptionalUser = Annotated[Optional[Utilisateur], Depends(get_current_user_optional)]
