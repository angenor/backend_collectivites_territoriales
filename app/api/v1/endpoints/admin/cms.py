"""
Admin API endpoints for CMS management.
CRUD operations for pages and sections (editor/admin only).
"""

from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session, joinedload

from app.api.deps import CurrentEditor, get_db
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
from app.models.geographie import Commune
from app.models.enums import StatutPublication
from app.schemas.cms import (
    PageCompteAdministratifCreate,
    PageCompteAdministratifList,
    PageCompteAdministratifRead,
    PageCompteAdministratifUpdate,
    PagePublish,
    SectionCMSCreate,
    SectionCMSRead,
    SectionCMSUpdate,
    SectionCMSWithContent,
)
from app.schemas.base import Message

router = APIRouter(prefix="/cms", tags=["Admin - CMS"])


# =====================
# PAGES ENDPOINTS
# =====================


@router.get(
    "/pages",
    response_model=list[PageCompteAdministratifList],
    summary="Liste des pages CMS",
    description="Retourne la liste de toutes les pages (tous statuts).",
)
async def list_pages(
    commune_id: Optional[int] = Query(None, description="Filtrer par commune"),
    exercice_id: Optional[int] = Query(None, description="Filtrer par exercice"),
    statut: Optional[StatutPublication] = Query(None, description="Filtrer par statut"),
    limit: int = Query(50, ge=1, le=200, description="Nombre maximum"),
    offset: int = Query(0, ge=0, description="Offset"),
    current_user: CurrentEditor = None,
    db: Session = Depends(get_db),
):
    """
    Get list of all CMS pages.
    """
    query = db.query(PageCompteAdministratif)

    if commune_id:
        query = query.filter(PageCompteAdministratif.commune_id == commune_id)

    if exercice_id:
        query = query.filter(PageCompteAdministratif.exercice_id == exercice_id)

    if statut:
        query = query.filter(PageCompteAdministratif.statut == statut)

    pages = (
        query.order_by(PageCompteAdministratif.date_mise_a_jour.desc())
        .offset(offset)
        .limit(limit)
        .all()
    )

    return [
        PageCompteAdministratifList(
            id=p.id,
            commune_id=p.commune_id,
            exercice_id=p.exercice_id,
            titre=p.titre,
            statut=p.statut,
            date_mise_a_jour=p.date_mise_a_jour,
        )
        for p in pages
    ]


@router.get(
    "/pages/{page_id}",
    response_model=PageCompteAdministratifRead,
    summary="Détail d'une page",
    description="Retourne les détails d'une page CMS.",
)
async def get_page(
    page_id: int,
    current_user: CurrentEditor = None,
    db: Session = Depends(get_db),
):
    """
    Get a page by ID.
    """
    page = (
        db.query(PageCompteAdministratif)
        .filter(PageCompteAdministratif.id == page_id)
        .first()
    )

    if not page:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Page non trouvée"
        )

    return PageCompteAdministratifRead(
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
    )


@router.post(
    "/pages",
    response_model=PageCompteAdministratifRead,
    status_code=status.HTTP_201_CREATED,
    summary="Créer une page",
    description="Crée une nouvelle page CMS.",
)
async def create_page(
    data: PageCompteAdministratifCreate,
    current_user: CurrentEditor = None,
    db: Session = Depends(get_db),
):
    """
    Create a new CMS page.
    """
    # Validate commune
    commune = db.query(Commune).filter(Commune.id == data.commune_id).first()
    if not commune:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Commune non trouvée"
        )

    # Validate exercice
    exercice = db.query(Exercice).filter(Exercice.id == data.exercice_id).first()
    if not exercice:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Exercice non trouvé"
        )

    # Check for existing page
    existing = (
        db.query(PageCompteAdministratif)
        .filter(
            PageCompteAdministratif.commune_id == data.commune_id,
            PageCompteAdministratif.exercice_id == data.exercice_id,
        )
        .first()
    )

    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Une page existe déjà pour cette commune/exercice",
        )

    page = PageCompteAdministratif(
        **data.model_dump(),
        cree_par=current_user.id,
        modifie_par=current_user.id,
        date_mise_a_jour=datetime.now(),
    )
    db.add(page)
    db.commit()
    db.refresh(page)

    return PageCompteAdministratifRead(
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
    )


