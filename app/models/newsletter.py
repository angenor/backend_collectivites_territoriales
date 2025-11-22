"""
Modèles pour la newsletter
"""

import uuid
from sqlalchemy import Column, String, Text, Integer, Boolean, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.models.base import Base, TimestampMixin, ActiveMixin


class NewsletterAbonne(Base, TimestampMixin, ActiveMixin):
    """Abonnés à la newsletter"""
    __tablename__ = "newsletter_abonnes"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, nullable=False, index=True)
    nom = Column(String(255))
    prenom = Column(String(255))
    token_confirmation = Column(String(255))
    confirme = Column(Boolean, default=False)
    confirme_le = Column(DateTime)

    def __repr__(self):
        return f"<NewsletterAbonne(email='{self.email}', confirme={self.confirme})>"


class NewsletterCampagne(Base, TimestampMixin):
    """Campagnes d'envoi de newsletter"""
    __tablename__ = "newsletter_campagnes"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    titre = Column(String(255), nullable=False)
    sujet = Column(String(255), nullable=False)
    contenu = Column(Text, nullable=False)
    date_envoi = Column(DateTime)
    statut = Column(String(50), default="brouillon")  # brouillon, programmée, envoyée
    nb_destinataires = Column(Integer)
    nb_envoyes = Column(Integer, default=0)
    nb_ouverts = Column(Integer, default=0)
    nb_clics = Column(Integer, default=0)
    created_by = Column(UUID(as_uuid=True), ForeignKey("utilisateurs.id", ondelete="SET NULL"))

    # Relations
    createur = relationship("Utilisateur", back_populates="campagnes_newsletter")

    def __repr__(self):
        return f"<NewsletterCampagne(titre='{self.titre}', statut='{self.statut}')>"
