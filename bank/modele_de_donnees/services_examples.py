"""
Exemples de services pour FastAPI
Ces services contiennent la logique métier pour manipuler les données
"""

from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func, and_, or_
from typing import List, Optional, Dict, Any
from uuid import UUID
from datetime import datetime
from decimal import Decimal

from models import (
    Region, Departement, Commune,
    Exercice, Periode, Rubrique, Revenu,
    ProjetMinier, Utilisateur, Document,
    LogActivite, LogTelechargement
)
from schemas import (
    RevenuCreate, RevenuUpdate, RevenuFilter,
    CommuneCreate, RubriqueCreate,
    PaginationParams
)


# ============================================================================
# SERVICES GÉOGRAPHIQUES
# ============================================================================

class CommuneService:
    """Service pour la gestion des communes"""

    @staticmethod
    def get_all_regions(db: Session) -> List[Region]:
        """Récupère toutes les régions actives"""
        return db.query(Region).filter(Region.actif == True).order_by(Region.nom).all()

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
        departement_code: Optional[str] = None,
        search_term: Optional[str] = None
    ) -> List[Commune]:
        """Recherche de communes avec filtres"""
        query = db.query(Commune).filter(Commune.actif == True)

        if region_code:
            query = query.join(Region).filter(Region.code == region_code)

        if departement_code:
            query = query.join(Departement).filter(Departement.code == departement_code)

        if search_term:
            query = query.filter(
                or_(
                    Commune.nom.ilike(f"%{search_term}%"),
                    Commune.code.ilike(f"%{search_term}%")
                )
            )

        return query.order_by(Commune.nom).all()


# ============================================================================
# SERVICES REVENUS
# ============================================================================

