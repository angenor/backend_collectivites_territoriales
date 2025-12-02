"""
Pydantic schemas for CMS models.
PageCompteAdministratif, SectionCMS, and content blocks.
"""

from datetime import date, datetime
from typing import Any, Dict, List, Optional

from pydantic import Field, HttpUrl

from app.models.enums import StatutPublication, TypeCarte, TypeSectionCMS
from app.schemas.base import BaseSchema, TimestampSchema


# =====================
# Button Schema (shared)
# =====================

class BoutonSchema(BaseSchema):
    """Schema for button/link in CMS blocks."""
    texte: str = Field(..., max_length=100)
    url: str = Field(..., max_length=500)
    type: str = Field(default="primary", max_length=50)  # primary, secondary, outline
    icone: Optional[str] = Field(None, max_length=50)
    ouvrir_nouvel_onglet: bool = True


# =====================
# ContenuEditorJS Schemas
# =====================

class ContenuEditorJSBase(BaseSchema):
    """Base schema for EditorJS content."""
    contenu: Dict[str, Any]  # EditorJS JSON structure
    version: int = 1


class ContenuEditorJSCreate(ContenuEditorJSBase):
    """Schema for creating EditorJS content."""
    section_id: int


class ContenuEditorJSUpdate(BaseSchema):
    """Schema for updating EditorJS content."""
    contenu: Optional[Dict[str, Any]] = None


class ContenuEditorJSRead(ContenuEditorJSBase, TimestampSchema):
    """Schema for reading EditorJS content."""
    id: int
    section_id: int


# =====================
# BlocImageTexte Schemas
# =====================

class BlocImageTexteBase(BaseSchema):
    """Base schema for image-text block."""
    titre: Optional[str] = Field(None, max_length=255)
    sous_titre: Optional[str] = Field(None, max_length=255)
    contenu: Optional[str] = None
    contenu_html: Optional[str] = None
    image_url: str = Field(..., max_length=500)
    image_alt: Optional[str] = Field(None, max_length=255)
    legende_image: Optional[str] = Field(None, max_length=500)
    boutons: List[BoutonSchema] = []
    note: Optional[str] = None
    note_source: Optional[str] = Field(None, max_length=255)
    couleur_fond: Optional[str] = Field(None, max_length=50)
    icone_titre: Optional[str] = Field(None, max_length=50)


class BlocImageTexteCreate(BlocImageTexteBase):
    """Schema for creating image-text block."""
    section_id: int


class BlocImageTexteUpdate(BaseSchema):
    """Schema for updating image-text block."""
    titre: Optional[str] = Field(None, max_length=255)
    sous_titre: Optional[str] = Field(None, max_length=255)
    contenu: Optional[str] = None
    contenu_html: Optional[str] = None
    image_url: Optional[str] = Field(None, max_length=500)
    image_alt: Optional[str] = Field(None, max_length=255)
    legende_image: Optional[str] = Field(None, max_length=500)
    boutons: Optional[List[BoutonSchema]] = None
    note: Optional[str] = None
    note_source: Optional[str] = Field(None, max_length=255)
    couleur_fond: Optional[str] = Field(None, max_length=50)
    icone_titre: Optional[str] = Field(None, max_length=50)


class BlocImageTexteRead(BlocImageTexteBase, TimestampSchema):
    """Schema for reading image-text block."""
    id: int
    section_id: int


# =====================
# BlocCarteFond Schemas
# =====================

class BlocCarteFondBase(BaseSchema):
    """Base schema for background card block."""
    image_url: str = Field(..., max_length=500)
    image_alt: Optional[str] = Field(None, max_length=255)
    badge_texte: Optional[str] = Field(None, max_length=100)
    badge_icone: Optional[str] = Field(None, max_length=50)
    titre: Optional[str] = Field(None, max_length=255)
    contenu: Optional[str] = None
    boutons: List[BoutonSchema] = []
    hauteur_min: int = Field(default=400, ge=100, le=1000)
    opacite_overlay: int = Field(default=50, ge=0, le=100)


class BlocCarteFondCreate(BlocCarteFondBase):
    """Schema for creating background card block."""
    section_id: int


class BlocCarteFondUpdate(BaseSchema):
    """Schema for updating background card block."""
    image_url: Optional[str] = Field(None, max_length=500)
    image_alt: Optional[str] = Field(None, max_length=255)
    badge_texte: Optional[str] = Field(None, max_length=100)
    badge_icone: Optional[str] = Field(None, max_length=50)
    titre: Optional[str] = Field(None, max_length=255)
    contenu: Optional[str] = None
    boutons: Optional[List[BoutonSchema]] = None
    hauteur_min: Optional[int] = Field(None, ge=100, le=1000)
    opacite_overlay: Optional[int] = Field(None, ge=0, le=100)


class BlocCarteFondRead(BlocCarteFondBase, TimestampSchema):
    """Schema for reading background card block."""
    id: int
    section_id: int


