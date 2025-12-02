"""
CMS models for administrative account pages.
PageCompteAdministratif, SectionCMS, and content blocks.
"""

from datetime import date, datetime
from typing import TYPE_CHECKING, List, Optional

from sqlalchemy import (
    Boolean, Date, DateTime, Enum, ForeignKey, Index,
    Integer, String, Text, UniqueConstraint
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from app.models.base import TimestampMixin
from app.models.enums import StatutPublication, TypeCarte, TypeSectionCMS

if TYPE_CHECKING:
    from app.models.geographie import Commune
    from app.models.comptabilite import Exercice
    from app.models.utilisateurs import Utilisateur


class PageCompteAdministratif(Base, TimestampMixin):
    """
    Pages CMS pour afficher les comptes administratifs.
    Une page par commune/exercice avec contenu éditorialisé.
    """
    __tablename__ = "pages_compte_administratif"
    __table_args__ = (
        UniqueConstraint("commune_id", "exercice_id", name="uk_page_commune_exercice"),
        Index("idx_pages_ca_commune", "commune_id"),
        Index("idx_pages_ca_exercice", "exercice_id"),
        Index("idx_pages_ca_statut", "statut"),
        Index(
            "idx_pages_ca_publie",
            "statut", "date_publication",
            postgresql_where="statut = 'publie'"
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    commune_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("communes.id", ondelete="CASCADE"),
        nullable=False
    )
    exercice_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("exercices.id", ondelete="CASCADE"),
        nullable=False
    )

    # Métadonnées de la page
    titre: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    sous_titre: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    meta_description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    image_hero_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)

    # Statut et publication
    statut: Mapped[StatutPublication] = mapped_column(
        Enum(StatutPublication, name="statut_publication", create_type=False),
        nullable=False,
        default=StatutPublication.BROUILLON
    )
    date_publication: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    date_mise_a_jour: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    # Options d'affichage
    afficher_tableau_financier: Mapped[bool] = mapped_column(Boolean, default=True)
    afficher_graphiques: Mapped[bool] = mapped_column(Boolean, default=True)

    # Audit
    cree_par: Mapped[Optional[int]] = mapped_column(
        Integer,
        ForeignKey("utilisateurs.id", ondelete="SET NULL"),
        nullable=True
    )
    modifie_par: Mapped[Optional[int]] = mapped_column(
        Integer,
        ForeignKey("utilisateurs.id", ondelete="SET NULL"),
        nullable=True
    )

    # Relations
    commune: Mapped["Commune"] = relationship(
        "Commune",
        back_populates="pages_compte_administratif"
    )
    exercice: Mapped["Exercice"] = relationship(
        "Exercice",
        back_populates="pages_compte_administratif"
    )
    createur: Mapped[Optional["Utilisateur"]] = relationship(
        "Utilisateur",
        back_populates="pages_creees",
        foreign_keys=[cree_par]
    )
    modificateur: Mapped[Optional["Utilisateur"]] = relationship(
        "Utilisateur",
        back_populates="pages_modifiees",
        foreign_keys=[modifie_par]
    )
    sections: Mapped[List["SectionCMS"]] = relationship(
        "SectionCMS",
        back_populates="page",
        cascade="all, delete-orphan",
        order_by="SectionCMS.ordre"
    )

    def __repr__(self) -> str:
        return f"<PageCompteAdministratif(id={self.id}, commune_id={self.commune_id}, exercice_id={self.exercice_id})>"

    @property
    def is_published(self) -> bool:
        """Vérifie si la page est publiée."""
        return self.statut == StatutPublication.PUBLIE