class RevenuService:
    """Service pour la gestion des revenus"""

    @staticmethod
    def create_revenu(db: Session, revenu_data: RevenuCreate) -> Revenu:
        """Crée une nouvelle entrée de revenu"""
        revenu = Revenu(**revenu_data.model_dump())

        # Calcul automatique de l'écart et du taux de réalisation
        if revenu.montant_prevu and revenu.montant_prevu > 0:
            revenu.ecart = revenu.montant - revenu.montant_prevu
            revenu.taux_realisation = (revenu.montant / revenu.montant_prevu) * 100

        db.add(revenu)
        db.commit()
        db.refresh(revenu)

        # Log de l'activité
        LogActivite.log_action(
            db=db,
            utilisateur_id=revenu.created_by,
            action="CREATE",
            entite="revenus",
            entite_id=revenu.id,
            nouvelles_valeurs=revenu_data.model_dump()
        )

        return revenu

    @staticmethod
    def update_revenu(
        db: Session,
        revenu_id: UUID,
        revenu_data: RevenuUpdate,
        utilisateur_id: UUID
    ) -> Revenu:
        """Met à jour un revenu existant"""
        revenu = db.query(Revenu).filter(Revenu.id == revenu_id).first()
        if not revenu:
            raise ValueError("Revenu non trouvé")

        # Sauvegarde des anciennes valeurs pour le log
        anciennes_valeurs = {
            "montant": float(revenu.montant),
            "montant_prevu": float(revenu.montant_prevu) if revenu.montant_prevu else None,
            "observations": revenu.observations
        }

        # Mise à jour des champs
        update_data = revenu_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(revenu, field, value)

        revenu.updated_by = utilisateur_id

        # Recalcul de l'écart et du taux
        if revenu.montant_prevu and revenu.montant_prevu > 0:
            revenu.ecart = revenu.montant - revenu.montant_prevu
            revenu.taux_realisation = (revenu.montant / revenu.montant_prevu) * 100

        db.commit()
        db.refresh(revenu)

        # Log de l'activité
        LogActivite.log_action(
            db=db,
            utilisateur_id=utilisateur_id,
            action="UPDATE",
            entite="revenus",
            entite_id=revenu.id,
            anciennes_valeurs=anciennes_valeurs,
            nouvelles_valeurs=update_data
        )

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
        """
        Génère le tableau de compte administratif complet pour une commune et un exercice
        Structure pivot optimisée pour l'affichage en tableau
        """
        # Récupération de la commune
        commune = CommuneService.get_commune_with_hierarchy(db, commune_code)
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

        # Récupération des rubriques avec hiérarchie
        rubriques = (
            db.query(Rubrique)
            .filter(Rubrique.actif == True)
            .order_by(Rubrique.niveau, Rubrique.ordre)
            .all()
        )

        # Récupération de tous les revenus
        revenus = (
            db.query(Revenu)
            .filter(
                Revenu.commune_id == commune.id,
                Revenu.periode_id.in_([p.id for p in periodes])
            )
            .all()
        )

        # Construction de la structure de données
        # Dictionnaire: rubrique_id -> periode_id -> revenu
        donnees_pivot = {}
        for revenu in revenus:
            if revenu.rubrique_id not in donnees_pivot:
                donnees_pivot[revenu.rubrique_id] = {}
            donnees_pivot[revenu.rubrique_id][revenu.periode_id] = revenu

        # Calcul des totaux par rubrique
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
    def search_revenus(
        db: Session,
        filters: RevenuFilter,
        pagination: PaginationParams
    ) -> Dict[str, Any]:
        """Recherche de revenus avec filtres et pagination"""
        query = db.query(Revenu)

        # Application des filtres
        if filters.commune_code:
            query = query.join(Commune).filter(Commune.code == filters.commune_code)

        if filters.region_code:
            query = query.join(Commune).join(Region).filter(Region.code == filters.region_code)

        if filters.exercice_annee:
            query = query.join(Periode).join(Exercice).filter(
                Exercice.annee == filters.exercice_annee
            )

        if filters.rubrique_code:
            query = query.join(Rubrique).filter(Rubrique.code == filters.rubrique_code)

        if filters.projet_minier_id:
            query = query.filter(Revenu.projet_minier_id == filters.projet_minier_id)

        if filters.valide is not None:
            query = query.filter(Revenu.valide == filters.valide)

        # Comptage total
        total = query.count()

        # Application de la pagination
        offset = (pagination.page - 1) * pagination.page_size
        items = query.offset(offset).limit(pagination.page_size).all()

        total_pages = (total + pagination.page_size - 1) // pagination.page_size

        return {
            "items": items,
            "total": total,
            "page": pagination.page,
            "page_size": pagination.page_size,
            "total_pages": total_pages
        }


# ============================================================================
# SERVICES STATISTIQUES
# ============================================================================

