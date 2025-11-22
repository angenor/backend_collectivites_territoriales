"""
Modèles pour la gestion des documents
"""

import uuid
from sqlalchemy import Column, String, Text, Integer, Boolean, ForeignKey, Index
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from sqlalchemy.orm import relationship

from app.models.base import Base, TimestampMixin, ActiveMixin


class TypeDocument(Base, TimestampMixin, ActiveMixin):
    """Types de documents avec contraintes"""
    __tablename__ = "types_documents"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    code = Column(String(50), unique=True, nullable=False, index=True)
    nom = Column(String(255), nullable=False)
    description = Column(Text)
    extensions_autorisees = Column(ARRAY(Text))  # ['.pdf', '.xlsx', '.docx']
    taille_max_mo = Column(Integer, default=10)

    # Relations
    documents = relationship("Document", back_populates="type_document")

    def __repr__(self):
        return f"<TypeDocument(code='{self.code}', nom='{self.nom}')>"


class Document(Base, TimestampMixin):
    """Documents justificatifs avec indexation full-text"""
    __tablename__ = "documents"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    titre = Column(String(255), nullable=False)
    nom_fichier = Column(String(255), nullable=False)
    chemin_fichier = Column(Text, nullable=False)
    type_document_id = Column(UUID(as_uuid=True), ForeignKey("types_documents.id", ondelete="SET NULL"))
    taille_ko = Column(Integer)
    extension = Column(String(10))
    commune_id = Column(UUID(as_uuid=True), ForeignKey("communes.id", ondelete="CASCADE"))
    exercice_id = Column(UUID(as_uuid=True), ForeignKey("exercices.id", ondelete="CASCADE"))
    revenu_id = Column(UUID(as_uuid=True), ForeignKey("revenus.id", ondelete="CASCADE"))
    description = Column(Text)
    tags = Column(ARRAY(Text))
    indexe = Column(Boolean, default=False)
    contenu_texte = Column(Text)  # Contenu extrait pour la recherche
    uploaded_by = Column(UUID(as_uuid=True), ForeignKey("utilisateurs.id", ondelete="SET NULL"))

    # Relations
    type_document = relationship("TypeDocument", back_populates="documents")
    commune = relationship("Commune", back_populates="documents")
    exercice = relationship("Exercice", back_populates="documents")
    uploader = relationship("Utilisateur", back_populates="documents_uploadés")
    logs_telechargements = relationship("LogTelechargement", back_populates="document")

    # Index pour la recherche
    __table_args__ = (
        Index('idx_documents_tags', 'tags', postgresql_using='gin'),
    )

    def __repr__(self):
        return f"<Document(titre='{self.titre}', nom_fichier='{self.nom_fichier}')>"
