"""
Admin API endpoints for Colonnes Dynamiques.
Returns column definitions for the budget tables.
"""

from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Query
from pydantic import BaseModel

router = APIRouter(prefix="/colonnes", tags=["Admin - Colonnes Dynamiques"])


# ============================================================================
# SCHEMAS
# ============================================================================

class ColonneDynamiqueRead(BaseModel):
    id: str
    code: str
    nom: str
    type_donnee: str  # montant | pourcentage | texte | date | nombre
    ordre: int
    est_calculee: bool
    formule_calcul: Optional[str] = None
    format_affichage: Optional[str] = None
    est_active: bool
    applicable_a: str  # recette | depense | tous
    description: Optional[str] = None
    created_at: datetime
    updated_at: datetime


# ============================================================================
# STATIC COLUMN DEFINITIONS
# ============================================================================

# Colonnes pour les recettes
COLONNES_RECETTES = [
    ColonneDynamiqueRead(
        id="col-rec-bp",
        code="budget_primitif",
        nom="Budget Primitif",
        type_donnee="montant",
        ordre=1,
        est_calculee=False,
        est_active=True,
        applicable_a="recette",
        description="Budget voté initialement",
        created_at=datetime.now(),
        updated_at=datetime.now(),
    ),
    ColonneDynamiqueRead(
        id="col-rec-ba",
        code="budget_additionnel",
        nom="Budget Additionnel",
        type_donnee="montant",
        ordre=2,
        est_calculee=False,
        est_active=True,
        applicable_a="recette",
        description="Modifications budgétaires additionnelles",
        created_at=datetime.now(),
        updated_at=datetime.now(),
    ),
    ColonneDynamiqueRead(
        id="col-rec-mod",
        code="modifications",
        nom="Modifications",
        type_donnee="montant",
        ordre=3,
        est_calculee=False,
        est_active=True,
        applicable_a="recette",
        description="Autres modifications",
        created_at=datetime.now(),
        updated_at=datetime.now(),
    ),
    ColonneDynamiqueRead(
        id="col-rec-pd",
        code="previsions_definitives",
        nom="Prévisions Définitives",
        type_donnee="montant",
        ordre=4,
        est_calculee=True,
        formule_calcul="budget_primitif + budget_additionnel + modifications",
        est_active=True,
        applicable_a="recette",
        description="Total des prévisions",
        created_at=datetime.now(),
        updated_at=datetime.now(),
    ),
    ColonneDynamiqueRead(
        id="col-rec-or",
        code="or_admis",
        nom="OR Admis",
        type_donnee="montant",
        ordre=5,
        est_calculee=False,
        est_active=True,
        applicable_a="recette",
        description="Ordres de recettes admis",
        created_at=datetime.now(),
        updated_at=datetime.now(),
    ),
    ColonneDynamiqueRead(
        id="col-rec-rec",
        code="recouvrement",
        nom="Recouvrement",
        type_donnee="montant",
        ordre=6,
        est_calculee=False,
        est_active=True,
        applicable_a="recette",
        description="Montant recouvré",
        created_at=datetime.now(),
        updated_at=datetime.now(),
    ),
    ColonneDynamiqueRead(
        id="col-rec-rar",
        code="reste_a_recouvrer",
        nom="Reste à Recouvrer",
        type_donnee="montant",
        ordre=7,
        est_calculee=True,
        formule_calcul="or_admis - recouvrement",
        est_active=True,
        applicable_a="recette",
        description="Montant restant à recouvrer",
        created_at=datetime.now(),
        updated_at=datetime.now(),
    ),
]