@router.put(
    "/pages/{page_id}",
    response_model=PageCompteAdministratifRead,
    summary="Modifier une page",
    description="Modifie une page CMS.",
)
async def update_page(
    page_id: int,
    data: PageCompteAdministratifUpdate,
    current_user: CurrentEditor = None,
    db: Session = Depends(get_db),
):
    """
    Update a CMS page.
    """
    page = (
        db.query(PageCompteAdministratif)
        .filter(PageCompteAdministratif.id == page_id)
        .first()
    )

    if not page:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Page non trouvée"
        )

    update_data = data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(page, field, value)

    page.modifie_par = current_user.id
    page.date_mise_a_jour = datetime.now()

    db.commit()
    db.refresh(page)

    return PageCompteAdministratifRead(
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
    )


@router.delete(
    "/pages/{page_id}",
    response_model=Message,
    summary="Supprimer une page",
    description="Supprime une page CMS et toutes ses sections.",
)
async def delete_page(
    page_id: int,
    current_user: CurrentEditor = None,
    db: Session = Depends(get_db),
):
    """
    Delete a CMS page and all its sections.
    """
    page = (
        db.query(PageCompteAdministratif)
        .filter(PageCompteAdministratif.id == page_id)
        .first()
    )

    if not page:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Page non trouvée"
        )

    # Delete all sections (cascade should handle content)
    db.query(SectionCMS).filter(SectionCMS.page_id == page_id).delete()

    db.delete(page)
    db.commit()

    return Message(message="Page supprimée")


@router.put(
    "/pages/{page_id}/publish",
    response_model=PageCompteAdministratifRead,
    summary="Publier/Dépublier une page",
    description="Change le statut de publication d'une page.",
)
async def publish_page(
    page_id: int,
    data: PagePublish,
    current_user: CurrentEditor = None,
    db: Session = Depends(get_db),
):
    """
    Publish or unpublish a page.
    """
    page = (
        db.query(PageCompteAdministratif)
        .filter(PageCompteAdministratif.id == page_id)
        .first()
    )

    if not page:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Page non trouvée"
        )

    page.statut = data.statut
    page.modifie_par = current_user.id
    page.date_mise_a_jour = datetime.now()

    if data.statut == StatutPublication.PUBLIE and not page.date_publication:
        page.date_publication = datetime.now()

    db.commit()
    db.refresh(page)

    return PageCompteAdministratifRead(
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
    )


# =====================
# SECTIONS ENDPOINTS
# =====================


@router.get(
    "/pages/{page_id}/sections",
    response_model=list[SectionCMSRead],
    summary="Sections d'une page",
    description="Retourne toutes les sections d'une page.",
)
async def list_sections(
    page_id: int,
    current_user: CurrentEditor = None,
    db: Session = Depends(get_db),
):
    """
    Get all sections for a page.
    """
    page = (
        db.query(PageCompteAdministratif)
        .filter(PageCompteAdministratif.id == page_id)
        .first()
    )

    if not page:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Page non trouvée"
        )

    sections = (
        db.query(SectionCMS)
        .filter(SectionCMS.page_id == page_id)
        .order_by(SectionCMS.ordre)
        .all()
    )

    return [
        SectionCMSRead(
            id=s.id,
            page_id=s.page_id,
            type_section=s.type_section,
            titre=s.titre,
            ordre=s.ordre,
            visible=s.visible,
            visible_accueil=s.visible_accueil,
            config=s.config,
            created_at=s.created_at,
            updated_at=s.updated_at,
        )
        for s in sections
    ]


@router.post(
    "/sections",
    response_model=SectionCMSRead,
    status_code=status.HTTP_201_CREATED,
    summary="Créer une section",
    description="Crée une nouvelle section CMS.",
)
async def create_section(
    data: SectionCMSCreate,
    current_user: CurrentEditor = None,
    db: Session = Depends(get_db),
):
    """
    Create a new section.
    """
    page = (
        db.query(PageCompteAdministratif)
        .filter(PageCompteAdministratif.id == data.page_id)
        .first()
    )

    if not page:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Page non trouvée"
        )

    section = SectionCMS(**data.model_dump())
    db.add(section)
    db.commit()
    db.refresh(section)

    # Update page modification date
    page.modifie_par = current_user.id
    page.date_mise_a_jour = datetime.now()
    db.commit()

    return SectionCMSRead(
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
    )