class SectionCMS(Base, TimestampMixin):
    """
    Sections de contenu pour les pages compte administratif.
    Chaque section a un type et peut contenir différents blocs.
    """
    __tablename__ = "sections_cms"
    __table_args__ = (
        Index("idx_sections_cms_page", "page_id"),
        Index("idx_sections_cms_ordre", "page_id", "ordre"),
        Index("idx_sections_cms_type", "type_section"),
        Index(
            "idx_sections_cms_visible",
            "page_id", "visible",
            postgresql_where="visible = TRUE"
        ),
        Index(
            "idx_sections_cms_accueil",
            "visible_accueil",
            postgresql_where="visible_accueil = TRUE"
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    page_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("pages_compte_administratif.id", ondelete="CASCADE"),
        nullable=False
    )

    # Type et identification
    type_section: Mapped[TypeSectionCMS] = mapped_column(
        Enum(TypeSectionCMS, name="type_section_cms", create_type=False),
        nullable=False
    )
    titre: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)

    # Ordre et positionnement
    ordre: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    # Visibilité
    visible: Mapped[bool] = mapped_column(Boolean, default=True)
    visible_accueil: Mapped[bool] = mapped_column(Boolean, default=False)

    # Configuration JSON pour options spécifiques au type
    config: Mapped[Optional[dict]] = mapped_column(JSONB, default=dict)

    # Relations
    page: Mapped["PageCompteAdministratif"] = relationship(
        "PageCompteAdministratif",
        back_populates="sections"
    )

    # Relations 1:1 vers contenus spécifiques
    contenu_editorjs: Mapped[Optional["ContenuEditorJS"]] = relationship(
        "ContenuEditorJS",
        back_populates="section",
        uselist=False,
        cascade="all, delete-orphan"
    )
    bloc_image_texte: Mapped[Optional["BlocImageTexte"]] = relationship(
        "BlocImageTexte",
        back_populates="section",
        uselist=False,
        cascade="all, delete-orphan"
    )
    bloc_carte_fond: Mapped[Optional["BlocCarteFond"]] = relationship(
        "BlocCarteFond",
        back_populates="section",
        uselist=False,
        cascade="all, delete-orphan"
    )

    # Relations 1:N vers contenus multiples
    cartes_informatives: Mapped[List["CarteInformative"]] = relationship(
        "CarteInformative",
        back_populates="section",
        cascade="all, delete-orphan",
        order_by="CarteInformative.ordre"
    )
    photos_galerie: Mapped[List["PhotoGalerie"]] = relationship(
        "PhotoGalerie",
        back_populates="section",
        cascade="all, delete-orphan",
        order_by="PhotoGalerie.ordre"
    )
    liens_utiles: Mapped[List["LienUtile"]] = relationship(
        "LienUtile",
        back_populates="section",
        cascade="all, delete-orphan",
        order_by="LienUtile.ordre"
    )

    def __repr__(self) -> str:
        return f"<SectionCMS(id={self.id}, type='{self.type_section.value}', ordre={self.ordre})>"


class ContenuEditorJS(Base, TimestampMixin):
    """
    Contenu texte enrichi au format EditorJS.
    """
    __tablename__ = "contenus_editorjs"
    __table_args__ = (
        UniqueConstraint("section_id", name="uk_editorjs_section"),
        Index("idx_editorjs_section", "section_id"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    section_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("sections_cms.id", ondelete="CASCADE"),
        nullable=False
    )

    # Contenu EditorJS stocké en JSON
    contenu: Mapped[dict] = mapped_column(JSONB, nullable=False)

    # Version pour historique
    version: Mapped[int] = mapped_column(Integer, default=1)

    # Relations
    section: Mapped["SectionCMS"] = relationship(
        "SectionCMS",
        back_populates="contenu_editorjs"
    )

    def __repr__(self) -> str:
        return f"<ContenuEditorJS(id={self.id}, section_id={self.section_id})>"


class BlocImageTexte(Base, TimestampMixin):
    """
    Blocs avec image (gauche ou droite) et contenu texte.
    """
    __tablename__ = "blocs_image_texte"
    __table_args__ = (
        UniqueConstraint("section_id", name="uk_bloc_image_section"),
        Index("idx_blocs_image_section", "section_id"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    section_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("sections_cms.id", ondelete="CASCADE"),
        nullable=False
    )

    # Contenu
    titre: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    sous_titre: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    contenu: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    contenu_html: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Image
    image_url: Mapped[str] = mapped_column(String(500), nullable=False)
    image_alt: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    legende_image: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)

    # Liens/Boutons (stockés en JSON array)
    boutons: Mapped[Optional[list]] = mapped_column(JSONB, default=list)

    # Note de bas
    note: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    note_source: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)

    # Style
    couleur_fond: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    icone_titre: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)

    # Relations
    section: Mapped["SectionCMS"] = relationship(
        "SectionCMS",
        back_populates="bloc_image_texte"
    )

    def __repr__(self) -> str:
        return f"<BlocImageTexte(id={self.id}, titre='{self.titre}')>"


