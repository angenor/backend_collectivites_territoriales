"""
Pydantic schemas for financial tables display.
Structures for administrative accounts presentation.
"""

from decimal import Decimal
from typing import List, Optional

from pydantic import Field

from app.models.enums import SectionBudgetaire
from app.schemas.base import BaseSchema


# =====================
# Ligne de tableau
# =====================

class LigneTableauBase(BaseSchema):
    """Base schema for a table row."""
    code: str
    intitule: str
    niveau: int = Field(..., ge=1, le=3)
    est_sommable: bool = True


class LigneRecettes(LigneTableauBase):
    """Row for receipts table."""
    budget_primitif: Decimal = Field(default=Decimal("0.00"))
    budget_additionnel: Decimal = Field(default=Decimal("0.00"))
    modifications: Decimal = Field(default=Decimal("0.00"))
    previsions_definitives: Decimal = Field(default=Decimal("0.00"))
    or_admis: Decimal = Field(default=Decimal("0.00"))
    recouvrement: Decimal = Field(default=Decimal("0.00"))
    reste_a_recouvrer: Decimal = Field(default=Decimal("0.00"))
    taux_execution: Optional[Decimal] = None


class LigneDepenses(LigneTableauBase):
    """Row for expenses table."""
    budget_primitif: Decimal = Field(default=Decimal("0.00"))
    budget_additionnel: Decimal = Field(default=Decimal("0.00"))
    modifications: Decimal = Field(default=Decimal("0.00"))
    previsions_definitives: Decimal = Field(default=Decimal("0.00"))
    engagement: Decimal = Field(default=Decimal("0.00"))
    mandat_admis: Decimal = Field(default=Decimal("0.00"))
    paiement: Decimal = Field(default=Decimal("0.00"))
    reste_a_payer: Decimal = Field(default=Decimal("0.00"))
    taux_execution: Optional[Decimal] = None


# =====================
# Section de tableau
# =====================

class SectionTableauRecettes(BaseSchema):
    """Section of receipts table (fonctionnement or investissement)."""
    section: SectionBudgetaire
    titre: str
    lignes: List[LigneRecettes] = []
    # Totals
    total_budget_primitif: Decimal = Field(default=Decimal("0.00"))
    total_budget_additionnel: Decimal = Field(default=Decimal("0.00"))
    total_modifications: Decimal = Field(default=Decimal("0.00"))
    total_previsions_definitives: Decimal = Field(default=Decimal("0.00"))
    total_or_admis: Decimal = Field(default=Decimal("0.00"))
    total_recouvrement: Decimal = Field(default=Decimal("0.00"))
    total_reste_a_recouvrer: Decimal = Field(default=Decimal("0.00"))
    taux_execution_global: Optional[Decimal] = None


class SectionTableauDepenses(BaseSchema):
    """Section of expenses table (fonctionnement or investissement)."""
    section: SectionBudgetaire
    titre: str
    lignes: List[LigneDepenses] = []
    # Totals
    total_budget_primitif: Decimal = Field(default=Decimal("0.00"))
    total_budget_additionnel: Decimal = Field(default=Decimal("0.00"))
    total_modifications: Decimal = Field(default=Decimal("0.00"))
    total_previsions_definitives: Decimal = Field(default=Decimal("0.00"))
    total_engagement: Decimal = Field(default=Decimal("0.00"))
    total_mandat_admis: Decimal = Field(default=Decimal("0.00"))
    total_paiement: Decimal = Field(default=Decimal("0.00"))
    total_reste_a_payer: Decimal = Field(default=Decimal("0.00"))
    taux_execution_global: Optional[Decimal] = None


# =====================
# Tableaux complets
# =====================

class TableauRecettes(BaseSchema):
    """Complete receipts table with both sections."""
    commune_id: int
    commune_nom: str
    exercice_annee: int
    sections: List[SectionTableauRecettes] = []
    # Grand totals
    total_general_previsions: Decimal = Field(default=Decimal("0.00"))
    total_general_or_admis: Decimal = Field(default=Decimal("0.00"))
    total_general_recouvrement: Decimal = Field(default=Decimal("0.00"))
    taux_execution_global: Optional[Decimal] = None


class TableauDepenses(BaseSchema):
    """Complete expenses table with both sections."""
    commune_id: int
    commune_nom: str
    exercice_annee: int
    sections: List[SectionTableauDepenses] = []
    # Grand totals
    total_general_previsions: Decimal = Field(default=Decimal("0.00"))
    total_general_mandat_admis: Decimal = Field(default=Decimal("0.00"))
    total_general_paiement: Decimal = Field(default=Decimal("0.00"))
    taux_execution_global: Optional[Decimal] = None


