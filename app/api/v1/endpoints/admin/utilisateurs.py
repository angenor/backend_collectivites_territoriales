"""
Admin API endpoints for user management.
CRUD operations for users (admin only).
"""

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session, joinedload

from app.api.deps import CurrentAdmin, get_db
from app.core.security import get_password_hash, verify_password
from app.models.utilisateurs import Utilisateur
from app.models.geographie import Commune
from app.models.enums import RoleUtilisateur
from app.schemas.auth import (
    UserCreate,
    UserList,
    UserRead,
    UserUpdate,
    UserWithCommune,
)
from app.schemas.base import Message

router = APIRouter(prefix="/utilisateurs", tags=["Admin - Utilisateurs"])


@router.get(
    "",
    response_model=list[UserList],
    summary="Liste des utilisateurs",
    description="Retourne la liste de tous les utilisateurs (admin uniquement).",
)
async def list_utilisateurs(
    current_user: CurrentAdmin,
    role: Optional[RoleUtilisateur] = Query(None, description="Filtrer par rôle"),
    actif: Optional[bool] = Query(None, description="Filtrer par statut actif"),
    commune_id: Optional[int] = Query(None, description="Filtrer par commune"),
    search: Optional[str] = Query(
        None, min_length=2, max_length=100, description="Recherche par nom/email"
    ),
    limit: int = Query(50, ge=1, le=200, description="Nombre maximum de résultats"),
    offset: int = Query(0, ge=0, description="Nombre de résultats à ignorer"),
    db: Session = Depends(get_db),
):
    """
    Get list of all users.

    - **role**: Filter by user role
    - **actif**: Filter by active status
    - **commune_id**: Filter by commune
    - **search**: Search in name or email
    - **limit**: Max results (default 50)
    - **offset**: Skip results for pagination
    """
    query = db.query(Utilisateur)

    if role:
        query = query.filter(Utilisateur.role == role)

    if actif is not None:
        query = query.filter(Utilisateur.actif == actif)

    if commune_id:
        query = query.filter(Utilisateur.commune_id == commune_id)

    if search:
        search_pattern = f"%{search}%"
        query = query.filter(
            (Utilisateur.nom.ilike(search_pattern))
            | (Utilisateur.prenom.ilike(search_pattern))
            | (Utilisateur.email.ilike(search_pattern))
        )

    users = query.order_by(Utilisateur.nom).offset(offset).limit(limit).all()

    return [
        UserList(
            id=u.id,
            email=u.email,
            nom=u.nom,
            prenom=u.prenom,
            role=u.role,
            actif=u.actif,
        )
        for u in users
    ]


@router.get(
    "/{user_id}",
    response_model=UserWithCommune,
    summary="Détail d'un utilisateur",
    description="Retourne les détails complets d'un utilisateur.",
)
async def get_utilisateur(
    user_id: int,
    current_user: CurrentAdmin,
    db: Session = Depends(get_db),
):
    """
    Get a user by ID with full details.
    """
    user = (
        db.query(Utilisateur)
        .options(joinedload(Utilisateur.commune))
        .filter(Utilisateur.id == user_id)
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Utilisateur non trouvé"
        )

    return UserWithCommune(
        id=user.id,
        email=user.email,
        nom=user.nom,
        prenom=user.prenom,
        role=user.role,
        commune_id=user.commune_id,
        actif=user.actif,
        email_verifie=user.email_verifie,
        derniere_connexion=user.derniere_connexion,
        nom_complet=user.nom_complet,
        is_admin=user.is_admin,
        is_editor=user.is_editor,
        created_at=user.created_at,
        updated_at=user.updated_at,
        commune_nom=user.commune.nom if user.commune else None,
        commune_code=user.commune.code if user.commune else None,
    )


