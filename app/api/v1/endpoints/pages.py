"""
CMS Pages API endpoints.
Public access to published administrative account pages.
"""

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session, joinedload

from app.api.deps import DbSession, get_db
from app.models.cms import (
    BlocCarteFond,
    BlocImageTexte,
    CarteInformative,
    ContenuEditorJS,
    LienUtile,
    PageCompteAdministratif,
    PhotoGalerie,
    SectionCMS,
)
from app.models.comptabilite import Exercice
from app.models.geographie import Commune, Region
from app.models.enums import StatutPublication
from app.schemas.cms import (
    BlocCarteFondRead,
    BlocImageTexteRead,
    CarteInformativeRead,
    ContenuEditorJSRead,
    LienUtileRead,
    PageCompteAdministratifDetail,
    PageCompteAdministratifList,
    PageCompteAdministratifRead,
    PhotoGalerieRead,
    SectionCMSRead,
    SectionCMSWithContent,
)

router = APIRouter(prefix="/pages", tags=["Pages CMS"])


def _build_section_with_content(section: SectionCMS) -> SectionCMSWithContent:
    """Build a section with all its content."""
    return SectionCMSWithContent(
        id=section.id,
        page_id=section.page_id,
        type_section=section.type_section,
        titre=section.titre,
        ordre=section.ordre,
        visible=section.visible,
        visible_accueil=section.visible_accueil,
        config=section.config,
        created_at=section.created_at,
        updated_at=section.updated_at,
        contenu_editorjs=section.contenu_editorjs,
        bloc_image_texte=section.bloc_image_texte,
        bloc_carte_fond=section.bloc_carte_fond,
        cartes_informatives=section.cartes_informatives,
        photos_galerie=section.photos_galerie,
        liens_utiles=section.liens_utiles
    )


@router.get(
    "",
    response_model=list[PageCompteAdministratifList],
    summary="Liste des pages publiées",
    description="Retourne la liste des pages de compte administratif publiées."
)
async def list_pages(
    commune_id: Optional[int] = Query(
        None,
        description="Filtrer par commune"
    ),
    exercice_annee: Optional[int] = Query(
        None,
        description="Filtrer par année d'exercice"
    ),
    limit: int = Query(
        50,
        ge=1,
        le=200,
        description="Nombre maximum de résultats"
    ),
    offset: int = Query(
        0,
        ge=0,
        description="Nombre de résultats à ignorer"
    ),
    db: Session = Depends(get_db),
):
    """
    Get list of published administrative account pages.

    Only returns pages with status 'publie'.

    - **commune_id**: Filter by commune
    - **exercice_annee**: Filter by fiscal year
    - **limit**: Max results (default 50, max 200)
    - **offset**: Skip results for pagination
    """
    query = db.query(PageCompteAdministratif).filter(
        PageCompteAdministratif.statut == StatutPublication.PUBLIE
    )

    if commune_id:
        query = query.filter(PageCompteAdministratif.commune_id == commune_id)

    if exercice_annee:
        exercice = db.query(Exercice).filter(Exercice.annee == exercice_annee).first()
        if exercice:
            query = query.filter(PageCompteAdministratif.exercice_id == exercice.id)

    pages = query.order_by(
        PageCompteAdministratif.date_publication.desc()
    ).offset(offset).limit(limit).all()

    return pages


@router.get(
    "/by-commune/{commune_id}",
    response_model=list[PageCompteAdministratifList],
    summary="Pages d'une commune",
    description="Retourne les pages publiées d'une commune."
)
async def get_pages_by_commune(
    commune_id: int,
    db: Session = Depends(get_db),
):
    """
    Get all published pages for a specific commune.
    """
    commune = db.query(Commune).filter(Commune.id == commune_id).first()
    if not commune:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Commune non trouvée"
        )

    pages = db.query(PageCompteAdministratif).filter(
        PageCompteAdministratif.commune_id == commune_id,
        PageCompteAdministratif.statut == StatutPublication.PUBLIE
    ).order_by(
        PageCompteAdministratif.date_publication.desc()
    ).all()

    return pages


@router.get(
    "/by-exercice/{exercice_annee}",
    response_model=list[PageCompteAdministratifList],
    summary="Pages d'un exercice",
    description="Retourne les pages publiées d'un exercice."
)
async def get_pages_by_exercice(
    exercice_annee: int,
    db: Session = Depends(get_db),
):
    """
    Get all published pages for a specific fiscal year.
    """
    exercice = db.query(Exercice).filter(Exercice.annee == exercice_annee).first()
    if not exercice:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Exercice {exercice_annee} non trouvé"
        )

    pages = db.query(PageCompteAdministratif).filter(
        PageCompteAdministratif.exercice_id == exercice.id,
        PageCompteAdministratif.statut == StatutPublication.PUBLIE
    ).order_by(
        PageCompteAdministratif.date_publication.desc()
    ).all()

    return pages


