"""
Auxiliary models: Newsletter, Statistics, Audit.
"""

from datetime import date, datetime
from typing import TYPE_CHECKING, Optional

from sqlalchemy import Boolean, Date, DateTime, Enum, ForeignKey, Index, Integer, String, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from app.models.enums import ActionAudit

if TYPE_CHECKING:
    from app.models.geographie import Commune
    from app.models.utilisateurs import Utilisateur


class NewsletterAbonne(Base):
    """
    Abonnés à la newsletter.
    """
    __tablename__ = "newsletter_abonnes"
    __table_args__ = (
        Index("idx_newsletter_email", "email"),
        Index("idx_newsletter_actif", "actif", postgresql_where="actif = TRUE"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    nom: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    actif: Mapped[bool] = mapped_column(Boolean, default=True)
    date_inscription: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )
    date_desinscription: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    token_desinscription: Mapped[Optional[str]] = mapped_column(
        String(100),
        unique=True,
        nullable=True
    )

    def __repr__(self) -> str:
        return f"<NewsletterAbonne(id={self.id}, email='{self.email}', actif={self.actif})>"

    def desinscire(self) -> None:
        """Désactive l'abonnement."""
        self.actif = False
        self.date_desinscription = datetime.utcnow()


class StatistiqueVisite(Base):
    """
    Statistiques de visites pour le back-office.
    Agrège les visites par jour/page/commune.
    """
    __tablename__ = "statistiques_visites"
    __table_args__ = (
        Index("idx_stats_date", "date_visite"),
        Index("idx_stats_commune", "commune_id"),
        Index("idx_stats_page", "page"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    date_visite: Mapped[date] = mapped_column(Date, nullable=False)
    page: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    commune_id: Mapped[Optional[int]] = mapped_column(
        Integer,
        ForeignKey("communes.id", ondelete="SET NULL"),
        nullable=True
    )
    nb_visites: Mapped[int] = mapped_column(Integer, default=1)
    nb_telechargements: Mapped[int] = mapped_column(Integer, default=0)
    ip_address: Mapped[Optional[str]] = mapped_column(String(45), nullable=True)
    user_agent: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    # Relations
    commune: Mapped[Optional["Commune"]] = relationship(
        "Commune",
        back_populates="statistiques_visites"
    )

    def __repr__(self) -> str:
        return f"<StatistiqueVisite(id={self.id}, date={self.date_visite}, page='{self.page}')>"


class AuditLog(Base):
    """
    Journal d'audit des modifications.
    Enregistre les opérations INSERT, UPDATE, DELETE.
    """
    __tablename__ = "audit_log"
    __table_args__ = (
        Index("idx_audit_table", "table_name"),
        Index("idx_audit_record", "table_name", "record_id"),
        Index("idx_audit_date", "created_at"),
        Index("idx_audit_utilisateur", "utilisateur_id"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    table_name: Mapped[str] = mapped_column(String(100), nullable=False)
    record_id: Mapped[int] = mapped_column(Integer, nullable=False)
    action: Mapped[ActionAudit] = mapped_column(
        Enum(ActionAudit, name="action_audit", create_type=False),
        nullable=False
    )
    old_values: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)
    new_values: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)
    utilisateur_id: Mapped[Optional[int]] = mapped_column(
        Integer,
        ForeignKey("utilisateurs.id", ondelete="SET NULL"),
        nullable=True
    )
    ip_address: Mapped[Optional[str]] = mapped_column(String(45), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    # Relations
    utilisateur: Mapped[Optional["Utilisateur"]] = relationship(
        "Utilisateur",
        back_populates="audit_logs"
    )

    def __repr__(self) -> str:
        return f"<AuditLog(id={self.id}, table='{self.table_name}', action='{self.action.value}')>"

    @property
    def changes(self) -> dict:
        """Retourne les différences entre anciennes et nouvelles valeurs."""
        if not self.old_values or not self.new_values:
            return {}

        changes = {}
        all_keys = set(self.old_values.keys()) | set(self.new_values.keys())

        for key in all_keys:
            old_val = self.old_values.get(key)
            new_val = self.new_values.get(key)
            if old_val != new_val:
                changes[key] = {"old": old_val, "new": new_val}

        return changes