class BlocCarteFond(Base, TimestampMixin):
    """
    Cartes plein écran avec image de fond et contenu superposé.
    """
    __tablename__ = "blocs_carte_fond"
    __table_args__ = (
        UniqueConstraint("section_id", name="uk_carte_fond_section"),
        Index("idx_carte_fond_section", "section_id"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    section_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("sections_cms.id", ondelete="CASCADE"),
        nullable=False
    )

    # Image de fond
    image_url: Mapped[str] = mapped_column(String(500), nullable=False)
    image_alt: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)

    # Contenu superposé
    badge_texte: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    badge_icone: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    titre: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    contenu: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Boutons (JSON array)
    boutons: Mapped[Optional[list]] = mapped_column(JSONB, default=list)

    # Style
    hauteur_min: Mapped[int] = mapped_column(Integer, default=400)
    opacite_overlay: Mapped[int] = mapped_column(Integer, default=50)

    # Relations
    section: Mapped["SectionCMS"] = relationship(
        "SectionCMS",
        back_populates="bloc_carte_fond"
    )

    def __repr__(self) -> str:
        return f"<BlocCarteFond(id={self.id}, titre='{self.titre}')>"


class CarteInformative(Base, TimestampMixin):
    """
    Cartes pour les grilles (3 colonnes typiquement).
    Peut contenir une image, une statistique, ou une icône.
    """
    __tablename__ = "cartes_informatives"
    __table_args__ = (
        Index("idx_cartes_info_section", "section_id"),
        Index("idx_cartes_info_ordre", "section_id", "ordre"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    section_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("sections_cms.id", ondelete="CASCADE"),
        nullable=False
    )

    # Ordre dans la grille
    ordre: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    # Type de carte: image ou statistique
    type_carte: Mapped[TypeCarte] = mapped_column(
        Enum(TypeCarte, name="type_carte", create_type=False),
        default=TypeCarte.IMAGE
    )

    # Contenu image (si type = image)
    image_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    image_alt: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)

    # Contenu statistique (si type = statistique)
    stat_valeur: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    stat_unite: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    stat_evolution: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    stat_icone: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)

    # Badge
    badge_texte: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    badge_icone: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    badge_couleur: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)

    # Texte
    titre: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Lien
    lien_texte: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    lien_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)

    # Note de bas
    note: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)

    # Style
    couleur_fond: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    couleur_gradient_debut: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    couleur_gradient_fin: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)

    # Relations
    section: Mapped["SectionCMS"] = relationship(
        "SectionCMS",
        back_populates="cartes_informatives"
    )

    def __repr__(self) -> str:
        return f"<CarteInformative(id={self.id}, type='{self.type_carte.value}')>"


class PhotoGalerie(Base, TimestampMixin):
    """
    Photos pour les galeries d'images.
    """
    __tablename__ = "photos_galerie"
    __table_args__ = (
        Index("idx_photos_galerie_section", "section_id"),
        Index("idx_photos_galerie_ordre", "section_id", "ordre"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    section_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("sections_cms.id", ondelete="CASCADE"),
        nullable=False
    )

    # Ordre dans la galerie
    ordre: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    # Image
    image_url: Mapped[str] = mapped_column(String(500), nullable=False)
    image_alt: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    image_thumbnail_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)

    # Texte
    titre: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    description: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)

    # Métadonnées optionnelles
    date_prise: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    lieu: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    credit_photo: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)

    # Relations
    section: Mapped["SectionCMS"] = relationship(
        "SectionCMS",
        back_populates="photos_galerie"
    )

    def __repr__(self) -> str:
        return f"<PhotoGalerie(id={self.id}, titre='{self.titre}')>"


class LienUtile(Base, TimestampMixin):
    """
    Liens utiles et documentation.
    """
    __tablename__ = "liens_utiles"
    __table_args__ = (
        Index("idx_liens_utiles_section", "section_id"),
        Index("idx_liens_utiles_ordre", "section_id", "ordre"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    section_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("sections_cms.id", ondelete="CASCADE"),
        nullable=False
    )

    # Ordre
    ordre: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    # Contenu
    titre: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    url: Mapped[str] = mapped_column(String(500), nullable=False)

    # Style
    icone: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    couleur: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    couleur_fond: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)

    # Options
    ouvrir_nouvel_onglet: Mapped[bool] = mapped_column(Boolean, default=True)

    # Relations
    section: Mapped["SectionCMS"] = relationship(
        "SectionCMS",
        back_populates="liens_utiles"
    )

    def __repr__(self) -> str:
        return f"<LienUtile(id={self.id}, titre='{self.titre}')>"