@router.get(
    "/{commune_id}/{exercice_annee}",
    response_model=PageCompteAdministratifDetail,
    summary="Page compte administratif",
    description="Retourne une page de compte administratif avec son contenu complet."
)
async def get_page(
    commune_id: int,
    exercice_annee: int,
    db: Session = Depends(get_db),
):
    """
    Get a specific administrative account page by commune and year.

    Returns the full page with all sections and content.
    Only returns published pages.
    """
    # Get exercice
    exercice = db.query(Exercice).filter(Exercice.annee == exercice_annee).first()
    if not exercice:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Exercice {exercice_annee} non trouvé"
        )

    # Get commune with full geographic context
    commune = db.query(Commune).options(
        joinedload(Commune.region).joinedload(Region.province)
    ).filter(Commune.id == commune_id).first()

    if not commune:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Commune non trouvée"
        )

    # Get page with all sections and content
    page = db.query(PageCompteAdministratif).options(
        joinedload(PageCompteAdministratif.sections).joinedload(SectionCMS.contenu_editorjs),
        joinedload(PageCompteAdministratif.sections).joinedload(SectionCMS.bloc_image_texte),
        joinedload(PageCompteAdministratif.sections).joinedload(SectionCMS.bloc_carte_fond),
        joinedload(PageCompteAdministratif.sections).joinedload(SectionCMS.cartes_informatives),
        joinedload(PageCompteAdministratif.sections).joinedload(SectionCMS.photos_galerie),
        joinedload(PageCompteAdministratif.sections).joinedload(SectionCMS.liens_utiles),
    ).filter(
        PageCompteAdministratif.commune_id == commune_id,
        PageCompteAdministratif.exercice_id == exercice.id,
        PageCompteAdministratif.statut == StatutPublication.PUBLIE
    ).first()

    if not page:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Page non publiée ou inexistante"
        )

    # Build sections with content
    sections = [
        _build_section_with_content(s)
        for s in sorted(page.sections, key=lambda x: x.ordre)
        if s.visible
    ]

    return PageCompteAdministratifDetail(
        id=page.id,
        commune_id=page.commune_id,
        exercice_id=page.exercice_id,
        titre=page.titre,
        sous_titre=page.sous_titre,
        meta_description=page.meta_description,
        image_hero_url=page.image_hero_url,
        statut=page.statut,
        afficher_tableau_financier=page.afficher_tableau_financier,
        afficher_graphiques=page.afficher_graphiques,
        date_publication=page.date_publication,
        date_mise_a_jour=page.date_mise_a_jour,
        cree_par=page.cree_par,
        modifie_par=page.modifie_par,
        is_published=page.is_published,
        created_at=page.created_at,
        updated_at=page.updated_at,
        commune_nom=commune.nom,
        commune_code=commune.code,
        exercice_annee=exercice_annee,
        sections=sections
    )


@router.get(
    "/{page_id}/sections",
    response_model=list[SectionCMSWithContent],
    summary="Sections d'une page",
    description="Retourne les sections visibles d'une page publiée."
)
async def get_page_sections(
    page_id: int,
    db: Session = Depends(get_db),
):
    """
    Get visible sections for a published page.
    """
    page = db.query(PageCompteAdministratif).filter(
        PageCompteAdministratif.id == page_id,
        PageCompteAdministratif.statut == StatutPublication.PUBLIE
    ).first()

    if not page:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Page non publiée ou inexistante"
        )

    sections = db.query(SectionCMS).options(
        joinedload(SectionCMS.contenu_editorjs),
        joinedload(SectionCMS.bloc_image_texte),
        joinedload(SectionCMS.bloc_carte_fond),
        joinedload(SectionCMS.cartes_informatives),
        joinedload(SectionCMS.photos_galerie),
        joinedload(SectionCMS.liens_utiles),
    ).filter(
        SectionCMS.page_id == page_id,
        SectionCMS.visible == True
    ).order_by(SectionCMS.ordre).all()

    return [_build_section_with_content(s) for s in sections]


@router.get(
    "/accueil/sections",
    response_model=list[SectionCMSWithContent],
    summary="Sections pour l'accueil",
    description="Retourne les sections marquées comme visibles sur l'accueil."
)
async def get_homepage_sections(
    limit: int = Query(
        10,
        ge=1,
        le=50,
        description="Nombre maximum de sections"
    ),
    db: Session = Depends(get_db),
):
    """
    Get sections marked as visible on homepage.

    Returns sections from published pages that have visible_accueil=True.
    """
    sections = db.query(SectionCMS).options(
        joinedload(SectionCMS.contenu_editorjs),
        joinedload(SectionCMS.bloc_image_texte),
        joinedload(SectionCMS.bloc_carte_fond),
        joinedload(SectionCMS.cartes_informatives),
        joinedload(SectionCMS.photos_galerie),
        joinedload(SectionCMS.liens_utiles),
        joinedload(SectionCMS.page)
    ).filter(
        SectionCMS.visible == True,
        SectionCMS.visible_accueil == True
    ).join(PageCompteAdministratif).filter(
        PageCompteAdministratif.statut == StatutPublication.PUBLIE
    ).order_by(SectionCMS.ordre).limit(limit).all()

    return [_build_section_with_content(s) for s in sections]
