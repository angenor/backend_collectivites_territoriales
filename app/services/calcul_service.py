"""
Service de calcul des totaux et agrégations financières.
Calculs pour les comptes administratifs des collectivités territoriales.
"""

from dataclasses import dataclass
from decimal import Decimal
from typing import Optional

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.comptabilite import DonneesDepenses, DonneesRecettes, Exercice, PlanComptable
from app.models.enums import SectionBudgetaire, TypeMouvement
from app.models.geographie import Commune


@dataclass
class TotauxSection:
    """Totaux pour une section budgétaire."""
    section: SectionBudgetaire
    budget_primitif: Decimal
    budget_supplementaire: Decimal
    prevision_definitive: Decimal
    realisation: Decimal
    reste: Decimal  # reste à recouvrer ou reste à payer
    taux_execution: float


@dataclass
class TotauxGeneraux:
    """Totaux généraux recettes ou dépenses."""
    budget_primitif: Decimal
    budget_supplementaire: Decimal
    prevision_definitive: Decimal
    realisation: Decimal
    reste: Decimal
    taux_execution: float
    par_section: dict[SectionBudgetaire, TotauxSection]


@dataclass
class EquilibreBudgetaire:
    """Équilibre budgétaire global."""
    total_recettes: Decimal
    total_depenses: Decimal
    solde: Decimal
    est_excedentaire: bool
    recettes_fonctionnement: Decimal
    depenses_fonctionnement: Decimal
    solde_fonctionnement: Decimal
    recettes_investissement: Decimal
    depenses_investissement: Decimal
    solde_investissement: Decimal


