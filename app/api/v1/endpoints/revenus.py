"""
Endpoints pour les revenus
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
from uuid import UUID

from app.database import get_db
from app.schemas.revenus import Revenu, RevenuCreate, RevenuUpdate
from app.schemas.statistiques import StatistiquesCommune, TableauCompteAdministratif
from app.services.revenu_service import RevenuService
from app.api.deps import get_current_active_user
from app.models.utilisateurs import Utilisateur

router = APIRouter()


@router.post("/", response_model=Revenu, status_code=201, summary="Créer un revenu")
def create_revenu(
    revenu: RevenuCreate,
    db: Session = Depends(get_db),
    current_user: Utilisateur = Depends(get_current_active_user)
):
    """Crée une nouvelle entrée de revenu"""
    try:
        return RevenuService.create_revenu(db, revenu)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{revenu_id}", response_model=Revenu, summary="Mettre à jour un revenu")
def update_revenu(
    revenu_id: UUID,
    revenu: RevenuUpdate,
    db: Session = Depends(get_db),
    current_user: Utilisateur = Depends(get_current_active_user)
):
    """Met à jour un revenu existant"""
    try:
        return RevenuService.update_revenu(db, revenu_id, revenu, current_user.id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get(
    "/commune/{commune_code}",
    response_model=List[Revenu],
    summary="Revenus d'une commune"
)
def get_revenus_by_commune(
    commune_code: str,
    exercice_annee: Optional[int] = Query(None),
    db: Session = Depends(get_db)
):
    """Récupère tous les revenus d'une commune"""
    return RevenuService.get_revenus_by_commune(db, commune_code, exercice_annee)


@router.get(
    "/tableau/{commune_code}/{exercice_annee}",
    response_model=Dict[str, Any],
    summary="Tableau de compte administratif"
)
def get_tableau_compte_administratif(
    commune_code: str,
    exercice_annee: int,
    db: Session = Depends(get_db)
):
    """Génère le tableau de compte administratif complet"""
    try:
        return RevenuService.get_tableau_compte_administratif(db, commune_code, exercice_annee)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get(
    "/statistiques/{commune_code}",
    response_model=Dict[str, Any],
    summary="Statistiques d'une commune"
)
def get_statistiques_commune(
    commune_code: str,
    exercice_annee: int = Query(...),
    db: Session = Depends(get_db)
):
    """Statistiques financières pour une commune"""
    try:
        return RevenuService.get_statistiques_commune(db, commune_code, exercice_annee)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
