"""
Service pour la gestion des revenus
"""

from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func
from typing import List, Optional, Dict, Any
from uuid import UUID
from decimal import Decimal

from app.models.revenus import Revenu, Exercice, Periode, Rubrique
from app.models.geographie import Commune, Region, Departement
from app.schemas.revenus import RevenuCreate, RevenuUpdate


class RevenuService:
    """Service pour les opérations sur les revenus"""

    @staticmethod
    def create_revenu(db: Session, revenu_data: RevenuCreate) -> Revenu:
        """Crée une nouvelle entrée de revenu"""
        revenu = Revenu(**revenu_data.model_dump())

        # Calcul automatique de l'écart et du taux
        if revenu.montant_prevu and revenu.montant_prevu > 0:
            revenu.ecart = revenu.montant - revenu.montant_prevu
            revenu.taux_realisation = (revenu.montant / revenu.montant_prevu) * 100

        db.add(revenu)
        db.commit()
        db.refresh(revenu)
        return revenu

    @staticmethod
    def update_revenu(
        db: Session,
        revenu_id: UUID,
        revenu_data: RevenuUpdate,
        utilisateur_id: UUID
    ) -> Revenu:
        """Met à jour un revenu"""
        revenu = db.query(Revenu).filter(Revenu.id == revenu_id).first()
        if not revenu:
            raise ValueError("Revenu non trouvé")

        update_data = revenu_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(revenu, field, value)

        revenu.updated_by = utilisateur_id

        # Recalcul
        if revenu.montant_prevu and revenu.montant_prevu > 0:
            revenu.ecart = revenu.montant - revenu.montant_prevu
            revenu.taux_realisation = (revenu.montant / revenu.montant_prevu) * 100

        db.commit()
        db.refresh(revenu)
        return revenu

    @staticmethod
    def get_revenus_by_commune(
        db: Session,
        commune_code: str,
        exercice_annee: Optional[int] = None
    ) -> List[Revenu]:
        """Récupère tous les revenus d'une commune"""
        query = (
            db.query(Revenu)
            .join(Commune)
            .filter(Commune.code == commune_code)
            .options(
                joinedload(Revenu.rubrique),
                joinedload(Revenu.periode),
                joinedload(Revenu.projet_minier)
            )
        )

        if exercice_annee:
            query = query.join(Periode).join(Exercice).filter(
                Exercice.annee == exercice_annee
            )

        return query.all()

    @staticmethod
    def get_tableau_compte_administratif(
        db: Session,
        commune_code: str,
        exercice_annee: int
    ) -> Dict[str, Any]:
        """Génère le tableau de compte administratif complet"""
        # Récupération de la commune
        commune = (
            db.query(Commune)
            .options(
                joinedload(Commune.departement).joinedload(Departement.region),
                joinedload(Commune.region)
            )
            .filter(Commune.code == commune_code)
            .first()
        )
        if not commune:
            raise ValueError("Commune non trouvée")

        # Récupération de l'exercice
        exercice = db.query(Exercice).filter(Exercice.annee == exercice_annee).first()
        if not exercice:
            raise ValueError("Exercice non trouvé")

        # Récupération des périodes
        periodes = (
            db.query(Periode)
            .filter(Periode.exercice_id == exercice.id, Periode.actif == True)
            .order_by(Periode.ordre)
            .all()
        )

        # Récupération des rubriques
        rubriques = (
            db.query(Rubrique)
            .filter(Rubrique.actif == True)
            .order_by(Rubrique.niveau, Rubrique.ordre)
            .all()
        )

        # Récupération des revenus
        revenus = (
            db.query(Revenu)
            .filter(
                Revenu.commune_id == commune.id,
                Revenu.periode_id.in_([p.id for p in periodes])
            )
            .all()
        )

        # Construction structure pivot: rubrique_id -> periode_id -> revenu
        donnees_pivot = {}
        for revenu in revenus:
            if revenu.rubrique_id not in donnees_pivot:
                donnees_pivot[revenu.rubrique_id] = {}
            donnees_pivot[revenu.rubrique_id][revenu.periode_id] = revenu

        # Calcul des totaux
        totaux_rubriques = {}
        for rubrique in rubriques:
            if rubrique.id in donnees_pivot:
                total = sum(
                    float(rev.montant)
                    for rev in donnees_pivot[rubrique.id].values()
                )
                totaux_rubriques[rubrique.id] = Decimal(str(total))

        return {
            "commune": commune,
            "exercice": exercice,
            "periodes": periodes,
            "rubriques": rubriques,
            "donnees": donnees_pivot,
            "totaux": totaux_rubriques
        }

    @staticmethod
    def get_statistiques_commune(
        db: Session,
        commune_code: str,
        exercice_annee: int
    ) -> Dict[str, Any]:
        """Calcule les statistiques pour une commune"""
        commune = db.query(Commune).filter(Commune.code == commune_code).first()
        if not commune:
            raise ValueError("Commune non trouvée")

        # Total recettes
        total_recettes = (
            db.query(func.sum(Revenu.montant))
            .join(Rubrique)
            .join(Periode)
            .join(Exercice)
            .filter(
                Revenu.commune_id == commune.id,
                Exercice.annee == exercice_annee,
                Rubrique.type == 'recette'
            )
            .scalar() or Decimal(0)
        )

        # Total dépenses
        total_depenses = (
            db.query(func.sum(Revenu.montant))
            .join(Rubrique)
            .join(Periode)
            .join(Exercice)
            .filter(
                Revenu.commune_id == commune.id,
                Exercice.annee == exercice_annee,
                Rubrique.type == 'depense'
            )
            .scalar() or Decimal(0)
        )

        return {
            "commune": commune,
            "total_recettes": total_recettes,
            "total_depenses": total_depenses,
            "solde": total_recettes - total_depenses,
            "nb_projets_miniers": 0,  # TODO: implémenter
            "exercices_disponibles": []  # TODO: implémenter
        }
