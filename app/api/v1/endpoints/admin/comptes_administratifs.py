"""
Admin API endpoints for Comptes Administratifs.
Virtual view combining Commune + Exercice + financial data.
"""

from datetime import date, datetime
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.api.deps import CurrentEditor, get_db
from app.models.comptabilite import CompteAdministratif as CompteAdministratifModel, DonneesDepenses, DonneesRecettes, Exercice, PlanComptable
from app.models.geographie import Commune, Region, Province

router = APIRouter(prefix="/comptes-administratifs", tags=["Admin - Comptes Administratifs"])


# ============================================================================
# SCHEMAS
# ============================================================================

class CommuneInfo(BaseModel):
    id: str
    code: str
    nom: str


class RegionInfo(BaseModel):
    id: str
    code: str
    nom: str


class ProvinceInfo(BaseModel):
    id: str
    code: str
    nom: str


class CompteAdministratifRead(BaseModel):
    id: str
    commune_id: Optional[str] = None
    region_id: Optional[str] = None
    province_id: Optional[str] = None
    annee: int
    statut: str = "publie"  # brouillon, valide, publie, archive
    date_validation: Optional[datetime] = None
    date_publication: Optional[datetime] = None
    validateur_id: Optional[str] = None
    notes: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    created_by: Optional[str] = None
    # Relations
    commune: Optional[CommuneInfo] = None
    region: Optional[RegionInfo] = None
    province: Optional[ProvinceInfo] = None


class CompteAdministratifWithStats(CompteAdministratifRead):
    nombre_lignes: int = 0
    collectivite_nom: str = ""
    collectivite_type: str = "commune"


class CompteAdministratifListResponse(BaseModel):
    items: list[CompteAdministratifWithStats]
    total: int
    page: int
    limit: int
    pages: int


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def _generate_compte_id(commune_id: int, exercice_id: int) -> str:
    """Generate a unique ID for a compte administratif."""
    return f"{commune_id}-{exercice_id}"


def _parse_compte_id(compte_id: str) -> tuple[int, int]:
    """Parse commune_id and exercice_id from compte_id."""
    try:
        parts = compte_id.split("-")
        if len(parts) == 2:
            return int(parts[0]), int(parts[1])
    except (ValueError, IndexError):
        pass
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="ID de compte administratif invalide"
    )


def _get_statut(exercice: Exercice, has_data: bool) -> str:
    """Determine the status of a compte administratif."""
    if exercice.cloture:
        return "archive"
    if has_data:
        return "publie"
    return "brouillon"


# ============================================================================
# CREATE SCHEMA
# ============================================================================

class CompteAdministratifCreate(BaseModel):
    commune_id: int
    annee: int
    notes: Optional[str] = None


# ============================================================================
# ENDPOINTS
# ============================================================================

@router.post(
    "",
    response_model=CompteAdministratifRead,
    status_code=status.HTTP_201_CREATED,
    summary="Créer un compte administratif",
    description="Crée un nouveau compte administratif pour une commune et une année.",
)
async def create_compte_administratif(
    data: CompteAdministratifCreate,
    current_user: CurrentEditor,
    db: Session = Depends(get_db),
):
    """
    Create a new compte administratif (commune + exercice pair).
    If the exercice for the given year doesn't exist, it is created automatically.
    """
    # Validate commune
    commune = db.query(Commune).filter(Commune.id == data.commune_id).first()
    if not commune:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Commune non trouvée"
        )

    # Find or create exercice for the year
    exercice = db.query(Exercice).filter(Exercice.annee == data.annee).first()
    if not exercice:
        exercice = Exercice(
            annee=data.annee,
            libelle=f"Exercice {data.annee}",
            date_debut=date(data.annee, 1, 1),
            date_fin=date(data.annee, 12, 31),
            cloture=False,
        )
        db.add(exercice)
        db.commit()
        db.refresh(exercice)

    if exercice.cloture:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="L'exercice est clôturé, impossible de créer un compte"
        )

    # Check if already registered in the comptes_administratifs table
    existing = (
        db.query(CompteAdministratifModel)
        .filter(
            CompteAdministratifModel.commune_id == data.commune_id,
            CompteAdministratifModel.exercice_id == exercice.id,
        )
        .first()
    )
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Un compte administratif existe déjà pour cette commune et cet exercice"
        )

    # Persist into comptes_administratifs table
    compte_row = CompteAdministratifModel(
        commune_id=data.commune_id,
        exercice_id=exercice.id,
        notes=data.notes,
        created_by=current_user.id,
    )
    db.add(compte_row)
    db.commit()
    db.refresh(compte_row)

    # Check if financial data already exists for this pair
    has_data = (
        db.query(DonneesRecettes)
        .filter(
            DonneesRecettes.commune_id == data.commune_id,
            DonneesRecettes.exercice_id == exercice.id,
        )
        .count()
        + db.query(DonneesDepenses)
        .filter(
            DonneesDepenses.commune_id == data.commune_id,
            DonneesDepenses.exercice_id == exercice.id,
        )
        .count()
    ) > 0

    # Get region and province
    region = db.query(Region).filter(Region.id == commune.region_id).first()
    province = db.query(Province).filter(Province.id == region.province_id).first() if region else None

    compte_id = _generate_compte_id(commune.id, exercice.id)

    return CompteAdministratifRead(
        id=compte_id,
        commune_id=str(commune.id),
        region_id=str(region.id) if region else None,
        province_id=str(province.id) if province else None,
        annee=exercice.annee,
        statut=_get_statut(exercice, has_data),
        notes=data.notes,
        created_at=exercice.created_at or datetime.now(),
        updated_at=exercice.updated_at or datetime.now(),
        commune=CommuneInfo(
            id=str(commune.id),
            code=commune.code,
            nom=commune.nom
        ),
        region=RegionInfo(
            id=str(region.id),
            code=region.code,
            nom=region.nom
        ) if region else None,
        province=ProvinceInfo(
            id=str(province.id),
            code=province.code,
            nom=province.nom
        ) if province else None,
    )


