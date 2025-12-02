"""
Pydantic schemas for authentication.
Token, User schemas.
"""

from datetime import datetime
from typing import Optional

from pydantic import EmailStr, Field, field_validator

from app.models.enums import RoleUtilisateur
from app.schemas.base import BaseSchema, TimestampSchema


# =====================
# Token Schemas
# =====================

class Token(BaseSchema):
    """JWT Token response."""
    access_token: str
    token_type: str = "bearer"
    expires_in: int  # seconds
    refresh_token: Optional[str] = None


class TokenPayload(BaseSchema):
    """JWT Token payload."""
    sub: int  # user id
    email: str
    role: RoleUtilisateur
    commune_id: Optional[int] = None
    exp: datetime
    iat: datetime
    jti: Optional[str] = None  # token unique id


class RefreshTokenRequest(BaseSchema):
    """Request to refresh access token."""
    refresh_token: str


# =====================
# Login Schemas
# =====================

class UserLogin(BaseSchema):
    """User login credentials."""
    email: EmailStr
    password: str = Field(..., min_length=6)


class UserLoginResponse(BaseSchema):
    """Login response with token and user info."""
    token: Token
    user: "UserRead"


# =====================
# Registration Schemas
# =====================

class UserRegister(BaseSchema):
    """User registration (admin only)."""
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=100)
    nom: str = Field(..., min_length=1, max_length=100)
    prenom: Optional[str] = Field(None, max_length=100)
    role: RoleUtilisateur = RoleUtilisateur.LECTEUR
    commune_id: Optional[int] = None

    @field_validator("password")
    @classmethod
    def validate_password(cls, v: str) -> str:
        """Validate password strength."""
        if len(v) < 8:
            raise ValueError("Le mot de passe doit contenir au moins 8 caractères")
        if not any(c.isupper() for c in v):
            raise ValueError("Le mot de passe doit contenir au moins une majuscule")
        if not any(c.islower() for c in v):
            raise ValueError("Le mot de passe doit contenir au moins une minuscule")
        if not any(c.isdigit() for c in v):
            raise ValueError("Le mot de passe doit contenir au moins un chiffre")
        return v


# =====================
# User CRUD Schemas
# =====================

class UserBase(BaseSchema):
    """Base user schema."""
    email: EmailStr
    nom: str = Field(..., min_length=1, max_length=100)
    prenom: Optional[str] = Field(None, max_length=100)
    role: RoleUtilisateur = RoleUtilisateur.LECTEUR
    commune_id: Optional[int] = None
    actif: bool = True
    email_verifie: bool = False


class UserCreate(BaseSchema):
    """Schema for creating a user."""
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=100)
    nom: str = Field(..., min_length=1, max_length=100)
    prenom: Optional[str] = Field(None, max_length=100)
    role: RoleUtilisateur = RoleUtilisateur.LECTEUR
    commune_id: Optional[int] = None

    @field_validator("password")
    @classmethod
    def validate_password(cls, v: str) -> str:
        """Validate password strength."""
        if len(v) < 8:
            raise ValueError("Le mot de passe doit contenir au moins 8 caractères")
        return v


class UserUpdate(BaseSchema):
    """Schema for updating a user."""
    email: Optional[EmailStr] = None
    nom: Optional[str] = Field(None, min_length=1, max_length=100)
    prenom: Optional[str] = Field(None, max_length=100)
    role: Optional[RoleUtilisateur] = None
    commune_id: Optional[int] = None
    actif: Optional[bool] = None


class UserRead(UserBase, TimestampSchema):
    """Schema for reading a user."""
    id: int
    derniere_connexion: Optional[datetime] = None
    # Computed fields
    nom_complet: Optional[str] = None
    is_admin: Optional[bool] = None
    is_editor: Optional[bool] = None


class UserList(BaseSchema):
    """Simplified schema for listing users."""
    id: int
    email: str
    nom: str
    prenom: Optional[str] = None
    role: RoleUtilisateur
    actif: bool


class UserWithCommune(UserRead):
    """User with commune info."""
    commune_nom: Optional[str] = None
    commune_code: Optional[str] = None


# =====================
# Password Schemas
# =====================

class PasswordChange(BaseSchema):
    """Schema for changing password."""
    current_password: str
    new_password: str = Field(..., min_length=8, max_length=100)

    @field_validator("new_password")
    @classmethod
    def validate_password(cls, v: str) -> str:
        """Validate password strength."""
        if len(v) < 8:
            raise ValueError("Le mot de passe doit contenir au moins 8 caractères")
        if not any(c.isupper() for c in v):
            raise ValueError("Le mot de passe doit contenir au moins une majuscule")
        if not any(c.islower() for c in v):
            raise ValueError("Le mot de passe doit contenir au moins une minuscule")
        if not any(c.isdigit() for c in v):
            raise ValueError("Le mot de passe doit contenir au moins un chiffre")
        return v


class PasswordReset(BaseSchema):
    """Schema for password reset request."""
    email: EmailStr


class PasswordResetConfirm(BaseSchema):
    """Schema for confirming password reset."""
    token: str
    new_password: str = Field(..., min_length=8, max_length=100)

    @field_validator("new_password")
    @classmethod
    def validate_password(cls, v: str) -> str:
        """Validate password strength."""
        if len(v) < 8:
            raise ValueError("Le mot de passe doit contenir au moins 8 caractères")
        return v


# =====================
# Session Schemas
# =====================

class SessionRead(BaseSchema):
    """Schema for reading a session."""
    id: int
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    created_at: datetime
    expires_at: datetime
    is_expired: bool


class SessionList(BaseSchema):
    """Schema for listing sessions."""
    id: int
    ip_address: Optional[str] = None
    created_at: datetime
    is_current: bool = False


# Update forward references
UserLoginResponse.model_rebuild()
