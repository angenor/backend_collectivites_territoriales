"""
API endpoint pour la gestion des rôles utilisateurs
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import UUID

from app.database import get_db
from app.models.utilisateurs import Role
from app.schemas.utilisateurs import RoleResponse, RoleCreate, RoleUpdate
from app.api.deps import get_current_active_user

router = APIRouter()


@router.get("/", response_model=List[RoleResponse])
def get_roles(
    skip: int = 0,
    limit: int = 100,
    actif_only: bool = True,
    db: Session = Depends(get_db)
):
    """
    Récupère la liste des rôles disponibles.

    - **skip**: Nombre d'éléments à ignorer (pagination)
    - **limit**: Nombre maximum d'éléments à retourner
    - **actif_only**: Si True, retourne uniquement les rôles actifs
    """
    query = db.query(Role)

    if actif_only:
        query = query.filter(Role.actif == True)

    roles = query.order_by(Role.nom).offset(skip).limit(limit).all()
    return roles


@router.get("/{role_id}", response_model=RoleResponse)
def get_role(
    role_id: UUID,
    db: Session = Depends(get_db)
):
    """
    Récupère un rôle spécifique par son ID.

    - **role_id**: UUID du rôle
    """
    role = db.query(Role).filter(Role.id == role_id).first()

    if not role:
        raise HTTPException(
            status_code=404,
            detail=f"Rôle avec l'ID {role_id} introuvable"
        )

    return role


@router.get("/code/{code}", response_model=RoleResponse)
def get_role_by_code(
    code: str,
    db: Session = Depends(get_db)
):
    """
    Récupère un rôle par son code (ex: ADMIN, EDITEUR, LECTEUR).

    - **code**: Code du rôle
    """
    role = db.query(Role).filter(Role.code == code.upper()).first()

    if not role:
        raise HTTPException(
            status_code=404,
            detail=f"Rôle avec le code '{code}' introuvable"
        )

    return role


@router.post("/", response_model=RoleResponse)
def create_role(
    role_data: RoleCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """
    Crée un nouveau rôle (nécessite d'être authentifié).

    - **role_data**: Données du rôle à créer
    """
    # Vérifier que le code n'existe pas déjà
    existing_role = db.query(Role).filter(Role.code == role_data.code.upper()).first()
    if existing_role:
        raise HTTPException(
            status_code=400,
            detail=f"Un rôle avec le code '{role_data.code}' existe déjà"
        )

    # Créer le nouveau rôle
    db_role = Role(
        code=role_data.code.upper(),
        nom=role_data.nom,
        description=role_data.description,
        permissions=role_data.permissions,
        actif=role_data.actif if role_data.actif is not None else True
    )

    db.add(db_role)
    db.commit()
    db.refresh(db_role)

    return db_role


@router.put("/{role_id}", response_model=RoleResponse)
def update_role(
    role_id: UUID,
    role_data: RoleUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """
    Met à jour un rôle existant (nécessite d'être authentifié).

    - **role_id**: UUID du rôle à modifier
    - **role_data**: Nouvelles données du rôle
    """
    role = db.query(Role).filter(Role.id == role_id).first()

    if not role:
        raise HTTPException(
            status_code=404,
            detail=f"Rôle avec l'ID {role_id} introuvable"
        )

    # Mettre à jour les champs fournis
    update_data = role_data.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        if field == "code" and value:
            value = value.upper()
        setattr(role, field, value)

    db.commit()
    db.refresh(role)

    return role


@router.delete("/{role_id}")
def delete_role(
    role_id: UUID,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """
    Supprime un rôle (soft delete - désactive le rôle).
    Nécessite d'être authentifié.

    - **role_id**: UUID du rôle à supprimer
    """
    role = db.query(Role).filter(Role.id == role_id).first()

    if not role:
        raise HTTPException(
            status_code=404,
            detail=f"Rôle avec l'ID {role_id} introuvable"
        )

    # Vérifier que ce n'est pas un rôle système critique
    if role.code in ["ADMIN", "EDITEUR", "LECTEUR"]:
        raise HTTPException(
            status_code=400,
            detail=f"Le rôle système '{role.code}' ne peut pas être supprimé"
        )

    # Soft delete : désactiver le rôle au lieu de le supprimer
    role.actif = False
    db.commit()

    return {"message": f"Rôle '{role.nom}' désactivé avec succès"}