# Colonnes pour les dépenses
COLONNES_DEPENSES = [
    ColonneDynamiqueRead(
        id="col-dep-bp",
        code="budget_primitif",
        nom="Budget Primitif",
        type_donnee="montant",
        ordre=1,
        est_calculee=False,
        est_active=True,
        applicable_a="depense",
        description="Budget voté initialement",
        created_at=datetime.now(),
        updated_at=datetime.now(),
    ),
    ColonneDynamiqueRead(
        id="col-dep-ba",
        code="budget_additionnel",
        nom="Budget Additionnel",
        type_donnee="montant",
        ordre=2,
        est_calculee=False,
        est_active=True,
        applicable_a="depense",
        description="Modifications budgétaires additionnelles",
        created_at=datetime.now(),
        updated_at=datetime.now(),
    ),
    ColonneDynamiqueRead(
        id="col-dep-mod",
        code="modifications",
        nom="Modifications",
        type_donnee="montant",
        ordre=3,
        est_calculee=False,
        est_active=True,
        applicable_a="depense",
        description="Autres modifications",
        created_at=datetime.now(),
        updated_at=datetime.now(),
    ),
    ColonneDynamiqueRead(
        id="col-dep-pd",
        code="previsions_definitives",
        nom="Prévisions Définitives",
        type_donnee="montant",
        ordre=4,
        est_calculee=True,
        formule_calcul="budget_primitif + budget_additionnel + modifications",
        est_active=True,
        applicable_a="depense",
        description="Total des prévisions",
        created_at=datetime.now(),
        updated_at=datetime.now(),
    ),
    ColonneDynamiqueRead(
        id="col-dep-eng",
        code="engagement",
        nom="Engagement",
        type_donnee="montant",
        ordre=5,
        est_calculee=False,
        est_active=True,
        applicable_a="depense",
        description="Montant engagé",
        created_at=datetime.now(),
        updated_at=datetime.now(),
    ),
    ColonneDynamiqueRead(
        id="col-dep-ma",
        code="mandat_admis",
        nom="Mandat Admis",
        type_donnee="montant",
        ordre=6,
        est_calculee=False,
        est_active=True,
        applicable_a="depense",
        description="Mandats admis",
        created_at=datetime.now(),
        updated_at=datetime.now(),
    ),
    ColonneDynamiqueRead(
        id="col-dep-pai",
        code="paiement",
        nom="Paiement",
        type_donnee="montant",
        ordre=7,
        est_calculee=False,
        est_active=True,
        applicable_a="depense",
        description="Montant payé",
        created_at=datetime.now(),
        updated_at=datetime.now(),
    ),
    ColonneDynamiqueRead(
        id="col-dep-rap",
        code="reste_a_payer",
        nom="Reste à Payer",
        type_donnee="montant",
        ordre=8,
        est_calculee=True,
        formule_calcul="mandat_admis - paiement",
        est_active=True,
        applicable_a="depense",
        description="Montant restant à payer",
        created_at=datetime.now(),
        updated_at=datetime.now(),
    ),
]


# ============================================================================
# ENDPOINTS
# ============================================================================

@router.get(
    "",
    response_model=list[ColonneDynamiqueRead],
    summary="Liste des colonnes dynamiques",
    description="Retourne les définitions des colonnes pour les tableaux budgétaires.",
)
async def list_colonnes(
    applicable_a: Optional[str] = Query(default=None, description="Filtrer: recette, depense, tous"),
    est_active: Optional[bool] = Query(default=None, description="Filtrer par colonnes actives"),
):
    """
    Get list of dynamic column definitions.
    Returns predefined columns for recettes and depenses tables.
    """
    colonnes = []

    if applicable_a is None or applicable_a in ("recette", "tous"):
        colonnes.extend(COLONNES_RECETTES)

    if applicable_a is None or applicable_a in ("depense", "tous"):
        colonnes.extend(COLONNES_DEPENSES)

    if est_active is not None:
        colonnes = [c for c in colonnes if c.est_active == est_active]

    # Sort by ordre
    colonnes.sort(key=lambda c: c.ordre)

    return colonnes


@router.get(
    "/{colonne_id}",
    response_model=ColonneDynamiqueRead,
    summary="Détail d'une colonne dynamique",
    description="Retourne les détails d'une colonne dynamique.",
)
async def get_colonne(colonne_id: str):
    """Get a single column definition by ID."""
    all_colonnes = COLONNES_RECETTES + COLONNES_DEPENSES
    for col in all_colonnes:
        if col.id == colonne_id:
            return col

    from fastapi import HTTPException, status
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Colonne non trouvée"
    )
