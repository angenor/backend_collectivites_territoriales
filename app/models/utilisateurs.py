"""
Modèles pour les utilisateurs et rôles
"""

import uuid
from sqlalchemy import Column, String, Text, Boolean, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship

from app.models.base import Base, TimestampMixin, ActiveMixin


class Role(Base, TimestampMixin, ActiveMixin):
    """Rôles des utilisateurs avec permissions"""
    __tablename__ = "roles"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    code = Column(String(50), unique=True, nullable=False, index=True)
    nom = Column(String(255), nullable=False)
    description = Column(Text)
    permissions = Column(JSONB)  # Liste des permissions en JSON

    # Relations
    utilisateurs = relationship("Utilisateur", back_populates="role")

    def __repr__(self):
        return f"<Role(code='{self.code}', nom='{self.nom}')>"


class Utilisateur(Base, TimestampMixin, ActiveMixin):
    """Utilisateurs de la plateforme"""
    __tablename__ = "utilisateurs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, nullable=False, index=True)
    username = Column(String(100), unique=True, nullable=False, index=True)
    nom = Column(String(255), nullable=False)
    prenom = Column(String(255))
    password_hash = Column(String(255), nullable=False)
    role_id = Column(UUID(as_uuid=True), ForeignKey("roles.id", ondelete="RESTRICT"), nullable=False)
    commune_id = Column(UUID(as_uuid=True), ForeignKey("communes.id", ondelete="SET NULL"))
    telephone = Column(String(50))
    dernier_login = Column(DateTime)
    email_verifie = Column(Boolean, default=False)
    token_verification = Column(String(255))
    token_reset_password = Column(String(255))
    token_expiration = Column(DateTime)

    # Relations
    role = relationship("Role", back_populates="utilisateurs")
    commune = relationship("Commune", back_populates="utilisateurs")
    documents_uploadés = relationship("Document", foreign_keys="Document.uploaded_by", back_populates="uploader")
    logs_visites = relationship("LogVisite", back_populates="utilisateur")
    logs_telechargements = relationship("LogTelechargement", back_populates="utilisateur")
    logs_activites = relationship("LogActivite", back_populates="utilisateur")
    messages_envoyes = relationship("MessageSecurise", foreign_keys="MessageSecurise.expediteur_id", back_populates="expediteur")
    messages_recus = relationship("MessageSecurise", foreign_keys="MessageSecurise.destinataire_id", back_populates="destinataire")
    campagnes_newsletter = relationship("NewsletterCampagne", back_populates="createur")

    def __repr__(self):
        return f"<Utilisateur(username='{self.username}', email='{self.email}')>"
