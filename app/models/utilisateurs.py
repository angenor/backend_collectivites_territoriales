"""
User and authentication models.
Utilisateur and Session tables.
"""

from datetime import datetime
from typing import TYPE_CHECKING, List, Optional

from sqlalchemy import Boolean, DateTime, Enum, ForeignKey, Index, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from app.models.base import TimestampMixin
from app.models.enums import RoleUtilisateur

if TYPE_CHECKING:
    from app.models.geographie import Commune
    from app.models.comptabilite import DonneesRecettes, DonneesDepenses
    from app.models.documents import Document
    from app.models.cms import PageCompteAdministratif
    from app.models.annexes import AuditLog


class Utilisateur(Base, TimestampMixin):
    """
    Utilisateurs de la plateforme.
    Supporte différents rôles: admin, editeur, lecteur, commune.
    """
    __tablename__ = "utilisateurs"
    __table_args__ = (
        Index("idx_utilisateurs_email", "email"),
        Index("idx_utilisateurs_commune", "commune_id"),
        Index("idx_utilisateurs_role", "role"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    mot_de_passe_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    nom: Mapped[str] = mapped_column(String(100), nullable=False)
    prenom: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    role: Mapped[RoleUtilisateur] = mapped_column(
        Enum(RoleUtilisateur, name="role_utilisateur", create_type=False),
        nullable=False,
        default=RoleUtilisateur.LECTEUR
    )
    commune_id: Mapped[Optional[int]] = mapped_column(
        Integer,
        ForeignKey("communes.id", ondelete="SET NULL"),
        nullable=True
    )
    actif: Mapped[bool] = mapped_column(Boolean, default=True)
    email_verifie: Mapped[bool] = mapped_column(Boolean, default=False)
    derniere_connexion: Mapped[Optional[datetime]] = mapped_column(
        DateTime,
        nullable=True
    )

    # Relations
    commune: Mapped[Optional["Commune"]] = relationship(
        "Commune",
        back_populates="utilisateurs"
    )
    sessions: Mapped[List["Session"]] = relationship(
        "Session",
        back_populates="utilisateur",
        cascade="all, delete-orphan"
    )

    # Relations vers tables avec valide_par
    recettes_validees: Mapped[List["DonneesRecettes"]] = relationship(
        "DonneesRecettes",
        back_populates="validateur",
        foreign_keys="DonneesRecettes.valide_par"
    )
    depenses_validees: Mapped[List["DonneesDepenses"]] = relationship(
        "DonneesDepenses",
        back_populates="validateur",
        foreign_keys="DonneesDepenses.valide_par"
    )

    # Relations vers documents uploadés
    documents_uploades: Mapped[List["Document"]] = relationship(
        "Document",
        back_populates="uploadeur",
        foreign_keys="Document.uploade_par"
    )

    # Relations vers pages CMS
    pages_creees: Mapped[List["PageCompteAdministratif"]] = relationship(
        "PageCompteAdministratif",
        back_populates="createur",
        foreign_keys="PageCompteAdministratif.cree_par"
    )
    pages_modifiees: Mapped[List["PageCompteAdministratif"]] = relationship(
        "PageCompteAdministratif",
        back_populates="modificateur",
        foreign_keys="PageCompteAdministratif.modifie_par"
    )

    # Relations vers audit log
    audit_logs: Mapped[List["AuditLog"]] = relationship(
        "AuditLog",
        back_populates="utilisateur"
    )

    def __repr__(self) -> str:
        return f"<Utilisateur(id={self.id}, email='{self.email}', role='{self.role.value}')>"

    @property
    def nom_complet(self) -> str:
        """Retourne le nom complet de l'utilisateur."""
        if self.prenom:
            return f"{self.prenom} {self.nom}"
        return self.nom

    @property
    def is_admin(self) -> bool:
        """Vérifie si l'utilisateur est admin."""
        return self.role == RoleUtilisateur.ADMIN

    @property
    def is_editor(self) -> bool:
        """Vérifie si l'utilisateur peut éditer (admin ou éditeur)."""
        return self.role in (RoleUtilisateur.ADMIN, RoleUtilisateur.EDITEUR)


class Session(Base):
    """
    Sessions utilisateurs et refresh tokens JWT.
    Permet de gérer les tokens de rafraîchissement.
    """
    __tablename__ = "sessions"
    __table_args__ = (
        Index("idx_sessions_utilisateur", "utilisateur_id"),
        Index("idx_sessions_token", "refresh_token"),
        Index("idx_sessions_expires", "expires_at"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    utilisateur_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("utilisateurs.id", ondelete="CASCADE"),
        nullable=False
    )
    refresh_token: Mapped[str] = mapped_column(String(500), nullable=False)
    expires_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    ip_address: Mapped[Optional[str]] = mapped_column(String(45), nullable=True)
    user_agent: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    # Relations
    utilisateur: Mapped["Utilisateur"] = relationship(
        "Utilisateur",
        back_populates="sessions"
    )

    def __repr__(self) -> str:
        return f"<Session(id={self.id}, utilisateur_id={self.utilisateur_id})>"

    @property
    def is_expired(self) -> bool:
        """Vérifie si la session a expiré."""
        return datetime.utcnow() > self.expires_at
