"""
Authentication service.
Handles user authentication, registration, and session management.
"""

from datetime import datetime, timezone
from typing import Optional, Tuple

from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.security import (
    create_access_token,
    create_refresh_token,
    get_password_hash,
    get_token_expiry,
    verify_password,
    verify_refresh_token,
)
from app.models.enums import RoleUtilisateur
from app.models.utilisateurs import Session as UserSession
from app.models.utilisateurs import Utilisateur
from app.schemas.auth import Token, UserCreate, UserRegister


class AuthService:
    """Service for authentication operations."""

    def __init__(self, db: Session):
        self.db = db

    def authenticate_user(self, email: str, password: str) -> Optional[Utilisateur]:
        """
        Authenticate a user by email and password.

        Args:
            email: User email
            password: Plain text password

        Returns:
            User object if authentication successful, None otherwise
        """
        user = self.db.query(Utilisateur).filter(
            Utilisateur.email == email
        ).first()

        if not user:
            return None

        if not verify_password(password, user.mot_de_passe_hash):
            return None

        return user

    def create_user(
        self,
        user_data: UserCreate | UserRegister,
        created_by: Optional[Utilisateur] = None
    ) -> Utilisateur:
        """
        Create a new user.

        Args:
            user_data: User registration data
            created_by: Optional admin user creating this account

        Returns:
            Created user object

        Raises:
            ValueError: If email already exists
        """
        # Check if email already exists
        existing = self.db.query(Utilisateur).filter(
            Utilisateur.email == user_data.email
        ).first()

        if existing:
            raise ValueError("Cet email est déjà utilisé")

        # Create user
        user = Utilisateur(
            email=user_data.email,
            mot_de_passe_hash=get_password_hash(user_data.password),
            nom=user_data.nom,
            prenom=user_data.prenom,
            role=user_data.role,
            commune_id=user_data.commune_id,
            actif=True,
            email_verifie=False,
        )

        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)

        return user

    def create_tokens(
        self,
        user: Utilisateur,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None
    ) -> Token:
        """
        Create access and refresh tokens for a user.

        Args:
            user: User object
            ip_address: Client IP address
            user_agent: Client user agent

        Returns:
            Token object with access and refresh tokens
        """
        # Create access token
        access_token = create_access_token(
            subject=user.id,
            email=user.email,
            role=user.role.value,
            commune_id=user.commune_id,
        )

        # Create refresh token
        refresh_token = create_refresh_token(subject=user.id)

        # Get expiry for session storage
        expiry = get_token_expiry(refresh_token)

        # Store session in database
        session = UserSession(
            utilisateur_id=user.id,
            refresh_token=refresh_token,
            expires_at=expiry,
            ip_address=ip_address,
            user_agent=user_agent,
        )
        self.db.add(session)

        # Update last login
        user.derniere_connexion = datetime.now(timezone.utc)
        self.db.commit()

        return Token(
            access_token=access_token,
            token_type="bearer",
            expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            refresh_token=refresh_token,
        )

    def refresh_tokens(
        self,
        refresh_token: str,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None
    ) -> Optional[Token]:
        """
        Refresh access token using refresh token.

        Args:
            refresh_token: Refresh token string
            ip_address: Client IP address
            user_agent: Client user agent

        Returns:
            New Token object or None if invalid
        """
        # Verify refresh token
        payload = verify_refresh_token(refresh_token)
        if not payload:
            return None

        user_id = int(payload.get("sub"))

        # Find session in database
        session = self.db.query(UserSession).filter(
            UserSession.refresh_token == refresh_token,
            UserSession.utilisateur_id == user_id,
        ).first()

        if not session:
            return None

        # Check if expired
        if session.is_expired:
            self.db.delete(session)
            self.db.commit()
            return None

        # Get user
        user = self.db.query(Utilisateur).filter(
            Utilisateur.id == user_id
        ).first()

        if not user or not user.actif:
            return None

        # Delete old session
        self.db.delete(session)
        self.db.commit()

        # Create new tokens
        return self.create_tokens(user, ip_address, user_agent)

    def logout(self, refresh_token: str) -> bool:
        """
        Logout user by invalidating refresh token.

        Args:
            refresh_token: Refresh token to invalidate

        Returns:
            True if logout successful
        """
        session = self.db.query(UserSession).filter(
            UserSession.refresh_token == refresh_token
        ).first()

        if session:
            self.db.delete(session)
            self.db.commit()
            return True

        return False

    def logout_all(self, user_id: int) -> int:
        """
        Logout user from all sessions.

        Args:
            user_id: User ID

        Returns:
            Number of sessions invalidated
        """
        result = self.db.query(UserSession).filter(
            UserSession.utilisateur_id == user_id
        ).delete()
        self.db.commit()
        return result

    def get_user_sessions(self, user_id: int) -> list[UserSession]:
        """
        Get all active sessions for a user.

        Args:
            user_id: User ID

        Returns:
            List of active sessions
        """
        return self.db.query(UserSession).filter(
            UserSession.utilisateur_id == user_id,
            UserSession.expires_at > datetime.now(timezone.utc)
        ).all()

    def update_password(
        self,
        user: Utilisateur,
        current_password: str,
        new_password: str
    ) -> bool:
        """
        Update user password.

        Args:
            user: User object
            current_password: Current password
            new_password: New password

        Returns:
            True if password updated successfully

        Raises:
            ValueError: If current password is incorrect
        """
        if not verify_password(current_password, user.mot_de_passe_hash):
            raise ValueError("Mot de passe actuel incorrect")

        user.mot_de_passe_hash = get_password_hash(new_password)
        self.db.commit()

        # Invalidate all sessions except current
        self.logout_all(user.id)

        return True

    def reset_password(self, email: str, new_password: str) -> bool:
        """
        Reset user password (after token verification).

        Args:
            email: User email
            new_password: New password

        Returns:
            True if password reset successfully
        """
        user = self.db.query(Utilisateur).filter(
            Utilisateur.email == email
        ).first()

        if not user:
            return False

        user.mot_de_passe_hash = get_password_hash(new_password)
        self.db.commit()

        # Invalidate all sessions
        self.logout_all(user.id)

        return True

    def verify_email(self, email: str) -> bool:
        """
        Mark user email as verified.

        Args:
            email: User email

        Returns:
            True if email verified successfully
        """
        user = self.db.query(Utilisateur).filter(
            Utilisateur.email == email
        ).first()

        if not user:
            return False

        user.email_verifie = True
        self.db.commit()

        return True

    def get_user_by_email(self, email: str) -> Optional[Utilisateur]:
        """
        Get user by email.

        Args:
            email: User email

        Returns:
            User object or None
        """
        return self.db.query(Utilisateur).filter(
            Utilisateur.email == email
        ).first()

    def get_user_by_id(self, user_id: int) -> Optional[Utilisateur]:
        """
        Get user by ID.

        Args:
            user_id: User ID

        Returns:
            User object or None
        """
        return self.db.query(Utilisateur).filter(
            Utilisateur.id == user_id
        ).first()


def get_auth_service(db: Session) -> AuthService:
    """Factory function for AuthService."""
    return AuthService(db)
