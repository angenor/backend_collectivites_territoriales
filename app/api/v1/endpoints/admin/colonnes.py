"""
Admin API endpoints for Colonnes Dynamiques.
CRUD operations for dynamic column definitions.
"""

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.api.deps import CurrentEditor, get_db
from app.models.comptabilite import ColonneDynamique

router = APIRouter(prefix="/colonnes", tags=["Admin - Colonnes Dynamiques"])


# ============================================================================
# SCHEMAS
# ============================================================================

class ColonneBase(BaseModel):
    """Base schema for colonne dynamique."""
    cle: str = Field(..., min_length=1, max_length=50)
    label: str = Field(..., min_length=1, max_length=100)
    applicable_a: str = Field(default="tous", pattern="^(recette|depense|tous|equilibre)$")
    type_donnee: str = Field(default="montant", pattern="^(montant|pourcentage|texte|date|nombre)$")
    formule: Optional[str] = Field(default=None, max_length=255)
    largeur: int = Field(default=120, ge=50, le=500)
    ordre: int = Field(default=1, ge=1)
    est_obligatoire: bool = False
    est_editable: bool = True
    est_visible: bool = True
    est_active: bool = True
    description: Optional[str] = None


class ColonneCreate(ColonneBase):
    """Schema for creating a colonne."""
    pass


class ColonneUpdate(BaseModel):
    """Schema for updating a colonne."""
    label: Optional[str] = Field(default=None, min_length=1, max_length=100)
    applicable_a: Optional[str] = Field(default=None, pattern="^(recette|depense|tous|equilibre)$")
    type_donnee: Optional[str] = Field(default=None, pattern="^(montant|pourcentage|texte|date|nombre)$")
    formule: Optional[str] = Field(default=None, max_length=255)
    largeur: Optional[int] = Field(default=None, ge=50, le=500)
    ordre: Optional[int] = Field(default=None, ge=1)
    est_obligatoire: Optional[bool] = None
    est_editable: Optional[bool] = None
    est_visible: Optional[bool] = None
    est_active: Optional[bool] = None
    description: Optional[str] = None


class ColonneRead(ColonneBase):
    """Schema for reading a colonne."""
    id: int
    est_systeme: bool

    class Config:
        from_attributes = True


class ColonneReorderItem(BaseModel):
    """Schema for reorder request item."""
    id: int
    ordre: int


class ColonneReorderRequest(BaseModel):
    """Schema for batch reorder request."""
    colonnes: list[ColonneReorderItem]


class PaginatedColonnesResponse(BaseModel):
    """Paginated response for colonnes."""
    items: list[ColonneRead]
    total: int
    page: int
    limit: int
    pages: int


# ============================================================================
# ENDPOINTS
# ============================================================================

@router.get(
    "",
    response_model=PaginatedColonnesResponse,
    summary="Liste des colonnes dynamiques",
    description="Retourne les définitions des colonnes pour les tableaux budgétaires.",
)
async def list_colonnes(
    current_user: CurrentEditor,
    applicable_a: Optional[str] = Query(default=None, description="Filtrer: recette, depense, tous, equilibre"),
    est_active: Optional[bool] = Query(default=None, description="Filtrer par colonnes actives"),
    search: Optional[str] = Query(default=None, description="Recherche par clé ou label"),
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=50, ge=1, le=200),
    db: Session = Depends(get_db),
):
    """Get paginated list of dynamic column definitions."""
    query = db.query(ColonneDynamique)

    # Apply filters
    if applicable_a:
        query = query.filter(ColonneDynamique.applicable_a == applicable_a)

    if est_active is not None:
        query = query.filter(ColonneDynamique.est_active == est_active)

    if search:
        search_pattern = f"%{search}%"
        query = query.filter(
            ColonneDynamique.cle.ilike(search_pattern) |
            ColonneDynamique.label.ilike(search_pattern)
        )

    # Count total
    total = query.count()

    # Apply ordering and pagination
    query = query.order_by(ColonneDynamique.applicable_a, ColonneDynamique.ordre)
    offset = (page - 1) * limit
    colonnes = query.offset(offset).limit(limit).all()

    pages = (total + limit - 1) // limit if total > 0 else 1

    items = []
    for c in colonnes:
        items.append(ColonneRead(
            id=c.id,
            cle=c.cle,
            label=c.label,
            applicable_a=c.applicable_a,
            type_donnee=c.type_donnee,
            formule=c.formule,
            largeur=c.largeur,
            ordre=c.ordre,
            est_obligatoire=c.est_obligatoire,
            est_editable=c.est_editable,
            est_visible=c.est_visible,
            est_active=c.est_active,
            est_systeme=c.est_systeme,
            description=c.description,
        ))

    return PaginatedColonnesResponse(
        items=items,
        total=total,
        page=page,
        limit=limit,
        pages=pages,
    )


@router.get(
    "/{colonne_id}",
    response_model=ColonneRead,
    summary="Détail d'une colonne dynamique",
    description="Retourne les détails d'une colonne dynamique.",
)
async def get_colonne(
    colonne_id: int,
    current_user: CurrentEditor,
    db: Session = Depends(get_db),
):
    """Get a single column definition by ID."""
    colonne = db.query(ColonneDynamique).filter(ColonneDynamique.id == colonne_id).first()

    if not colonne:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Colonne non trouvée"
        )

    return ColonneRead(
        id=colonne.id,
        cle=colonne.cle,
        label=colonne.label,
        applicable_a=colonne.applicable_a,
        type_donnee=colonne.type_donnee,
        formule=colonne.formule,
        largeur=colonne.largeur,
        ordre=colonne.ordre,
        est_obligatoire=colonne.est_obligatoire,
        est_editable=colonne.est_editable,
        est_visible=colonne.est_visible,
        est_active=colonne.est_active,
        est_systeme=colonne.est_systeme,
        description=colonne.description,
    )


