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

        # Calcul automatique des champs dérivés
        RevenuService._calculate_derived_fields(revenu, db)

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

        # Recalcul des champs dérivés
        RevenuService._calculate_derived_fields(revenu, db)

        db.commit()
        db.refresh(revenu)
        return revenu

    @staticmethod
    def _calculate_derived_fields(revenu: Revenu, db: Session) -> None:
        """Calcule automatiquement les champs dérivés (prévisions définitives, reste à recouvrer, etc.)"""

        # Calcul des prévisions définitives: BP + BA + MOD
        revenu.previsions_definitives = (
            (revenu.budget_primitif or Decimal(0)) +
            (revenu.budget_additionnel or Decimal(0)) +
            (revenu.modifications or Decimal(0))
        )

        # Récupérer le type de rubrique pour déterminer si c'est une recette ou une dépense
        rubrique = db.query(Rubrique).filter(Rubrique.id == revenu.rubrique_id).first()

        if rubrique and rubrique.type == 'recette':
            # Pour les RECETTES:
            # Reste à recouvrer = OR ADMIS - RECOUVREMENT
            revenu.reste_a_recouvrer = (
                (revenu.ordre_recette_admis or Decimal(0)) -
                (revenu.recouvrement or Decimal(0))
            )

            # Taux d'exécution = (OR ADMIS / Prévisions Définitives) * 100
            if revenu.previsions_definitives and revenu.previsions_definitives > 0:
                revenu.taux_realisation = (
                    (revenu.ordre_recette_admis or Decimal(0)) / revenu.previsions_definitives * 100
                )

        elif rubrique and rubrique.type == 'depense':
            # Pour les DEPENSES:
            # Reste à payer = MANDAT ADMIS - PAIEMENT
            revenu.reste_a_payer = (
                (revenu.mandat_admis or Decimal(0)) -
                (revenu.paiement or Decimal(0))
            )

            # Taux d'exécution = (MANDAT ADMIS / Prévisions Définitives) * 100
            if revenu.previsions_definitives and revenu.previsions_definitives > 0:
                revenu.taux_realisation = (
                    (revenu.mandat_admis or Decimal(0)) / revenu.previsions_definitives * 100
                )

        # Backward compatibility: Calcul avec l'ancien modèle
        if revenu.montant_prevu and revenu.montant_prevu > 0:
            revenu.ecart = (revenu.montant or Decimal(0)) - revenu.montant_prevu

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

        # Convertir les modèles SQLAlchemy en dictionnaires
        from app.schemas.geographie import Commune as CommuneSchema
        from app.schemas.revenus import Exercice as ExerciceSchema, Periode as PeriodeSchema, Rubrique as RubriqueSchema

        return {
            "commune": CommuneSchema.model_validate(commune).model_dump(),
            "exercice": ExerciceSchema.model_validate(exercice).model_dump(),
            "periodes": [PeriodeSchema.model_validate(p).model_dump() for p in periodes],
            "rubriques": [RubriqueSchema.model_validate(r).model_dump() for r in rubriques],
            "donnees": {
                str(rubrique_id): {
                    str(periode_id): {
                        # Colonnes de budget (communes)
                        "budget_primitif": float(revenu.budget_primitif) if revenu.budget_primitif else 0,
                        "budget_additionnel": float(revenu.budget_additionnel) if revenu.budget_additionnel else 0,
                        "modifications": float(revenu.modifications) if revenu.modifications else 0,
                        "previsions_definitives": float(revenu.previsions_definitives) if revenu.previsions_definitives else 0,

                        # Colonnes spécifiques RECETTES
                        "ordre_recette_admis": float(revenu.ordre_recette_admis) if revenu.ordre_recette_admis else 0,
                        "recouvrement": float(revenu.recouvrement) if revenu.recouvrement else 0,
                        "reste_a_recouvrer": float(revenu.reste_a_recouvrer) if revenu.reste_a_recouvrer else 0,

                        # Colonnes spécifiques DEPENSES
                        "engagement": float(revenu.engagement) if revenu.engagement else 0,
                        "mandat_admis": float(revenu.mandat_admis) if revenu.mandat_admis else 0,
                        "paiement": float(revenu.paiement) if revenu.paiement else 0,
                        "reste_a_payer": float(revenu.reste_a_payer) if revenu.reste_a_payer else 0,

                        # Taux d'exécution
                        "taux_realisation": float(revenu.taux_realisation) if revenu.taux_realisation else None,

                        # Ancien modèle (backward compatibility)
                        "montant": float(revenu.montant) if revenu.montant else 0,
                        "montant_prevu": float(revenu.montant_prevu) if revenu.montant_prevu else None,
                        "ecart": float(revenu.ecart) if revenu.ecart else None
                    }
                    for periode_id, revenu in periodes_data.items()
                }
                for rubrique_id, periodes_data in donnees_pivot.items()
            },
            "totaux": {str(k): float(v) for k, v in totaux_rubriques.items()}
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

        # Convertir le modèle SQLAlchemy en dictionnaire
        from app.schemas.geographie import Commune as CommuneSchema

        return {
            "commune": CommuneSchema.model_validate(commune).model_dump(),
            "total_recettes": float(total_recettes),
            "total_depenses": float(total_depenses),
            "solde": float(total_recettes - total_depenses),
            "nb_projets_miniers": 0,  # TODO: implémenter
            "exercices_disponibles": []  # TODO: implémenter
        }
