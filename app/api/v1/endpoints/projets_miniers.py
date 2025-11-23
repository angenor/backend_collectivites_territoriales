"""
Endpoints pour les projets miniers, types de minerais et sociétés minières
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from app.database import get_db
from app.schemas.projets_miniers import (
    TypeMinerai, TypeMineraiCreate, TypeMineraiUpdate,
    SocieteMiniere, SocieteMiniereCreate, SocieteMiniereUpdate,
    ProjetMinier, ProjetMinierCreate, ProjetMinierUpdate, ProjetMinierDetail
)
from app.api.deps import get_current_active_user
from app.models.projets_miniers import (
    TypeMinerai as TypeMineraiModel,
    SocieteMiniere as SocieteMiniereModel,
    ProjetMinier as ProjetMinierModel
)

router = APIRouter()


# ============================================================================
# TYPES DE MINERAIS
# ============================================================================

@router.get("/types-minerais", response_model=List[TypeMinerai], summary="Liste des types de minerais")
def get_types_minerais(
    skip: int = 0,
    limit: int = 100,
    actif_only: bool = True,
    db: Session = Depends(get_db)
):
    """
    Récupère la liste de tous les types de minerais.

    - **skip**: Nombre d'éléments à ignorer (pagination)
    - **limit**: Nombre maximum d'éléments à retourner
    - **actif_only**: Si True, retourne uniquement les types actifs
    """
    query = db.query(TypeMineraiModel)

    if actif_only:
        query = query.filter(TypeMineraiModel.actif == True)

    types = query.order_by(TypeMineraiModel.nom).offset(skip).limit(limit).all()
    return types


@router.get("/types-minerais/{type_id}", response_model=TypeMinerai, summary="Détails d'un type de minerai")
def get_type_minerai(
    type_id: UUID,
    db: Session = Depends(get_db)
):
    """Récupère un type de minerai spécifique par son ID."""
    type_minerai = db.query(TypeMineraiModel).filter(TypeMineraiModel.id == type_id).first()

    if not type_minerai:
        raise HTTPException(
            status_code=404,
            detail=f"Type de minerai avec l'ID {type_id} introuvable"
        )

    return type_minerai


@router.post("/types-minerais", response_model=TypeMinerai, status_code=201, summary="Créer un type de minerai")
def create_type_minerai(
    data: TypeMineraiCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """Crée un nouveau type de minerai (nécessite d'être authentifié)."""
    # Vérifier que le code n'existe pas déjà
    existing = db.query(TypeMineraiModel).filter(TypeMineraiModel.code == data.code.upper()).first()
    if existing:
        raise HTTPException(
            status_code=400,
            detail=f"Un type de minerai avec le code '{data.code}' existe déjà"
        )

    # Créer le nouveau type
    db_type = TypeMineraiModel(
        code=data.code.upper(),
        nom=data.nom,
        description=data.description,
        actif=data.actif
    )

    db.add(db_type)
    db.commit()
    db.refresh(db_type)

    return db_type


@router.put("/types-minerais/{type_id}", response_model=TypeMinerai, summary="Modifier un type de minerai")
def update_type_minerai(
    type_id: UUID,
    data: TypeMineraiUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """Met à jour un type de minerai existant (nécessite d'être authentifié)."""
    type_minerai = db.query(TypeMineraiModel).filter(TypeMineraiModel.id == type_id).first()

    if not type_minerai:
        raise HTTPException(
            status_code=404,
            detail=f"Type de minerai avec l'ID {type_id} introuvable"
        )

    # Mettre à jour les champs fournis
    update_data = data.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(type_minerai, field, value)

    db.commit()
    db.refresh(type_minerai)

    return type_minerai


@router.delete("/types-minerais/{type_id}", summary="Supprimer un type de minerai")
def delete_type_minerai(
    type_id: UUID,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """Désactive un type de minerai (soft delete - nécessite d'être authentifié)."""
    type_minerai = db.query(TypeMineraiModel).filter(TypeMineraiModel.id == type_id).first()

    if not type_minerai:
        raise HTTPException(
            status_code=404,
            detail=f"Type de minerai avec l'ID {type_id} introuvable"
        )

    # Soft delete : désactiver au lieu de supprimer
    type_minerai.actif = False
    db.commit()

    return {"message": f"Type de minerai '{type_minerai.nom}' désactivé avec succès"}


# ============================================================================
# SOCIÉTÉS MINIÈRES
# ============================================================================

@router.get("/societes", response_model=List[SocieteMiniere], summary="Liste des sociétés minières")
def get_societes_minieres(
    skip: int = 0,
    limit: int = 100,
    actif_only: bool = True,
    db: Session = Depends(get_db)
):
    """
    Récupère la liste de toutes les sociétés minières.

    - **skip**: Nombre d'éléments à ignorer (pagination)
    - **limit**: Nombre maximum d'éléments à retourner
    - **actif_only**: Si True, retourne uniquement les sociétés actives
    """
    query = db.query(SocieteMiniereModel)

    if actif_only:
        query = query.filter(SocieteMiniereModel.actif == True)

    societes = query.order_by(SocieteMiniereModel.nom).offset(skip).limit(limit).all()
    return societes


@router.get("/societes/{societe_id}", response_model=SocieteMiniere, summary="Détails d'une société minière")
def get_societe_miniere(
    societe_id: UUID,
    db: Session = Depends(get_db)
):
    """Récupère une société minière spécifique par son ID."""
    societe = db.query(SocieteMiniereModel).filter(SocieteMiniereModel.id == societe_id).first()

    if not societe:
        raise HTTPException(
            status_code=404,
            detail=f"Société minière avec l'ID {societe_id} introuvable"
        )

    return societe


@router.post("/societes", response_model=SocieteMiniere, status_code=201, summary="Créer une société minière")
def create_societe_miniere(
    data: SocieteMiniereCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """Crée une nouvelle société minière (nécessite d'être authentifié)."""
    # Vérifier que le code n'existe pas déjà
    existing = db.query(SocieteMiniereModel).filter(SocieteMiniereModel.code == data.code.upper()).first()
    if existing:
        raise HTTPException(
            status_code=400,
            detail=f"Une société avec le code '{data.code}' existe déjà"
        )

    # Créer la nouvelle société
    db_societe = SocieteMiniereModel(
        code=data.code.upper(),
        nom=data.nom,
        raison_sociale=data.raison_sociale,
        nif=data.nif,
        stat=data.stat,
        adresse=data.adresse,
        telephone=data.telephone,
        email=data.email,
        actif=data.actif
    )

    db.add(db_societe)
    db.commit()
    db.refresh(db_societe)

    return db_societe


@router.put("/societes/{societe_id}", response_model=SocieteMiniere, summary="Modifier une société minière")
def update_societe_miniere(
    societe_id: UUID,
    data: SocieteMiniereUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """Met à jour une société minière existante (nécessite d'être authentifié)."""
    societe = db.query(SocieteMiniereModel).filter(SocieteMiniereModel.id == societe_id).first()

    if not societe:
        raise HTTPException(
            status_code=404,
            detail=f"Société minière avec l'ID {societe_id} introuvable"
        )

    # Mettre à jour les champs fournis
    update_data = data.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(societe, field, value)

    db.commit()
    db.refresh(societe)

    return societe


@router.delete("/societes/{societe_id}", summary="Supprimer une société minière")
def delete_societe_miniere(
    societe_id: UUID,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """Désactive une société minière (soft delete - nécessite d'être authentifié)."""
    societe = db.query(SocieteMiniereModel).filter(SocieteMiniereModel.id == societe_id).first()

    if not societe:
        raise HTTPException(
            status_code=404,
            detail=f"Société minière avec l'ID {societe_id} introuvable"
        )

    # Soft delete : désactiver au lieu de supprimer
    societe.actif = False
    db.commit()

    return {"message": f"Société '{societe.nom}' désactivée avec succès"}