# =====================
# CarteInformative Schemas
# =====================

class CarteInformativeBase(BaseSchema):
    """Base schema for informative card."""
    ordre: int = Field(default=0, ge=0)
    type_carte: TypeCarte = TypeCarte.IMAGE
    # Image content
    image_url: Optional[str] = Field(None, max_length=500)
    image_alt: Optional[str] = Field(None, max_length=255)
    # Statistic content
    stat_valeur: Optional[str] = Field(None, max_length=50)
    stat_unite: Optional[str] = Field(None, max_length=50)
    stat_evolution: Optional[str] = Field(None, max_length=50)
    stat_icone: Optional[str] = Field(None, max_length=50)
    # Badge
    badge_texte: Optional[str] = Field(None, max_length=100)
    badge_icone: Optional[str] = Field(None, max_length=50)
    badge_couleur: Optional[str] = Field(None, max_length=50)
    # Text
    titre: Optional[str] = Field(None, max_length=255)
    description: Optional[str] = None
    # Link
    lien_texte: Optional[str] = Field(None, max_length=100)
    lien_url: Optional[str] = Field(None, max_length=500)
    # Note
    note: Optional[str] = Field(None, max_length=255)
    # Style
    couleur_fond: Optional[str] = Field(None, max_length=50)
    couleur_gradient_debut: Optional[str] = Field(None, max_length=50)
    couleur_gradient_fin: Optional[str] = Field(None, max_length=50)


class CarteInformativeCreate(CarteInformativeBase):
    """Schema for creating informative card."""
    section_id: int


class CarteInformativeUpdate(BaseSchema):
    """Schema for updating informative card."""
    ordre: Optional[int] = Field(None, ge=0)
    type_carte: Optional[TypeCarte] = None
    image_url: Optional[str] = Field(None, max_length=500)
    image_alt: Optional[str] = Field(None, max_length=255)
    stat_valeur: Optional[str] = Field(None, max_length=50)
    stat_unite: Optional[str] = Field(None, max_length=50)
    stat_evolution: Optional[str] = Field(None, max_length=50)
    stat_icone: Optional[str] = Field(None, max_length=50)
    badge_texte: Optional[str] = Field(None, max_length=100)
    badge_icone: Optional[str] = Field(None, max_length=50)
    badge_couleur: Optional[str] = Field(None, max_length=50)
    titre: Optional[str] = Field(None, max_length=255)
    description: Optional[str] = None
    lien_texte: Optional[str] = Field(None, max_length=100)
    lien_url: Optional[str] = Field(None, max_length=500)
    note: Optional[str] = Field(None, max_length=255)
    couleur_fond: Optional[str] = Field(None, max_length=50)
    couleur_gradient_debut: Optional[str] = Field(None, max_length=50)
    couleur_gradient_fin: Optional[str] = Field(None, max_length=50)


class CarteInformativeRead(CarteInformativeBase, TimestampSchema):
    """Schema for reading informative card."""
    id: int
    section_id: int


# =====================
# PhotoGalerie Schemas
# =====================

class PhotoGalerieBase(BaseSchema):
    """Base schema for gallery photo."""
    ordre: int = Field(default=0, ge=0)
    image_url: str = Field(..., max_length=500)
    image_alt: Optional[str] = Field(None, max_length=255)
    image_thumbnail_url: Optional[str] = Field(None, max_length=500)
    titre: Optional[str] = Field(None, max_length=255)
    description: Optional[str] = Field(None, max_length=500)
    date_prise: Optional[date] = None
    lieu: Optional[str] = Field(None, max_length=255)
    credit_photo: Optional[str] = Field(None, max_length=255)


class PhotoGalerieCreate(PhotoGalerieBase):
    """Schema for creating gallery photo."""
    section_id: int


class PhotoGalerieUpdate(BaseSchema):
    """Schema for updating gallery photo."""
    ordre: Optional[int] = Field(None, ge=0)
    image_url: Optional[str] = Field(None, max_length=500)
    image_alt: Optional[str] = Field(None, max_length=255)
    image_thumbnail_url: Optional[str] = Field(None, max_length=500)
    titre: Optional[str] = Field(None, max_length=255)
    description: Optional[str] = Field(None, max_length=500)
    date_prise: Optional[date] = None
    lieu: Optional[str] = Field(None, max_length=255)
    credit_photo: Optional[str] = Field(None, max_length=255)


class PhotoGalerieRead(PhotoGalerieBase, TimestampSchema):
    """Schema for reading gallery photo."""
    id: int
    section_id: int


# =====================
# LienUtile Schemas
# =====================

class LienUtileBase(BaseSchema):
    """Base schema for useful link."""
    ordre: int = Field(default=0, ge=0)
    titre: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=500)
    url: str = Field(..., max_length=500)
    icone: Optional[str] = Field(None, max_length=50)
    couleur: Optional[str] = Field(None, max_length=50)
    couleur_fond: Optional[str] = Field(None, max_length=50)
    ouvrir_nouvel_onglet: bool = True


