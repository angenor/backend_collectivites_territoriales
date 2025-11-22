"""
Service pour l'authentification et gestion des utilisateurs
"""

from sqlalchemy.orm import Session
from typing import Optional
from uuid import UUID
from datetime import datetime

from app.models.utilisateurs import Utilisateur, Role
from app.schemas.utilisateurs import UtilisateurCreate
from app.core.security import get_password_hash, verify_password, create_access_token


class AuthService:
    """Service pour l'authentification"""

    @staticmethod
    def authenticate_user(db: Session, username: str, password: str) -> Optional[Utilisateur]:
        """Authentifie un utilisateur"""
        utilisateur = (
            db.query(Utilisateur)
            .filter(Utilisateur.username == username, Utilisateur.actif == True)
            .first()
        )

        if not utilisateur:
            return None

        if not verify_password(password, utilisateur.password_hash):
            return None

        # Met à jour le dernier login
        utilisateur.dernier_login = datetime.utcnow()
        db.commit()

        return utilisateur

    @staticmethod
    def create_user(db: Session, user_data: UtilisateurCreate) -> Utilisateur:
        """Crée un nouvel utilisateur"""
        # Vérifier si l'email ou username existe déjà
        existing = (
            db.query(Utilisateur)
            .filter(
                (Utilisateur.email == user_data.email) |
                (Utilisateur.username == user_data.username)
            )
            .first()
        )

        if existing:
            raise ValueError("Email ou username déjà utilisé")

        # Hash du mot de passe
        password_hash = get_password_hash(user_data.password)

        # Créer l'utilisateur
        utilisateur = Utilisateur(
            **user_data.model_dump(exclude={"password"}),
            password_hash=password_hash
        )

        db.add(utilisateur)
        db.commit()
        db.refresh(utilisateur)

        return utilisateur

    @staticmethod
    def get_current_user(db: Session, user_id: UUID) -> Optional[Utilisateur]:
        """Récupère l'utilisateur courant"""
        return (
            db.query(Utilisateur)
            .filter(Utilisateur.id == user_id, Utilisateur.actif == True)
            .first()
        )

    @staticmethod
    def create_access_token_for_user(utilisateur: Utilisateur) -> str:
        """Crée un token d'accès pour un utilisateur"""
        return create_access_token(subject=str(utilisateur.id))