@router.put(
    "/sections/{section_id}",
    response_model=SectionCMSRead,
    summary="Modifier une section",
    description="Modifie une section CMS.",
)
async def update_section(
    section_id: int,
    data: SectionCMSUpdate,
    current_user: CurrentEditor = None,
    db: Session = Depends(get_db),
):
    """
    Update a section.
    """
    section = db.query(SectionCMS).filter(SectionCMS.id == section_id).first()

    if not section:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Section non trouvée"
        )

    update_data = data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(section, field, value)

    db.commit()
    db.refresh(section)

    # Update page modification date
    page = (
        db.query(PageCompteAdministratif)
        .filter(PageCompteAdministratif.id == section.page_id)
        .first()
    )
    if page:
        page.modifie_par = current_user.id
        page.date_mise_a_jour = datetime.now()
        db.commit()

    return SectionCMSRead(
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
    )


@router.delete(
    "/sections/{section_id}",
    response_model=Message,
    summary="Supprimer une section",
    description="Supprime une section et son contenu.",
)
async def delete_section(
    section_id: int,
    current_user: CurrentEditor = None,
    db: Session = Depends(get_db),
):
    """
    Delete a section and its content.
    """
    section = db.query(SectionCMS).filter(SectionCMS.id == section_id).first()

    if not section:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Section non trouvée"
        )

    page_id = section.page_id

    # Delete associated content
    db.query(ContenuEditorJS).filter(ContenuEditorJS.section_id == section_id).delete()
    db.query(BlocImageTexte).filter(BlocImageTexte.section_id == section_id).delete()
    db.query(BlocCarteFond).filter(BlocCarteFond.section_id == section_id).delete()
    db.query(CarteInformative).filter(CarteInformative.section_id == section_id).delete()
    db.query(PhotoGalerie).filter(PhotoGalerie.section_id == section_id).delete()
    db.query(LienUtile).filter(LienUtile.section_id == section_id).delete()

    db.delete(section)
    db.commit()

    # Update page modification date
    page = (
        db.query(PageCompteAdministratif)
        .filter(PageCompteAdministratif.id == page_id)
        .first()
    )
    if page:
        page.modifie_par = current_user.id
        page.date_mise_a_jour = datetime.now()
        db.commit()

    return Message(message="Section supprimée")


@router.put(
    "/sections/reorder",
    response_model=list[SectionCMSRead],
    summary="Réordonner les sections",
    description="Réordonne les sections d'une page.",
)
async def reorder_sections(
    page_id: int = Query(..., description="ID de la page"),
    section_ids: list[int] = Query(..., description="IDs des sections dans l'ordre souhaité"),
    current_user: CurrentEditor = None,
    db: Session = Depends(get_db),
):
    """
    Reorder sections on a page.
    """
    page = (
        db.query(PageCompteAdministratif)
        .filter(PageCompteAdministratif.id == page_id)
        .first()
    )

    if not page:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Page non trouvée"
        )

    for ordre, section_id in enumerate(section_ids):
        section = (
            db.query(SectionCMS)
            .filter(SectionCMS.id == section_id, SectionCMS.page_id == page_id)
            .first()
        )
        if section:
            section.ordre = ordre

    page.modifie_par = current_user.id
    page.date_mise_a_jour = datetime.now()
    db.commit()

    sections = (
        db.query(SectionCMS)
        .filter(SectionCMS.page_id == page_id)
        .order_by(SectionCMS.ordre)
        .all()
    )

    return [
        SectionCMSRead(
            id=s.id,
            page_id=s.page_id,
            type_section=s.type_section,
            titre=s.titre,
            ordre=s.ordre,
            visible=s.visible,
            visible_accueil=s.visible_accueil,
            config=s.config,
            created_at=s.created_at,
            updated_at=s.updated_at,
        )
        for s in sections
    ]
