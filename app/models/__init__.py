"""
Import de tous les modeles SQLAlchemy
Necessaire pour que Alembic puisse detecter les modeles
"""

from app.models.base import Base, TimestampMixin, ActiveMixin
from app.models.geographie import Region, Departement, Commune
from app.models.projets_miniers import TypeMinerai, SocieteMiniere, ProjetMinier
from app.models.revenus import (
    Exercice, Periode, CategorieRubrique, Rubrique, Revenu,
    ColonnePersonnalisee, ValeurColonnePersonnalisee
)
from app.models.utilisateurs import Role, Utilisateur
from app.models.documents import TypeDocument, Document
from app.models.newsletter import NewsletterAbonne, NewsletterCampagne
from app.models.logs import LogVisite, LogTelechargement, LogActivite, MessageSecurise

__all__ = [
    "Base",
    "TimestampMixin",
    "ActiveMixin",
    # Geographie
    "Region",
    "Departement",
    "Commune",
    # Projets miniers
    "TypeMinerai",
    "SocieteMiniere",
    "ProjetMinier",
    # Revenus
    "Exercice",
    "Periode",
    "CategorieRubrique",
    "Rubrique",
    "Revenu",
    "ColonnePersonnalisee",
    "ValeurColonnePersonnalisee",
    # Utilisateurs
    "Role",
    "Utilisateur",
    # Documents
    "TypeDocument",
    "Document",
    # Newsletter
    "NewsletterAbonne",
    "NewsletterCampagne",
    # Logs
    "LogVisite",
    "LogTelechargement",
    "LogActivite",
    "MessageSecurise",
]