class LienUtileCreate(LienUtileBase):
    """Schema for creating useful link."""
    section_id: int


class LienUtileUpdate(BaseSchema):
    """Schema for updating useful link."""
    ordre: Optional[int] = Field(None, ge=0)
    titre: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=500)
    url: Optional[str] = Field(None, max_length=500)
    icone: Optional[str] = Field(None, max_length=50)
    couleur: Optional[str] = Field(None, max_length=50)
    couleur_fond: Optional[str] = Field(None, max_length=50)
    ouvrir_nouvel_onglet: Optional[bool] = None


class LienUtileRead(LienUtileBase, TimestampSchema):
    """Schema for reading useful link."""
    id: int
    section_id: int


# =====================
# SectionCMS Schemas
# =====================

class SectionCMSBase(BaseSchema):
    """Base schema for CMS section."""
    type_section: TypeSectionCMS
    titre: Optional[str] = Field(None, max_length=255)
    ordre: int = Field(default=0, ge=0)
    visible: bool = True
    visible_accueil: bool = False
    config: Optional[Dict[str, Any]] = None


class SectionCMSCreate(SectionCMSBase):
    """Schema for creating CMS section."""
    page_id: int


class SectionCMSUpdate(BaseSchema):
    """Schema for updating CMS section."""
    type_section: Optional[TypeSectionCMS] = None
    titre: Optional[str] = Field(None, max_length=255)
    ordre: Optional[int] = Field(None, ge=0)
    visible: Optional[bool] = None
    visible_accueil: Optional[bool] = None
    config: Optional[Dict[str, Any]] = None


class SectionCMSRead(SectionCMSBase, TimestampSchema):
    """Schema for reading CMS section."""
    id: int
    page_id: int


class SectionCMSWithContent(SectionCMSRead):
    """Section with its content based on type."""
    contenu_editorjs: Optional[ContenuEditorJSRead] = None
    bloc_image_texte: Optional[BlocImageTexteRead] = None
    bloc_carte_fond: Optional[BlocCarteFondRead] = None
    cartes_informatives: List[CarteInformativeRead] = []
    photos_galerie: List[PhotoGalerieRead] = []
    liens_utiles: List[LienUtileRead] = []


# =====================
# PageCompteAdministratif Schemas
# =====================

class PageCompteAdministratifBase(BaseSchema):
    """Base schema for administrative account page."""
    commune_id: int
    exercice_id: int
    titre: Optional[str] = Field(None, max_length=255)
    sous_titre: Optional[str] = Field(None, max_length=500)
    meta_description: Optional[str] = None
    image_hero_url: Optional[str] = Field(None, max_length=500)
    statut: StatutPublication = StatutPublication.BROUILLON
    afficher_tableau_financier: bool = True
    afficher_graphiques: bool = True


class PageCompteAdministratifCreate(PageCompteAdministratifBase):
    """Schema for creating administrative account page."""
    pass


class PageCompteAdministratifUpdate(BaseSchema):
    """Schema for updating administrative account page."""
    titre: Optional[str] = Field(None, max_length=255)
    sous_titre: Optional[str] = Field(None, max_length=500)
    meta_description: Optional[str] = None
    image_hero_url: Optional[str] = Field(None, max_length=500)
    statut: Optional[StatutPublication] = None
    afficher_tableau_financier: Optional[bool] = None
    afficher_graphiques: Optional[bool] = None


class PageCompteAdministratifRead(PageCompteAdministratifBase, TimestampSchema):
    """Schema for reading administrative account page."""
    id: int
    date_publication: Optional[datetime] = None
    date_mise_a_jour: datetime
    cree_par: Optional[int] = None
    modifie_par: Optional[int] = None
    is_published: bool = False


class PageCompteAdministratifList(BaseSchema):
    """Simplified schema for listing pages."""
    id: int
    commune_id: int
    exercice_id: int
    titre: Optional[str] = None
    statut: StatutPublication
    date_mise_a_jour: datetime


class PageCompteAdministratifWithSections(PageCompteAdministratifRead):
    """Page with its sections."""
    sections: List[SectionCMSWithContent] = []


class PageCompteAdministratifDetail(PageCompteAdministratifRead):
    """Full page detail with commune and exercise info."""
    commune_nom: str
    commune_code: str
    exercice_annee: int
    sections: List[SectionCMSWithContent] = []


# =====================
# Page Publication
# =====================

class PagePublish(BaseSchema):
    """Schema for publishing a page."""
    statut: StatutPublication


# Update forward references
SectionCMSWithContent.model_rebuild()
PageCompteAdministratifWithSections.model_rebuild()
PageCompteAdministratifDetail.model_rebuild()