class StatistiquesService:
    """Service pour les statistiques et rapports"""

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

        # Total des recettes
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

        # Total des dépenses
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

        # Nombre de projets miniers
        nb_projets = (
            db.query(func.count(ProjetMinier.id.distinct()))
            .filter(ProjetMinier.commune_id == commune.id, ProjetMinier.actif == True)
            .scalar()
        )

        # Exercices disponibles
        exercices_disponibles = (
            db.query(Exercice.annee)
            .join(Periode)
            .join(Revenu)
            .filter(Revenu.commune_id == commune.id)
            .distinct()
            .order_by(Exercice.annee.desc())
            .all()
        )

        return {
            "commune": commune,
            "total_recettes": total_recettes,
            "total_depenses": total_depenses,
            "solde": total_recettes - total_depenses,
            "nb_projets_miniers": nb_projets,
            "exercices_disponibles": [ex[0] for ex in exercices_disponibles]
        }

    @staticmethod
    def get_statistiques_region(
        db: Session,
        region_code: str,
        exercice_annee: int
    ) -> Dict[str, Any]:
        """Calcule les statistiques pour une région"""
        region = db.query(Region).filter(Region.code == region_code).first()
        if not region:
            raise ValueError("Région non trouvée")

        # Nombre de communes
        nb_communes = (
            db.query(func.count(Commune.id))
            .filter(Commune.region_id == region.id, Commune.actif == True)
            .scalar()
        )

        # Nombre de projets miniers
        nb_projets = (
            db.query(func.count(ProjetMinier.id))
            .join(Commune)
            .filter(Commune.region_id == region.id, ProjetMinier.actif == True)
            .scalar()
        )

        # Total des revenus miniers
        total_revenus = (
            db.query(func.sum(Revenu.montant))
            .join(Commune)
            .join(Periode)
            .join(Exercice)
            .filter(
                Commune.region_id == region.id,
                Exercice.annee == exercice_annee
            )
            .scalar() or Decimal(0)
        )

        # Top 5 des communes
        communes_top = (
            db.query(
                Commune.nom,
                func.sum(Revenu.montant).label('total')
            )
            .join(Revenu)
            .join(Periode)
            .join(Exercice)
            .filter(
                Commune.region_id == region.id,
                Exercice.annee == exercice_annee
            )
            .group_by(Commune.id, Commune.nom)
            .order_by(func.sum(Revenu.montant).desc())
            .limit(5)
            .all()
        )

        return {
            "region": region,
            "nb_communes": nb_communes,
            "nb_projets_miniers": nb_projets,
            "total_revenus_miniers": total_revenus,
            "communes_top": [
                {"nom": c[0], "total": c[1]}
                for c in communes_top
            ]
        }


# ============================================================================
# SERVICES EXPORT
# ============================================================================

class ExportService:
    """Service pour l'export de données"""

    @staticmethod
    def log_telechargement(
        db: Session,
        type_export: str,
        commune_id: Optional[UUID] = None,
        exercice_id: Optional[UUID] = None,
        utilisateur_id: Optional[UUID] = None,
        ip_adresse: Optional[str] = None,
        user_agent: Optional[str] = None
    ):
        """Enregistre un téléchargement dans les logs"""
        log = LogTelechargement(
            type_export=type_export,
            commune_id=commune_id,
            exercice_id=exercice_id,
            utilisateur_id=utilisateur_id,
            ip_adresse=ip_adresse,
            user_agent=user_agent
        )
        db.add(log)
        db.commit()

    @staticmethod
    def get_statistiques_telechargements(
        db: Session,
        date_debut: Optional[datetime] = None,
        date_fin: Optional[datetime] = None
    ) -> Dict[str, Any]:
        """Récupère les statistiques de téléchargements"""
        query = db.query(
            LogTelechargement.type_export,
            func.count(LogTelechargement.id).label('nb_telechargements')
        )

        if date_debut:
            query = query.filter(LogTelechargement.created_at >= date_debut)

        if date_fin:
            query = query.filter(LogTelechargement.created_at <= date_fin)

        stats = query.group_by(LogTelechargement.type_export).all()

        return {
            "par_type": [
                {"type": s[0], "nombre": s[1]}
                for s in stats
            ],
            "total": sum(s[1] for s in stats)
        }


# Extension de LogActivite pour ajouter une méthode helper
def log_action_helper(
    db: Session,
    utilisateur_id: Optional[UUID],
    action: str,
    entite: str,
    entite_id: UUID,
    anciennes_valeurs: Optional[Dict] = None,
    nouvelles_valeurs: Optional[Dict] = None,
    ip_adresse: Optional[str] = None,
    user_agent: Optional[str] = None
):
    """Helper pour logger une action"""
    log = LogActivite(
        utilisateur_id=utilisateur_id,
        action=action,
        entite=entite,
        entite_id=entite_id,
        anciennes_valeurs=anciennes_valeurs,
        nouvelles_valeurs=nouvelles_valeurs,
        ip_adresse=ip_adresse,
        user_agent=user_agent
    )
    db.add(log)
    db.commit()


# Ajouter la méthode à la classe LogActivite
LogActivite.log_action = staticmethod(log_action_helper)
