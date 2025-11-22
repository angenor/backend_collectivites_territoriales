"""
Schémas Pydantic pour les utilisateurs et authentification
"""

from pydantic import BaseModel, EmailStr, Field
from typing import Optional, Dict, Any
from uuid import UUID
from datetime import datetime

from app.schemas.common import TimestampSchema


# Rôles
class RoleBase(BaseModel):
    code: str = Field(..., max_length=50)
    nom: str = Field(..., max_length=255)
    description: Optional[str] = None
    permissions: Optional[Dict[str, Any]] = None
    actif: bool = True


class RoleCreate(RoleBase):
    pass


class Role(RoleBase, TimestampSchema):
    id: UUID
    model_config = {"from_attributes": True}


# Utilisateurs
class UtilisateurBase(BaseModel):
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=100)
    nom: str = Field(..., max_length=255)
    prenom: Optional[str] = Field(None, max_length=255)
    role_id: UUID
    commune_id: Optional[UUID] = None
    telephone: Optional[str] = Field(None, max_length=50)
    actif: bool = True


class UtilisateurCreate(UtilisateurBase):
    password: str = Field(..., min_length=8)


class UtilisateurUpdate(BaseModel):
    email: Optional[EmailStr] = None
    nom: Optional[str] = Field(None, max_length=255)
    prenom: Optional[str] = Field(None, max_length=255)
    telephone: Optional[str] = Field(None, max_length=50)
    actif: Optional[bool] = None


class Utilisateur(UtilisateurBase, TimestampSchema):
    id: UUID
    email_verifie: bool = False
    dernier_login: Optional[datetime] = None

    model_config = {"from_attributes": True}


class UtilisateurDetail(Utilisateur):
    """Utilisateur avec rôle"""
    role: Role


# Authentification
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    user_id: Optional[UUID] = None


class LoginRequest(BaseModel):
    username: str
    password: str