@router.post(
    "",
    response_model=ColonneRead,
    status_code=status.HTTP_201_CREATED,
    summary="Créer une colonne dynamique",
    description="Crée une nouvelle colonne dynamique.",
)
async def create_colonne(
    data: ColonneCreate,
    current_user: CurrentEditor,
    db: Session = Depends(get_db),
):
    """Create a new column definition."""
    # Check if cle already exists
    existing = db.query(ColonneDynamique).filter(ColonneDynamique.cle == data.cle).first()

    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Une colonne avec la clé '{data.cle}' existe déjà"
        )

    # Create colonne
    colonne = ColonneDynamique(
        cle=data.cle,
        label=data.label,
        applicable_a=data.applicable_a,
        type_donnee=data.type_donnee,
        formule=data.formule,
        largeur=data.largeur,
        ordre=data.ordre,
        est_obligatoire=data.est_obligatoire,
        est_editable=data.est_editable,
        est_visible=data.est_visible,
        est_active=data.est_active,
        est_systeme=False,  # User-created columns are never system columns
        description=data.description,
    )

    db.add(colonne)
    db.commit()
    db.refresh(colonne)

    return ColonneRead(
        id=colonne.id,
        cle=colonne.cle,
        label=colonne.label,
        applicable_a=colonne.applicable_a,
        type_donnee=colonne.type_donnee,
        formule=colonne.formule,
        largeur=colonne.largeur,
        ordre=colonne.ordre,
        est_obligatoire=colonne.est_obligatoire,
        est_editable=colonne.est_editable,
        est_visible=colonne.est_visible,
        est_active=colonne.est_active,
        est_systeme=colonne.est_systeme,
        description=colonne.description,
    )


@router.put(
    "/{colonne_id}",
    response_model=ColonneRead,
    summary="Modifier une colonne dynamique",
    description="Met à jour une colonne dynamique existante.",
)
async def update_colonne(
    colonne_id: int,
    data: ColonneUpdate,
    current_user: CurrentEditor,
    db: Session = Depends(get_db),
):
    """Update an existing column definition."""
    colonne = db.query(ColonneDynamique).filter(ColonneDynamique.id == colonne_id).first()

    if not colonne:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Colonne non trouvée"
        )

    # Update fields
    update_data = data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(colonne, field, value)

    db.commit()
    db.refresh(colonne)

    return ColonneRead(
        id=colonne.id,
        cle=colonne.cle,
        label=colonne.label,
        applicable_a=colonne.applicable_a,
        type_donnee=colonne.type_donnee,
        formule=colonne.formule,
        largeur=colonne.largeur,
        ordre=colonne.ordre,
        est_obligatoire=colonne.est_obligatoire,
        est_editable=colonne.est_editable,
        est_visible=colonne.est_visible,
        est_active=colonne.est_active,
        est_systeme=colonne.est_systeme,
        description=colonne.description,
    )


@router.delete(
    "/{colonne_id}",
    status_code=status.HTTP_200_OK,
    summary="Supprimer une colonne dynamique",
    description="Supprime une colonne dynamique.",
)
async def delete_colonne(
    colonne_id: int,
    current_user: CurrentEditor,
    db: Session = Depends(get_db),
):
    """Delete a column definition."""
    colonne = db.query(ColonneDynamique).filter(ColonneDynamique.id == colonne_id).first()

    if not colonne:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Colonne non trouvée"
        )

    if colonne.est_systeme:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Les colonnes système ne peuvent pas être supprimées"
        )

    db.delete(colonne)
    db.commit()

    return {"message": "Colonne supprimée avec succès"}


@router.post(
    "/reorder",
    response_model=list[ColonneRead],
    summary="Réordonner les colonnes",
    description="Met à jour l'ordre des colonnes.",
)
async def reorder_colonnes(
    data: ColonneReorderRequest,
    current_user: CurrentEditor,
    db: Session = Depends(get_db),
):
    """Reorder multiple columns at once."""
    updated_colonnes = []

    for item in data.colonnes:
        colonne = db.query(ColonneDynamique).filter(ColonneDynamique.id == item.id).first()

        if colonne:
            colonne.ordre = item.ordre
            updated_colonnes.append(colonne)

    db.commit()

    # Refresh all
    result = []
    for colonne in updated_colonnes:
        db.refresh(colonne)
        result.append(ColonneRead(
            id=colonne.id,
            cle=colonne.cle,
            label=colonne.label,
            applicable_a=colonne.applicable_a,
            type_donnee=colonne.type_donnee,
            formule=colonne.formule,
            largeur=colonne.largeur,
            ordre=colonne.ordre,
            est_obligatoire=colonne.est_obligatoire,
            est_editable=colonne.est_editable,
            est_visible=colonne.est_visible,
            est_active=colonne.est_active,
            est_systeme=colonne.est_systeme,
            description=colonne.description,
        ))

    return result
