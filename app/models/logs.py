"""
Modèles pour les logs et audit trail
"""

import uuid
from sqlalchemy import Column, String, Text, Integer, Boolean, DateTime, ForeignKey, Index
from sqlalchemy.dialects.postgresql import UUID, JSONB, INET
from sqlalchemy.orm import relationship

from app.models.base import Base, TimestampMixin


class LogVisite(Base):
    """Logs de visites du site"""
    __tablename__ = "logs_visites"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    page = Column(String(255))
    utilisateur_id = Column(UUID(as_uuid=True), ForeignKey("utilisateurs.id", ondelete="SET NULL"))
    ip_adresse = Column(INET)
    user_agent = Column(Text)
    session_id = Column(String(255))
    duree_secondes = Column(Integer)
    created_at = Column(DateTime)

    # Relations
    utilisateur = relationship("Utilisateur", back_populates="logs_visites")

    def __repr__(self):
        return f"<LogVisite(page='{self.page}', created_at={self.created_at})>"


class LogTelechargement(Base):
    """Logs de téléchargements"""
    __tablename__ = "logs_telechargements"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    document_id = Column(UUID(as_uuid=True), ForeignKey("documents.id", ondelete="SET NULL"))
    type_export = Column(String(50))  # excel, word, pdf
    commune_id = Column(UUID(as_uuid=True), ForeignKey("communes.id", ondelete="SET NULL"))
    exercice_id = Column(UUID(as_uuid=True), ForeignKey("exercices.id", ondelete="SET NULL"))
    utilisateur_id = Column(UUID(as_uuid=True), ForeignKey("utilisateurs.id", ondelete="SET NULL"))
    ip_adresse = Column(INET)
    user_agent = Column(Text)
    created_at = Column(DateTime)

    # Relations
    document = relationship("Document", back_populates="logs_telechargements")
    commune = relationship("Commune")
    exercice = relationship("Exercice", back_populates="logs_telechargements")
    utilisateur = relationship("Utilisateur", back_populates="logs_telechargements")

    def __repr__(self):
        return f"<LogTelechargement(type_export='{self.type_export}', created_at={self.created_at})>"


class LogActivite(Base):
    """Logs d'activité système pour audit"""
    __tablename__ = "logs_activites"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    utilisateur_id = Column(UUID(as_uuid=True), ForeignKey("utilisateurs.id", ondelete="SET NULL"))
    action = Column(String(100), nullable=False)  # CREATE, UPDATE, DELETE, LOGIN, LOGOUT
    entite = Column(String(100))  # nom de la table concernée
    entite_id = Column(UUID(as_uuid=True))
    anciennes_valeurs = Column(JSONB)
    nouvelles_valeurs = Column(JSONB)
    ip_adresse = Column(INET)
    user_agent = Column(Text)
    created_at = Column(DateTime)

    # Relations
    utilisateur = relationship("Utilisateur", back_populates="logs_activites")

    # Index
    __table_args__ = (
        Index('idx_logs_activites_utilisateur', 'utilisateur_id'),
        Index('idx_logs_activites_action', 'action'),
        Index('idx_logs_activites_date', 'created_at'),
    )

    def __repr__(self):
        return f"<LogActivite(action='{self.action}', entite='{self.entite}')>"


class MessageSecurise(Base, TimestampMixin):
    """Messages sécurisés entre utilisateurs"""
    __tablename__ = "messages_securises"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    sujet = Column(String(255), nullable=False)
    contenu = Column(Text, nullable=False)
    expediteur_id = Column(UUID(as_uuid=True), ForeignKey("utilisateurs.id", ondelete="SET NULL"))
    destinataire_id = Column(UUID(as_uuid=True), ForeignKey("utilisateurs.id", ondelete="CASCADE"), nullable=False)
    commune_id = Column(UUID(as_uuid=True), ForeignKey("communes.id", ondelete="SET NULL"))
    lu = Column(Boolean, default=False)
    lu_le = Column(DateTime)
    priorite = Column(String(50), default="normale")  # basse, normale, haute, urgente
    fichiers_joints = Column(JSONB)
    archive = Column(Boolean, default=False)

    # Relations
    expediteur = relationship("Utilisateur", foreign_keys=[expediteur_id], back_populates="messages_envoyes")
    destinataire = relationship("Utilisateur", foreign_keys=[destinataire_id], back_populates="messages_recus")
    commune = relationship("Commune", back_populates="messages_securises")

    def __repr__(self):
        return f"<MessageSecurise(sujet='{self.sujet}', lu={self.lu})>"