@router.post(
    "",
    response_model=UserRead,
    status_code=status.HTTP_201_CREATED,
    summary="Créer un utilisateur",
    description="Crée un nouvel utilisateur (admin uniquement).",
)
async def create_utilisateur(
    user_data: UserCreate,
    current_user: CurrentAdmin,
    db: Session = Depends(get_db),
):
    """
    Create a new user.

    - **email**: Unique email address
    - **password**: Min 8 characters
    - **nom**: User's last name
    - **prenom**: User's first name (optional)
    - **role**: User role (default: lecteur)
    - **commune_id**: Associated commune (optional)
    """
    # Check if email exists
    existing = db.query(Utilisateur).filter(Utilisateur.email == user_data.email).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Un utilisateur avec cet email existe déjà",
        )

    # Validate commune if provided
    if user_data.commune_id:
        commune = db.query(Commune).filter(Commune.id == user_data.commune_id).first()
        if not commune:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Commune non trouvée"
            )

    # Create user
    user = Utilisateur(
        email=user_data.email,
        mot_de_passe_hash=get_password_hash(user_data.password),
        nom=user_data.nom,
        prenom=user_data.prenom,
        role=user_data.role,
        commune_id=user_data.commune_id,
        actif=True,
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    return UserRead(
        id=user.id,
        email=user.email,
        nom=user.nom,
        prenom=user.prenom,
        role=user.role,
        commune_id=user.commune_id,
        actif=user.actif,
        email_verifie=user.email_verifie,
        derniere_connexion=user.derniere_connexion,
        nom_complet=user.nom_complet,
        is_admin=user.is_admin,
        is_editor=user.is_editor,
        created_at=user.created_at,
        updated_at=user.updated_at,
    )


@router.put(
    "/{user_id}",
    response_model=UserRead,
    summary="Modifier un utilisateur",
    description="Modifie les informations d'un utilisateur.",
)
async def update_utilisateur(
    user_id: int,
    user_data: UserUpdate,
    current_user: CurrentAdmin,
    db: Session = Depends(get_db),
):
    """
    Update a user's information.
    """
    user = db.query(Utilisateur).filter(Utilisateur.id == user_id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Utilisateur non trouvé"
        )

    # Check email uniqueness if changing
    if user_data.email and user_data.email != user.email:
        existing = (
            db.query(Utilisateur).filter(Utilisateur.email == user_data.email).first()
        )
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Un utilisateur avec cet email existe déjà",
            )

    # Validate commune if changing
    if user_data.commune_id is not None and user_data.commune_id != user.commune_id:
        if user_data.commune_id:
            commune = (
                db.query(Commune).filter(Commune.id == user_data.commune_id).first()
            )
            if not commune:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="Commune non trouvée"
                )

    # Update fields
    update_data = user_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(user, field, value)

    db.commit()
    db.refresh(user)

    return UserRead(
        id=user.id,
        email=user.email,
        nom=user.nom,
        prenom=user.prenom,
        role=user.role,
        commune_id=user.commune_id,
        actif=user.actif,
        email_verifie=user.email_verifie,
        derniere_connexion=user.derniere_connexion,
        nom_complet=user.nom_complet,
        is_admin=user.is_admin,
        is_editor=user.is_editor,
        created_at=user.created_at,
        updated_at=user.updated_at,
    )


@router.delete(
    "/{user_id}",
    response_model=Message,
    summary="Supprimer un utilisateur",
    description="Supprime un utilisateur (désactivation).",
)
async def delete_utilisateur(
    user_id: int,
    current_user: CurrentAdmin,
    permanent: bool = Query(
        False, description="Suppression permanente (sinon désactivation)"
    ),
    db: Session = Depends(get_db),
):
    """
    Delete or deactivate a user.

    - **permanent**: If True, permanently deletes the user.
                     If False (default), just deactivates.
    """
    user = db.query(Utilisateur).filter(Utilisateur.id == user_id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Utilisateur non trouvé"
        )

    # Prevent self-deletion
    if user.id == current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Impossible de supprimer votre propre compte",
        )

    if permanent:
        db.delete(user)
        db.commit()
        return Message(message="Utilisateur supprimé définitivement")
    else:
        user.actif = False
        db.commit()
        return Message(message="Utilisateur désactivé")


@router.put(
    "/{user_id}/role",
    response_model=UserRead,
    summary="Changer le rôle",
    description="Change le rôle d'un utilisateur.",
)
async def change_role(
    user_id: int,
    role: RoleUtilisateur,
    current_user: CurrentAdmin,
    db: Session = Depends(get_db),
):
    """
    Change a user's role.
    """
    user = db.query(Utilisateur).filter(Utilisateur.id == user_id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Utilisateur non trouvé"
        )

    # Prevent changing own role
    if user.id == current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Impossible de modifier votre propre rôle",
        )

    user.role = role
    db.commit()
    db.refresh(user)

    return UserRead(
        id=user.id,
        email=user.email,
        nom=user.nom,
        prenom=user.prenom,
        role=user.role,
        commune_id=user.commune_id,
        actif=user.actif,
        email_verifie=user.email_verifie,
        derniere_connexion=user.derniere_connexion,
        nom_complet=user.nom_complet,
        is_admin=user.is_admin,
        is_editor=user.is_editor,
        created_at=user.created_at,
        updated_at=user.updated_at,
    )


@router.put(
    "/{user_id}/activate",
    response_model=UserRead,
    summary="Activer/Désactiver",
    description="Active ou désactive un utilisateur.",
)
async def toggle_active(
    user_id: int,
    actif: bool,
    current_user: CurrentAdmin,
    db: Session = Depends(get_db),
):
    """
    Activate or deactivate a user.
    """
    user = db.query(Utilisateur).filter(Utilisateur.id == user_id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Utilisateur non trouvé"
        )

    # Prevent deactivating self
    if user.id == current_user.id and not actif:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Impossible de désactiver votre propre compte",
        )

    user.actif = actif
    db.commit()
    db.refresh(user)

    return UserRead(
        id=user.id,
        email=user.email,
        nom=user.nom,
        prenom=user.prenom,
        role=user.role,
        commune_id=user.commune_id,
        actif=user.actif,
        email_verifie=user.email_verifie,
        derniere_connexion=user.derniere_connexion,
        nom_complet=user.nom_complet,
        is_admin=user.is_admin,
        is_editor=user.is_editor,
        created_at=user.created_at,
        updated_at=user.updated_at,
    )
