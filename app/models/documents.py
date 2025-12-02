"""
Document model for file attachments.
"""

from typing import TYPE_CHECKING, Optional

from sqlalchemy import BigInteger, Boolean, Enum, ForeignKey, Index, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from app.models.base import TimestampMixin
from app.models.enums import TypeDocument

if TYPE_CHECKING:
    from app.models.geographie import Commune
    from app.models.comptabilite import Exercice
    from app.models.utilisateurs import Utilisateur


class Document(Base, TimestampMixin):
    """
    Documents et pièces justificatives.
    Stocke les métadonnées des fichiers uploadés.
    """
    __tablename__ = "documents"
    __table_args__ = (
        Index("idx_documents_commune", "commune_id"),
        Index("idx_documents_exercice", "exercice_id"),
        Index("idx_documents_type", "type_document"),
        Index("idx_documents_public", "public", postgresql_where="public = TRUE"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    commune_id: Mapped[Optional[int]] = mapped_column(
        Integer,
        ForeignKey("communes.id", ondelete="CASCADE"),
        nullable=True
    )
    exercice_id: Mapped[Optional[int]] = mapped_column(
        Integer,
        ForeignKey("exercices.id", ondelete="SET NULL"),
        nullable=True
    )
    type_document: Mapped[TypeDocument] = mapped_column(
        Enum(TypeDocument, name="type_document", create_type=False),
        nullable=False
    )
    titre: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    nom_fichier: Mapped[str] = mapped_column(String(255), nullable=False)
    chemin_fichier: Mapped[str] = mapped_column(String(500), nullable=False)
    taille_octets: Mapped[Optional[int]] = mapped_column(BigInteger, nullable=True)
    mime_type: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    uploade_par: Mapped[Optional[int]] = mapped_column(
        Integer,
        ForeignKey("utilisateurs.id", ondelete="SET NULL"),
        nullable=True
    )
    nb_telechargements: Mapped[int] = mapped_column(Integer, default=0)
    public: Mapped[bool] = mapped_column(Boolean, default=True)

    # Relations
    commune: Mapped[Optional["Commune"]] = relationship(
        "Commune",
        back_populates="documents"
    )
    exercice: Mapped[Optional["Exercice"]] = relationship(
        "Exercice",
        back_populates="documents"
    )
    uploadeur: Mapped[Optional["Utilisateur"]] = relationship(
        "Utilisateur",
        back_populates="documents_uploades",
        foreign_keys=[uploade_par]
    )

    def __repr__(self) -> str:
        return f"<Document(id={self.id}, titre='{self.titre}', type='{self.type_document.value}')>"

    @property
    def taille_formatee(self) -> str:
        """Retourne la taille du fichier formatée (Ko, Mo, Go)."""
        if self.taille_octets is None:
            return "Inconnu"

        size = self.taille_octets
        for unit in ["o", "Ko", "Mo", "Go"]:
            if size < 1024:
                return f"{size:.1f} {unit}"
            size /= 1024
        return f"{size:.1f} To"

    @property
    def extension(self) -> str:
        """Retourne l'extension du fichier."""
        if "." in self.nom_fichier:
            return self.nom_fichier.rsplit(".", 1)[1].lower()
        return ""