@router.get(
    "",
    response_model=CompteAdministratifListResponse,
    summary="Liste des comptes administratifs",
    description="Retourne la liste des comptes administratifs (combinaisons commune/exercice).",
)
async def list_comptes_administratifs(
    commune_id: Optional[int] = Query(default=None, description="Filtrer par commune"),
    region_id: Optional[int] = Query(default=None, description="Filtrer par région"),
    annee: Optional[int] = Query(default=None, description="Filtrer par année"),
    statut: Optional[str] = Query(default=None, description="Filtrer par statut"),  # noqa: ARG001
    search: Optional[str] = Query(default=None, description="Recherche textuelle"),
    page: int = Query(default=1, ge=1, description="Numéro de page"),
    limit: int = Query(default=20, ge=1, le=100, description="Nombre d'éléments par page"),
    db: Session = Depends(get_db),
):
    """
    Get list of all comptes administratifs.
    A compte administratif is a virtual view of a commune's financial data for a fiscal year.
    """
    # Approche simplifiée: récupérer toutes les combinaisons commune/exercice avec des données
    # D'abord, récupérer les IDs uniques depuis recettes et dépenses
    recettes_pairs = db.query(
        DonneesRecettes.commune_id.label('commune_id'),
        DonneesRecettes.exercice_id.label('exercice_id')
    ).distinct().all()

    depenses_pairs = db.query(
        DonneesDepenses.commune_id.label('commune_id'),
        DonneesDepenses.exercice_id.label('exercice_id')
    ).distinct().all()

    # Also include registered comptes from the comptes_administratifs table
    registered_pairs = db.query(
        CompteAdministratifModel.commune_id,
        CompteAdministratifModel.exercice_id,
    ).all()

    # Combiner les paires uniques
    all_pairs = set()
    for r in recettes_pairs:
        all_pairs.add((r.commune_id, r.exercice_id))
    for d in depenses_pairs:
        all_pairs.add((d.commune_id, d.exercice_id))
    for rp in registered_pairs:
        all_pairs.add((rp.commune_id, rp.exercice_id))

    # Si pas de données, retourner liste vide
    if not all_pairs:
        return CompteAdministratifListResponse(
            items=[],
            total=0,
            page=page,
            limit=limit,
            pages=0
        )

    # Construire la liste des résultats
    results_raw = []
    for commune_id_val, exercice_id_val in all_pairs:
        commune = db.query(Commune).filter(Commune.id == commune_id_val).first()
        exercice = db.query(Exercice).filter(Exercice.id == exercice_id_val).first()

        if not commune or not exercice:
            continue

        # Compter les lignes
        recettes_count = db.query(DonneesRecettes).filter(
            DonneesRecettes.commune_id == commune_id_val,
            DonneesRecettes.exercice_id == exercice_id_val
        ).count()

        depenses_count = db.query(DonneesDepenses).filter(
            DonneesDepenses.commune_id == commune_id_val,
            DonneesDepenses.exercice_id == exercice_id_val
        ).count()

        results_raw.append({
            'commune': commune,
            'exercice': exercice,
            'recettes_count': recettes_count,
            'depenses_count': depenses_count,
        })

    # Appliquer les filtres sur results_raw
    if commune_id:
        results_raw = [r for r in results_raw if r['commune'].id == commune_id]

    if region_id:
        results_raw = [r for r in results_raw if r['commune'].region_id == region_id]

    if annee:
        results_raw = [r for r in results_raw if r['exercice'].annee == annee]

    if search:
        search_lower = search.lower()
        results_raw = [r for r in results_raw if search_lower in r['commune'].nom.lower()]

    # Trier par année (desc) puis par nom de commune
    results_raw.sort(key=lambda r: (-r['exercice'].annee, r['commune'].nom))

    # Total et pagination
    total = len(results_raw)
    pages = (total + limit - 1) // limit if total > 0 else 0
    offset = (page - 1) * limit
    paginated = results_raw[offset:offset + limit]

    # Construire la réponse
    items = []
    for r in paginated:
        commune = r['commune']
        exercice = r['exercice']
        recettes_count = r['recettes_count']
        depenses_count = r['depenses_count']

        # Get region and province info
        region = db.query(Region).filter(Region.id == commune.region_id).first()
        province = db.query(Province).filter(Province.id == region.province_id).first() if region else None

        compte_id = _generate_compte_id(commune.id, exercice.id)
        has_data = (recettes_count or 0) + (depenses_count or 0) > 0

        items.append(CompteAdministratifWithStats(
            id=compte_id,
            commune_id=str(commune.id),
            region_id=str(region.id) if region else None,
            province_id=str(province.id) if province else None,
            annee=exercice.annee,
            statut=_get_statut(exercice, has_data),
            created_at=exercice.created_at or datetime.now(),
            updated_at=exercice.updated_at or datetime.now(),
            commune=CommuneInfo(
                id=str(commune.id),
                code=commune.code,
                nom=commune.nom
            ) if commune else None,
            region=RegionInfo(
                id=str(region.id),
                code=region.code,
                nom=region.nom
            ) if region else None,
            province=ProvinceInfo(
                id=str(province.id),
                code=province.code,
                nom=province.nom
            ) if province else None,
            nombre_lignes=(recettes_count or 0) + (depenses_count or 0),
            collectivite_nom=commune.nom,
            collectivite_type="commune"
        ))

    return CompteAdministratifListResponse(
        items=items,
        total=total,
        page=page,
        limit=limit,
        pages=pages
    )


