"""
Enumeration types for the database models.
Maps to PostgreSQL ENUM types defined in schema.sql.
"""

import enum


class TypeMouvement(str, enum.Enum):
    """Type de mouvement financier (recette ou dépense)."""
    RECETTE = "recette"
    DEPENSE = "depense"


class SectionBudgetaire(str, enum.Enum):
    """Section budgétaire (fonctionnement ou investissement)."""
    FONCTIONNEMENT = "fonctionnement"
    INVESTISSEMENT = "investissement"


class RoleUtilisateur(str, enum.Enum):
    """Rôles des utilisateurs de la plateforme."""
    ADMIN = "admin"
    EDITEUR = "editeur"
    LECTEUR = "lecteur"
    COMMUNE = "commune"


class TypeDocument(str, enum.Enum):
    """Types de documents uploadés."""
    COMPTE_ADMINISTRATIF = "compte_administratif"
    BUDGET_PRIMITIF = "budget_primitif"
    BUDGET_ADDITIONNEL = "budget_additionnel"
    PIECE_JUSTIFICATIVE = "piece_justificative"
    RAPPORT = "rapport"
    AUTRE = "autre"


class StatutPublication(str, enum.Enum):
    """Statut de publication des pages CMS."""
    BROUILLON = "brouillon"
    PUBLIE = "publie"
    ARCHIVE = "archive"


class TypeSectionCMS(str, enum.Enum):
    """Types de sections CMS pour les pages compte administratif."""
    EDITORJS = "editorjs"
    BLOC_IMAGE_GAUCHE = "bloc_image_gauche"
    BLOC_IMAGE_DROITE = "bloc_image_droite"
    CARTE_FOND_IMAGE = "carte_fond_image"
    GRILLE_CARTES = "grille_cartes"
    GALERIE_PHOTOS = "galerie_photos"
    NOTE_INFORMATIVE = "note_informative"
    LIENS_UTILES = "liens_utiles"
    TABLEAU_FINANCIER = "tableau_financier"
    GRAPHIQUES_ANALYTIQUES = "graphiques_analytiques"


class TypeRevenuMinier(str, enum.Enum):
    """Types de revenus miniers."""
    RISTOURNE_MINIERE = "ristourne_miniere"
    REDEVANCE_MINIERE = "redevance_miniere"
    FRAIS_ADMINISTRATION_MINIERE = "frais_administration_miniere"
    QUOTE_PART_RISTOURNE = "quote_part_ristourne"
    AUTRE = "autre"


class StatutProjetMinier(str, enum.Enum):
    """Statut des projets miniers."""
    EXPLORATION = "exploration"
    EXPLOITATION = "exploitation"
    REHABILITATION = "rehabilitation"
    FERME = "ferme"


class TypeCommune(str, enum.Enum):
    """Type de commune (urbaine ou rurale)."""
    URBAINE = "urbaine"
    RURALE = "rurale"


class TypeCarte(str, enum.Enum):
    """Type de carte informative."""
    IMAGE = "image"
    STATISTIQUE = "statistique"
    ICONE = "icone"


class ActionAudit(str, enum.Enum):
    """Types d'actions pour l'audit log."""
    INSERT = "INSERT"
    UPDATE = "UPDATE"
    DELETE = "DELETE"