class CalculService:
    """
    Service pour les calculs financiers des comptes administratifs.
    """

    def calculer_prevision_definitive(
        self,
        budget_primitif: Decimal,
        budget_supplementaire: Decimal,
    ) -> Decimal:
        """
        Calcule la prévision définitive.
        Prévision définitive = Budget primitif + Budget supplémentaire
        """
        bp = budget_primitif or Decimal("0")
        bs = budget_supplementaire or Decimal("0")
        return bp + bs

    def calculer_reste_a_recouvrer(
        self,
        prevision_definitive: Decimal,
        realisation: Decimal,
    ) -> Decimal:
        """
        Calcule le reste à recouvrer pour les recettes.
        Reste à recouvrer = Prévision définitive - Réalisation
        """
        pd = prevision_definitive or Decimal("0")
        real = realisation or Decimal("0")
        return pd - real

    def calculer_reste_a_payer(
        self,
        prevision_definitive: Decimal,
        realisation: Decimal,
    ) -> Decimal:
        """
        Calcule le reste à payer pour les dépenses.
        Reste à payer = Prévision définitive - Réalisation
        """
        pd = prevision_definitive or Decimal("0")
        real = realisation or Decimal("0")
        return pd - real

    def calculer_taux_execution(
        self,
        prevision_definitive: Decimal,
        realisation: Decimal,
    ) -> float:
        """
        Calcule le taux d'exécution budgétaire.
        Taux = (Réalisation / Prévision définitive) * 100
        Retourne 0 si la prévision est nulle.
        """
        pd = prevision_definitive or Decimal("0")
        real = realisation or Decimal("0")

        if pd == Decimal("0"):
            return 0.0

        taux = (real / pd) * 100
        return round(float(taux), 2)

    def agreger_recettes_par_section(
        self,
        db: Session,
        commune_id: int,
        exercice_id: int,
    ) -> dict[SectionBudgetaire, TotauxSection]:
        """
        Agrège les recettes par section budgétaire.
        """
        result = {}

        for section in SectionBudgetaire:
            # Joindre avec le plan comptable pour filtrer par section
            totaux = db.query(
                func.coalesce(func.sum(DonneesRecettes.budget_primitif), 0).label("bp"),
                func.coalesce(func.sum(DonneesRecettes.budget_supplementaire), 0).label("bs"),
                func.coalesce(func.sum(DonneesRecettes.realisation), 0).label("real"),
            ).join(
                PlanComptable,
                DonneesRecettes.compte_code == PlanComptable.code
            ).filter(
                DonneesRecettes.commune_id == commune_id,
                DonneesRecettes.exercice_id == exercice_id,
                PlanComptable.section == section,
            ).first()

            bp = Decimal(str(totaux.bp)) if totaux else Decimal("0")
            bs = Decimal(str(totaux.bs)) if totaux else Decimal("0")
            real = Decimal(str(totaux.real)) if totaux else Decimal("0")
            pd = self.calculer_prevision_definitive(bp, bs)
            reste = self.calculer_reste_a_recouvrer(pd, real)
            taux = self.calculer_taux_execution(pd, real)

            result[section] = TotauxSection(
                section=section,
                budget_primitif=bp,
                budget_supplementaire=bs,
                prevision_definitive=pd,
                realisation=real,
                reste=reste,
                taux_execution=taux,
            )

        return result

    def agreger_depenses_par_section(
        self,
        db: Session,
        commune_id: int,
        exercice_id: int,
    ) -> dict[SectionBudgetaire, TotauxSection]:
        """
        Agrège les dépenses par section budgétaire.
        """
        result = {}

        for section in SectionBudgetaire:
            totaux = db.query(
                func.coalesce(func.sum(DonneesDepenses.budget_primitif), 0).label("bp"),
                func.coalesce(func.sum(DonneesDepenses.budget_supplementaire), 0).label("bs"),
                func.coalesce(func.sum(DonneesDepenses.realisation), 0).label("real"),
            ).join(
                PlanComptable,
                DonneesDepenses.compte_code == PlanComptable.code
            ).filter(
                DonneesDepenses.commune_id == commune_id,
                DonneesDepenses.exercice_id == exercice_id,
                PlanComptable.section == section,
            ).first()

            bp = Decimal(str(totaux.bp)) if totaux else Decimal("0")
            bs = Decimal(str(totaux.bs)) if totaux else Decimal("0")
            real = Decimal(str(totaux.real)) if totaux else Decimal("0")
            pd = self.calculer_prevision_definitive(bp, bs)
            reste = self.calculer_reste_a_payer(pd, real)
            taux = self.calculer_taux_execution(pd, real)

            result[section] = TotauxSection(
                section=section,
                budget_primitif=bp,
                budget_supplementaire=bs,
                prevision_definitive=pd,
                realisation=real,
                reste=reste,
                taux_execution=taux,
            )

        return result

    def calculer_totaux_recettes(
        self,
        db: Session,
        commune_id: int,
        exercice_id: int,
    ) -> TotauxGeneraux:
        """
        Calcule les totaux généraux des recettes.
        """
        par_section = self.agreger_recettes_par_section(db, commune_id, exercice_id)

        bp_total = sum(s.budget_primitif for s in par_section.values())
        bs_total = sum(s.budget_supplementaire for s in par_section.values())
        pd_total = sum(s.prevision_definitive for s in par_section.values())
        real_total = sum(s.realisation for s in par_section.values())
        reste_total = sum(s.reste for s in par_section.values())
        taux = self.calculer_taux_execution(pd_total, real_total)

        return TotauxGeneraux(
            budget_primitif=bp_total,
            budget_supplementaire=bs_total,
            prevision_definitive=pd_total,
            realisation=real_total,
            reste=reste_total,
            taux_execution=taux,
            par_section=par_section,
        )

    def calculer_totaux_depenses(
        self,
        db: Session,
        commune_id: int,
        exercice_id: int,
    ) -> TotauxGeneraux:
        """
        Calcule les totaux généraux des dépenses.
        """
        par_section = self.agreger_depenses_par_section(db, commune_id, exercice_id)

        bp_total = sum(s.budget_primitif for s in par_section.values())
        bs_total = sum(s.budget_supplementaire for s in par_section.values())
        pd_total = sum(s.prevision_definitive for s in par_section.values())
        real_total = sum(s.realisation for s in par_section.values())
        reste_total = sum(s.reste for s in par_section.values())
        taux = self.calculer_taux_execution(pd_total, real_total)

        return TotauxGeneraux(
            budget_primitif=bp_total,
            budget_supplementaire=bs_total,
            prevision_definitive=pd_total,
            realisation=real_total,
            reste=reste_total,
            taux_execution=taux,
            par_section=par_section,
        )

    def calculer_equilibre(
        self,
        db: Session,
        commune_id: int,
        exercice_id: int,
    ) -> EquilibreBudgetaire:
        """
        Calcule l'équilibre budgétaire global.
        """
        recettes = self.calculer_totaux_recettes(db, commune_id, exercice_id)
        depenses = self.calculer_totaux_depenses(db, commune_id, exercice_id)

        total_recettes = recettes.realisation
        total_depenses = depenses.realisation
        solde = total_recettes - total_depenses

        # Fonctionnement
        rec_fonct = recettes.par_section.get(
            SectionBudgetaire.FONCTIONNEMENT,
            TotauxSection(
                section=SectionBudgetaire.FONCTIONNEMENT,
                budget_primitif=Decimal("0"),
                budget_supplementaire=Decimal("0"),
                prevision_definitive=Decimal("0"),
                realisation=Decimal("0"),
                reste=Decimal("0"),
                taux_execution=0.0,
            )
        )
        dep_fonct = depenses.par_section.get(
            SectionBudgetaire.FONCTIONNEMENT,
            TotauxSection(
                section=SectionBudgetaire.FONCTIONNEMENT,
                budget_primitif=Decimal("0"),
                budget_supplementaire=Decimal("0"),
                prevision_definitive=Decimal("0"),
                realisation=Decimal("0"),
                reste=Decimal("0"),
                taux_execution=0.0,
            )
        )

        # Investissement
        rec_invest = recettes.par_section.get(
            SectionBudgetaire.INVESTISSEMENT,
            TotauxSection(
                section=SectionBudgetaire.INVESTISSEMENT,
                budget_primitif=Decimal("0"),
                budget_supplementaire=Decimal("0"),
                prevision_definitive=Decimal("0"),
                realisation=Decimal("0"),
                reste=Decimal("0"),
                taux_execution=0.0,
            )
        )
        dep_invest = depenses.par_section.get(
            SectionBudgetaire.INVESTISSEMENT,
            TotauxSection(
                section=SectionBudgetaire.INVESTISSEMENT,
                budget_primitif=Decimal("0"),
                budget_supplementaire=Decimal("0"),
                prevision_definitive=Decimal("0"),
                realisation=Decimal("0"),
                reste=Decimal("0"),
                taux_execution=0.0,
            )
        )

        return EquilibreBudgetaire(
            total_recettes=total_recettes,
            total_depenses=total_depenses,
            solde=solde,
            est_excedentaire=solde >= Decimal("0"),
            recettes_fonctionnement=rec_fonct.realisation,
            depenses_fonctionnement=dep_fonct.realisation,
            solde_fonctionnement=rec_fonct.realisation - dep_fonct.realisation,
            recettes_investissement=rec_invest.realisation,
            depenses_investissement=dep_invest.realisation,
            solde_investissement=rec_invest.realisation - dep_invest.realisation,
        )

    def calculer_evolution(
        self,
        db: Session,
        commune_id: int,
        annee_debut: int,
        annee_fin: int,
    ) -> list[dict]:
        """
        Calcule l'évolution des finances sur plusieurs exercices.
        """
        evolution = []

        exercices = db.query(Exercice).filter(
            Exercice.annee >= annee_debut,
            Exercice.annee <= annee_fin,
        ).order_by(Exercice.annee).all()

        for exercice in exercices:
            equilibre = self.calculer_equilibre(db, commune_id, exercice.id)
            evolution.append({
                "annee": exercice.annee,
                "recettes": float(equilibre.total_recettes),
                "depenses": float(equilibre.total_depenses),
                "solde": float(equilibre.solde),
                "est_excedentaire": equilibre.est_excedentaire,
            })

        return evolution


# Singleton instance
calcul_service = CalculService()