@router.get(
    "/{compte_id}",
    response_model=CompteAdministratifRead,
    summary="Détail d'un compte administratif",
    description="Retourne les détails d'un compte administratif.",
)
async def get_compte_administratif(
    compte_id: str,
    db: Session = Depends(get_db),
):
    """
    Get a compte administratif by ID.
    The ID format is: {commune_id}-{exercice_id}
    """
    commune_id_parsed, exercice_id = _parse_compte_id(compte_id)

    # Get commune
    commune = db.query(Commune).filter(Commune.id == commune_id_parsed).first()
    if not commune:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Commune non trouvée"
        )

    # Get exercice
    exercice = db.query(Exercice).filter(Exercice.id == exercice_id).first()
    if not exercice:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Exercice non trouvé"
        )

    # Check if data exists
    recettes_count = (
        db.query(DonneesRecettes)
        .filter(
            DonneesRecettes.commune_id == commune_id_parsed,
            DonneesRecettes.exercice_id == exercice_id
        )
        .count()
    )

    depenses_count = (
        db.query(DonneesDepenses)
        .filter(
            DonneesDepenses.commune_id == commune_id_parsed,
            DonneesDepenses.exercice_id == exercice_id
        )
        .count()
    )

    has_data = recettes_count + depenses_count > 0

    # Get region and province
    region = db.query(Region).filter(Region.id == commune.region_id).first()
    province = db.query(Province).filter(Province.id == region.province_id).first() if region else None

    return CompteAdministratifRead(
        id=compte_id,
        commune_id=str(commune.id),
        region_id=str(region.id) if region else None,
        province_id=str(province.id) if province else None,
        annee=exercice.annee,
        statut=_get_statut(exercice, has_data),
        created_at=exercice.created_at or datetime.now(),
        updated_at=exercice.updated_at or datetime.now(),
        commune=CommuneInfo(
            id=str(commune.id),
            code=commune.code,
            nom=commune.nom
        ),
        region=RegionInfo(
            id=str(region.id),
            code=region.code,
            nom=region.nom
        ) if region else None,
        province=ProvinceInfo(
            id=str(province.id),
            code=province.code,
            nom=province.nom
        ) if province else None,
    )


# ============================================================================
# SCHEMAS FOR LIGNES BUDGETAIRES
# ============================================================================

