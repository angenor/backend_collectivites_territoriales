"""
Classes de base et mixins pour les modèles SQLAlchemy
"""

from datetime import datetime
from sqlalchemy import Boolean, Column, DateTime
from app.database import Base


class TimestampMixin:
    """Mixin pour ajouter les timestamps created_at et updated_at"""
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False
    )


class ActiveMixin:
    """Mixin pour le soft delete avec le champ actif"""
    actif = Column(Boolean, default=True, nullable=False)


# Ré-export de Base pour faciliter les imports
__all__ = ["Base", "TimestampMixin", "ActiveMixin"]
