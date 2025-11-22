"""
Service pour la gestion des communes et géographie
"""

from sqlalchemy.orm import Session, joinedload
from sqlalchemy import or_
from typing import List, Optional

from app.models.geographie import Region, Departement, Commune


class CommuneService:
    """Service pour les opérations géographiques"""

    @staticmethod
    def get_all_regions(db: Session, actif_only: bool = True) -> List[Region]:
        """Récupère toutes les régions"""
        query = db.query(Region)
        if actif_only:
            query = query.filter(Region.actif == True)
        return query.order_by(Region.nom).all()

    @staticmethod
    def get_departements_by_region(db: Session, region_code: str) -> List[Departement]:
        """Récupère tous les départements d'une région"""
        return (
            db.query(Departement)
            .join(Region)
            .filter(Region.code == region_code, Departement.actif == True)
            .order_by(Departement.nom)
            .all()
        )

    @staticmethod
    def get_communes_by_departement(db: Session, departement_code: str) -> List[Commune]:
        """Récupère toutes les communes d'un département"""
        return (
            db.query(Commune)
            .join(Departement)
            .filter(Departement.code == departement_code, Commune.actif == True)
            .order_by(Commune.nom)
            .all()
        )

    @staticmethod
    def get_commune_with_hierarchy(db: Session, commune_code: str) -> Optional[Commune]:
        """Récupère une commune avec sa hiérarchie complète"""
        return (
            db.query(Commune)
            .options(
                joinedload(Commune.departement).joinedload(Departement.region),
                joinedload(Commune.region)
            )
            .filter(Commune.code == commune_code)
            .first()
        )

    @staticmethod
    def search_communes(
        db: Session,
        region_code: Optional[str] = None,
        search_term: Optional[str] = None
    ) -> List[Commune]:
        """Recherche de communes avec filtres"""
        query = db.query(Commune).filter(Commune.actif == True)

        if region_code:
            query = query.join(Region).filter(Region.code == region_code)

        if search_term:
            query = query.filter(
                or_(
                    Commune.nom.ilike(f"%{search_term}%"),
                    Commune.code.ilike(f"%{search_term}%")
                )
            )

        return query.order_by(Commune.nom).all()