class RubriqueInfo(BaseModel):
    id: str
    code: str
    intitule: str
    type: str  # recette | depense
    section: Optional[str] = None  # fonctionnement | investissement
    niveau: int
    parent_id: Optional[str] = None


class LigneBudgetaireRead(BaseModel):
    id: str
    compte_administratif_id: str
    rubrique_id: str
    valeurs: dict
    notes: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    updated_by: Optional[str] = None
    rubrique: Optional[RubriqueInfo] = None


# ============================================================================
# LIGNES BUDGETAIRES ENDPOINT
# ============================================================================

@router.get(
    "/{compte_id}/lignes",
    response_model=list[LigneBudgetaireRead],
    summary="Lignes budgétaires d'un compte administratif",
    description="Retourne les lignes budgétaires (recettes et dépenses) d'un compte administratif.",
)
async def get_lignes_budgetaires(
    compte_id: str,
    type: Optional[str] = Query(default=None, description="Filtrer par type: recette, depense"),
    db: Session = Depends(get_db),
):
    """
    Get budget lines for a compte administratif.
    Returns recettes and depenses data transformed into LigneBudgetaire format.
    """
    commune_id_parsed, exercice_id = _parse_compte_id(compte_id)

    # Verify commune and exercice exist
    commune = db.query(Commune).filter(Commune.id == commune_id_parsed).first()
    if not commune:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Commune non trouvée"
        )

    exercice = db.query(Exercice).filter(Exercice.id == exercice_id).first()
    if not exercice:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Exercice non trouvé"
        )

    lignes = []

    # Get recettes if type is None or "recette"
    if type is None or type == "recette":
        recettes = db.query(DonneesRecettes).filter(
            DonneesRecettes.commune_id == commune_id_parsed,
            DonneesRecettes.exercice_id == exercice_id
        ).all()

        for r in recettes:
            compte = db.query(PlanComptable).filter(PlanComptable.code == r.compte_code).first()
            lignes.append(LigneBudgetaireRead(
                id=f"R-{r.id}",
                compte_administratif_id=compte_id,
                rubrique_id=r.compte_code,
                valeurs={
                    "budget_primitif": float(r.budget_primitif or 0),
                    "budget_additionnel": float(r.budget_additionnel or 0),
                    "modifications": float(r.modifications or 0),
                    "previsions_definitives": float(r.previsions_definitives or 0),
                    "or_admis": float(r.or_admis or 0),
                    "recouvrement": float(r.recouvrement or 0),
                    "reste_a_recouvrer": float(r.reste_a_recouvrer or 0),
                },
                notes=r.commentaire,
                created_at=r.created_at or datetime.now(),
                updated_at=r.updated_at or datetime.now(),
                rubrique=RubriqueInfo(
                    id=compte.code if compte else r.compte_code,
                    code=compte.code if compte else r.compte_code,
                    intitule=compte.intitule if compte else r.compte_code,
                    type="recette",
                    section=compte.section.value if compte and compte.section else None,
                    niveau=compte.niveau if compte else 1,
                    parent_id=compte.parent_code if compte else None,
                ) if compte else None,
            ))

    # Get depenses if type is None or "depense"
    if type is None or type == "depense":
        depenses = db.query(DonneesDepenses).filter(
            DonneesDepenses.commune_id == commune_id_parsed,
            DonneesDepenses.exercice_id == exercice_id
        ).all()

        for d in depenses:
            compte = db.query(PlanComptable).filter(PlanComptable.code == d.compte_code).first()
            lignes.append(LigneBudgetaireRead(
                id=f"D-{d.id}",
                compte_administratif_id=compte_id,
                rubrique_id=d.compte_code,
                valeurs={
                    "budget_primitif": float(d.budget_primitif or 0),
                    "budget_additionnel": float(d.budget_additionnel or 0),
                    "modifications": float(d.modifications or 0),
                    "previsions_definitives": float(d.previsions_definitives or 0),
                    "engagement": float(d.engagement or 0),
                    "mandat_admis": float(d.mandat_admis or 0),
                    "paiement": float(d.paiement or 0),
                    "reste_a_payer": float(d.reste_a_payer or 0),
                },
                notes=d.commentaire,
                created_at=d.created_at or datetime.now(),
                updated_at=d.updated_at or datetime.now(),
                rubrique=RubriqueInfo(
                    id=compte.code if compte else d.compte_code,
                    code=compte.code if compte else d.compte_code,
                    intitule=compte.intitule if compte else d.compte_code,
                    type="depense",
                    section=compte.section.value if compte and compte.section else None,
                    niveau=compte.niveau if compte else 1,
                    parent_id=compte.parent_code if compte else None,
                ) if compte else None,
            ))

    return lignes