# =====================
# Équilibre budgétaire
# =====================

class LigneEquilibre(BaseSchema):
    """Row for balance table."""
    libelle: str
    section: Optional[SectionBudgetaire] = None
    recettes_previsions: Decimal = Field(default=Decimal("0.00"))
    recettes_realisations: Decimal = Field(default=Decimal("0.00"))
    depenses_previsions: Decimal = Field(default=Decimal("0.00"))
    depenses_realisations: Decimal = Field(default=Decimal("0.00"))
    solde_previsions: Decimal = Field(default=Decimal("0.00"))
    solde_realisations: Decimal = Field(default=Decimal("0.00"))


class TableauEquilibre(BaseSchema):
    """Budget balance table."""
    commune_id: int
    commune_nom: str
    exercice_annee: int
    lignes: List[LigneEquilibre] = []
    # Section fonctionnement
    fonctionnement_recettes_prev: Decimal = Field(default=Decimal("0.00"))
    fonctionnement_recettes_real: Decimal = Field(default=Decimal("0.00"))
    fonctionnement_depenses_prev: Decimal = Field(default=Decimal("0.00"))
    fonctionnement_depenses_real: Decimal = Field(default=Decimal("0.00"))
    fonctionnement_solde_prev: Decimal = Field(default=Decimal("0.00"))
    fonctionnement_solde_real: Decimal = Field(default=Decimal("0.00"))
    # Section investissement
    investissement_recettes_prev: Decimal = Field(default=Decimal("0.00"))
    investissement_recettes_real: Decimal = Field(default=Decimal("0.00"))
    investissement_depenses_prev: Decimal = Field(default=Decimal("0.00"))
    investissement_depenses_real: Decimal = Field(default=Decimal("0.00"))
    investissement_solde_prev: Decimal = Field(default=Decimal("0.00"))
    investissement_solde_real: Decimal = Field(default=Decimal("0.00"))
    # Totaux généraux
    total_recettes_prev: Decimal = Field(default=Decimal("0.00"))
    total_recettes_real: Decimal = Field(default=Decimal("0.00"))
    total_depenses_prev: Decimal = Field(default=Decimal("0.00"))
    total_depenses_real: Decimal = Field(default=Decimal("0.00"))
    total_solde_prev: Decimal = Field(default=Decimal("0.00"))
    total_solde_real: Decimal = Field(default=Decimal("0.00"))


# =====================
# Tableau complet combiné
# =====================

class TableauComplet(BaseSchema):
    """Complete administrative account with all tables."""
    commune_id: int
    commune_nom: str
    commune_code: str
    region_nom: str
    province_nom: str
    exercice_annee: int
    exercice_cloture: bool
    # Tables
    recettes: TableauRecettes
    depenses: TableauDepenses
    equilibre: TableauEquilibre
    # Metadata
    date_generation: Optional[str] = None
    validee: bool = False


# =====================
# Résumé et statistiques
# =====================

class ResumeFinancier(BaseSchema):
    """Financial summary for a commune/year."""
    commune_id: int
    exercice_annee: int
    total_recettes_prevues: Decimal
    total_recettes_realisees: Decimal
    total_depenses_prevues: Decimal
    total_depenses_realisees: Decimal
    solde_budgetaire: Decimal
    taux_execution_recettes: Optional[Decimal] = None
    taux_execution_depenses: Optional[Decimal] = None


class ComparaisonExercices(BaseSchema):
    """Comparison between two fiscal years."""
    commune_id: int
    commune_nom: str
    exercice_annee_1: int
    exercice_annee_2: int
    # Recettes
    recettes_annee_1: Decimal
    recettes_annee_2: Decimal
    variation_recettes: Decimal
    variation_recettes_pct: Optional[Decimal] = None
    # Depenses
    depenses_annee_1: Decimal
    depenses_annee_2: Decimal
    variation_depenses: Decimal
    variation_depenses_pct: Optional[Decimal] = None


class StatistiquesRegion(BaseSchema):
    """Aggregated statistics for a region."""
    region_id: int
    region_nom: str
    exercice_annee: int
    nb_communes: int
    total_recettes: Decimal
    total_depenses: Decimal
    moyenne_recettes_commune: Decimal
    moyenne_depenses_commune: Decimal
    taux_execution_moyen: Optional[Decimal] = None
