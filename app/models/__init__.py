"""
SQLAlchemy models for the application.
Exports all models for easy access.
"""

# Enums
from app.models.enums import (
    TypeMouvement,
    SectionBudgetaire,
    RoleUtilisateur,
    TypeDocument,
    StatutPublication,
    TypeSectionCMS,
    TypeRevenuMinier,
    StatutProjetMinier,
    TypeCommune,
    TypeCarte,
    ActionAudit,
)

# Base classes
from app.models.base import TimestampMixin

# Geography models
from app.models.geographie import Province, Region, Commune

# User models
from app.models.utilisateurs import Utilisateur, Session

# Accounting models
from app.models.comptabilite import (
    PlanComptable,
    Exercice,
    DonneesRecettes,
    DonneesDepenses,
)

# Mining project models
from app.models.projets_miniers import (
    SocieteMiniere,
    ProjetMinier,
    ProjetCommune,
    RevenuMinier,
)

# Document model
from app.models.documents import Document

# CMS models
from app.models.cms import (
    PageCompteAdministratif,
    SectionCMS,
    ContenuEditorJS,
    BlocImageTexte,
    BlocCarteFond,
    CarteInformative,
    PhotoGalerie,
    LienUtile,
)

# Auxiliary models
from app.models.annexes import (
    NewsletterAbonne,
    StatistiqueVisite,
    AuditLog,
)

__all__ = [
    # Enums
    "TypeMouvement",
    "SectionBudgetaire",
    "RoleUtilisateur",
    "TypeDocument",
    "StatutPublication",
    "TypeSectionCMS",
    "TypeRevenuMinier",
    "StatutProjetMinier",
    "TypeCommune",
    "TypeCarte",
    "ActionAudit",
    # Base
    "TimestampMixin",
    # Geography
    "Province",
    "Region",
    "Commune",
    # Users
    "Utilisateur",
    "Session",
    # Accounting
    "PlanComptable",
    "Exercice",
    "DonneesRecettes",
    "DonneesDepenses",
    # Mining
    "SocieteMiniere",
    "ProjetMinier",
    "ProjetCommune",
    "RevenuMinier",
    # Documents
    "Document",
    # CMS
    "PageCompteAdministratif",
    "SectionCMS",
    "ContenuEditorJS",
    "BlocImageTexte",
    "BlocCarteFond",
    "CarteInformative",
    "PhotoGalerie",
    "LienUtile",
    # Auxiliary
    "NewsletterAbonne",
    "StatistiqueVisite",
    "AuditLog",
]
