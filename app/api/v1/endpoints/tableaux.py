"""
Financial tables API endpoints.
Administrative accounts data presentation (recettes, depenses, equilibre).
"""

from decimal import Decimal
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import func
from sqlalchemy.orm import Session, joinedload

from app.api.deps import DbSession, get_db
from app.models.comptabilite import (
    DonneesDepenses,
    DonneesRecettes,
    Exercice,
    PlanComptable,
)
from app.models.geographie import Commune, Region
from app.models.enums import SectionBudgetaire, TypeMouvement
from app.schemas.tableau import (
    ComparaisonExercices,
    LigneDepenses,
    LigneEquilibre,
    LigneRecettes,
    ResumeFinancier,
    SectionTableauDepenses,
    SectionTableauRecettes,
    StatistiquesRegion,
    TableauComplet,
    TableauDepenses,
    TableauEquilibre,
    TableauRecettes,
)

router = APIRouter(prefix="/tableaux", tags=["Tableaux"])


def _aggregate_parent_values_recettes(lignes: list[LigneRecettes]) -> list[LigneRecettes]:
    """
    Agrège les valeurs des enfants vers les parents.
    Les parents (niveau 1 et 2) cumulent les valeurs de leurs enfants directs.
    """
    # Créer un dictionnaire par code pour accès rapide
    lignes_by_code = {l.code: l for l in lignes}

    # Trier par niveau décroissant pour agréger du bas vers le haut
    sorted_codes = sorted(lignes_by_code.keys(), key=len, reverse=True)

    for code in sorted_codes:
        ligne = lignes_by_code[code]

        # Trouver le parent (code sans le dernier caractère)
        if len(code) > 2:
            parent_code = code[:-1]
            if parent_code in lignes_by_code:
                parent = lignes_by_code[parent_code]

                # Vérifier si c'est un enfant direct (un seul niveau de différence)
                if parent.niveau == ligne.niveau - 1:
                    # Agréger les valeurs
                    parent.budget_primitif = (parent.budget_primitif or Decimal("0")) + (ligne.budget_primitif or Decimal("0"))
                    parent.budget_additionnel = (parent.budget_additionnel or Decimal("0")) + (ligne.budget_additionnel or Decimal("0"))
                    parent.modifications = (parent.modifications or Decimal("0")) + (ligne.modifications or Decimal("0"))
                    parent.previsions_definitives = (parent.previsions_definitives or Decimal("0")) + (ligne.previsions_definitives or Decimal("0"))
                    parent.or_admis = (parent.or_admis or Decimal("0")) + (ligne.or_admis or Decimal("0"))
                    parent.recouvrement = (parent.recouvrement or Decimal("0")) + (ligne.recouvrement or Decimal("0"))
                    parent.reste_a_recouvrer = (parent.reste_a_recouvrer or Decimal("0")) + (ligne.reste_a_recouvrer or Decimal("0"))

    # Recalculer les taux d'exécution pour les parents
    for ligne in lignes:
        if ligne.niveau < 3 and ligne.previsions_definitives and ligne.previsions_definitives > 0:
            ligne.taux_execution = (ligne.or_admis / ligne.previsions_definitives * 100) if ligne.or_admis else None

    return lignes


def _aggregate_parent_values_depenses(lignes: list[LigneDepenses]) -> list[LigneDepenses]:
    """
    Agrège les valeurs des enfants vers les parents pour les dépenses.
    Les parents (niveau 1 et 2) cumulent les valeurs de leurs enfants directs.
    """
    # Créer un dictionnaire par code pour accès rapide
    lignes_by_code = {l.code: l for l in lignes}

    # Trier par niveau décroissant pour agréger du bas vers le haut
    sorted_codes = sorted(lignes_by_code.keys(), key=len, reverse=True)

    for code in sorted_codes:
        ligne = lignes_by_code[code]

        # Trouver le parent (code sans le dernier caractère)
        if len(code) > 2:
            parent_code = code[:-1]
            if parent_code in lignes_by_code:
                parent = lignes_by_code[parent_code]

                # Vérifier si c'est un enfant direct (un seul niveau de différence)
                if parent.niveau == ligne.niveau - 1:
                    # Agréger les valeurs
                    parent.budget_primitif = (parent.budget_primitif or Decimal("0")) + (ligne.budget_primitif or Decimal("0"))
                    parent.budget_additionnel = (parent.budget_additionnel or Decimal("0")) + (ligne.budget_additionnel or Decimal("0"))
                    parent.modifications = (parent.modifications or Decimal("0")) + (ligne.modifications or Decimal("0"))
                    parent.previsions_definitives = (parent.previsions_definitives or Decimal("0")) + (ligne.previsions_definitives or Decimal("0"))
                    parent.engagement = (parent.engagement or Decimal("0")) + (ligne.engagement or Decimal("0"))
                    parent.mandat_admis = (parent.mandat_admis or Decimal("0")) + (ligne.mandat_admis or Decimal("0"))
                    parent.paiement = (parent.paiement or Decimal("0")) + (ligne.paiement or Decimal("0"))
                    parent.reste_a_payer = (parent.reste_a_payer or Decimal("0")) + (ligne.reste_a_payer or Decimal("0"))

    # Recalculer les taux d'exécution pour les parents
    for ligne in lignes:
        if ligne.niveau < 3 and ligne.previsions_definitives and ligne.previsions_definitives > 0:
            ligne.taux_execution = (ligne.mandat_admis / ligne.previsions_definitives * 100) if ligne.mandat_admis else None

    return lignes


def _get_commune_and_exercice(
    db: Session,
    commune_id: int,
    exercice_annee: int
) -> tuple[Commune, Exercice]:
    """Helper to get commune and exercice, raising 404 if not found."""
    commune = db.query(Commune).options(
        joinedload(Commune.region).joinedload(Region.province)
    ).filter(Commune.id == commune_id).first()

    if not commune:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Commune non trouvée"
        )

    exercice = db.query(Exercice).filter(
        Exercice.annee == exercice_annee
    ).first()

    if not exercice:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Exercice {exercice_annee} non trouvé"
        )

    return commune, exercice


def _build_recettes_sections(
    db: Session,
    commune_id: int,
    exercice_id: int
) -> list[SectionTableauRecettes]:
    """Build receipts sections with data."""
    sections = []

    for section_type in [SectionBudgetaire.FONCTIONNEMENT, SectionBudgetaire.INVESTISSEMENT]:
        # Get plan comptable entries for this section (receipts)
        comptes = db.query(PlanComptable).filter(
            PlanComptable.type_mouvement == TypeMouvement.RECETTE,
            PlanComptable.section == section_type,
            PlanComptable.actif == True
        ).order_by(PlanComptable.ordre_affichage, PlanComptable.code).all()

        lignes = []
        totals = {
            'budget_primitif': Decimal("0.00"),
            'budget_additionnel': Decimal("0.00"),
            'modifications': Decimal("0.00"),
            'previsions_definitives': Decimal("0.00"),
            'or_admis': Decimal("0.00"),
            'recouvrement': Decimal("0.00"),
            'reste_a_recouvrer': Decimal("0.00"),
        }

        for compte in comptes:
            # Get data for this compte
            donnee = db.query(DonneesRecettes).filter(
                DonneesRecettes.commune_id == commune_id,
                DonneesRecettes.exercice_id == exercice_id,
                DonneesRecettes.compte_code == compte.code
            ).first()

            if donnee:
                prev_def = donnee.previsions_definitives or donnee.previsions_calculees
                taux = (donnee.or_admis / prev_def * 100) if prev_def > 0 else None

                ligne = LigneRecettes(
                    code=compte.code,
                    intitule=compte.intitule,
                    niveau=compte.niveau,
                    est_sommable=compte.est_sommable,
                    budget_primitif=donnee.budget_primitif,
                    budget_additionnel=donnee.budget_additionnel,
                    modifications=donnee.modifications,
                    previsions_definitives=prev_def,
                    or_admis=donnee.or_admis,
                    recouvrement=donnee.recouvrement,
                    reste_a_recouvrer=donnee.reste_a_recouvrer,
                    taux_execution=taux
                )
                lignes.append(ligne)
            else:
                # No data for this compte, include with zeros
                ligne = LigneRecettes(
                    code=compte.code,
                    intitule=compte.intitule,
                    niveau=compte.niveau,
                    est_sommable=compte.est_sommable,
                )
                lignes.append(ligne)

        # Agréger les valeurs des enfants vers les parents
        lignes = _aggregate_parent_values_recettes(lignes)

        # Calculer les totaux à partir des lignes de niveau 1 (après agrégation)
        for ligne in lignes:
            if ligne.niveau == 1 and ligne.est_sommable:
                totals['budget_primitif'] += ligne.budget_primitif or Decimal("0")
                totals['budget_additionnel'] += ligne.budget_additionnel or Decimal("0")
                totals['modifications'] += ligne.modifications or Decimal("0")
                totals['previsions_definitives'] += ligne.previsions_definitives or Decimal("0")
                totals['or_admis'] += ligne.or_admis or Decimal("0")
                totals['recouvrement'] += ligne.recouvrement or Decimal("0")
                totals['reste_a_recouvrer'] += ligne.reste_a_recouvrer or Decimal("0")

        # Calculate global execution rate
        taux_global = None
        if totals['previsions_definitives'] > 0:
            taux_global = totals['or_admis'] / totals['previsions_definitives'] * 100

        titre = "SECTION DE FONCTIONNEMENT" if section_type == SectionBudgetaire.FONCTIONNEMENT else "SECTION D'INVESTISSEMENT"

        sections.append(SectionTableauRecettes(
            section=section_type,
            titre=titre,
            lignes=lignes,
            total_budget_primitif=totals['budget_primitif'],
            total_budget_additionnel=totals['budget_additionnel'],
            total_modifications=totals['modifications'],
            total_previsions_definitives=totals['previsions_definitives'],
            total_or_admis=totals['or_admis'],
            total_recouvrement=totals['recouvrement'],
            total_reste_a_recouvrer=totals['reste_a_recouvrer'],
            taux_execution_global=taux_global
        ))

    return sections


def _build_depenses_sections(
    db: Session,
    commune_id: int,
    exercice_id: int
) -> list[SectionTableauDepenses]:
    """Build expenses sections with data."""
    sections = []

    for section_type in [SectionBudgetaire.FONCTIONNEMENT, SectionBudgetaire.INVESTISSEMENT]:
        # Get plan comptable entries for this section (expenses)
        comptes = db.query(PlanComptable).filter(
            PlanComptable.type_mouvement == TypeMouvement.DEPENSE,
            PlanComptable.section == section_type,
            PlanComptable.actif == True
        ).order_by(PlanComptable.ordre_affichage, PlanComptable.code).all()

        lignes = []
        totals = {
            'budget_primitif': Decimal("0.00"),
            'budget_additionnel': Decimal("0.00"),
            'modifications': Decimal("0.00"),
            'previsions_definitives': Decimal("0.00"),
            'engagement': Decimal("0.00"),
            'mandat_admis': Decimal("0.00"),
            'paiement': Decimal("0.00"),
            'reste_a_payer': Decimal("0.00"),
        }

        for compte in comptes:
            # Get data for this compte
            donnee = db.query(DonneesDepenses).filter(
                DonneesDepenses.commune_id == commune_id,
                DonneesDepenses.exercice_id == exercice_id,
                DonneesDepenses.compte_code == compte.code
            ).first()

            if donnee:
                prev_def = donnee.previsions_definitives or donnee.previsions_calculees
                taux = (donnee.mandat_admis / prev_def * 100) if prev_def > 0 else None

                ligne = LigneDepenses(
                    code=compte.code,
                    intitule=compte.intitule,
                    niveau=compte.niveau,
                    est_sommable=compte.est_sommable,
                    budget_primitif=donnee.budget_primitif,
                    budget_additionnel=donnee.budget_additionnel,
                    modifications=donnee.modifications,
                    previsions_definitives=prev_def,
                    engagement=donnee.engagement,
                    mandat_admis=donnee.mandat_admis,
                    paiement=donnee.paiement,
                    reste_a_payer=donnee.reste_a_payer,
                    taux_execution=taux
                )
                lignes.append(ligne)
            else:
                # No data for this compte, include with zeros
                ligne = LigneDepenses(
                    code=compte.code,
                    intitule=compte.intitule,
                    niveau=compte.niveau,
                    est_sommable=compte.est_sommable,
                )
                lignes.append(ligne)

        # Agréger les valeurs des enfants vers les parents
        lignes = _aggregate_parent_values_depenses(lignes)

        # Calculer les totaux à partir des lignes de niveau 1 (après agrégation)
        for ligne in lignes:
            if ligne.niveau == 1 and ligne.est_sommable:
                totals['budget_primitif'] += ligne.budget_primitif or Decimal("0")
                totals['budget_additionnel'] += ligne.budget_additionnel or Decimal("0")
                totals['modifications'] += ligne.modifications or Decimal("0")
                totals['previsions_definitives'] += ligne.previsions_definitives or Decimal("0")
                totals['engagement'] += ligne.engagement or Decimal("0")
                totals['mandat_admis'] += ligne.mandat_admis or Decimal("0")
                totals['paiement'] += ligne.paiement or Decimal("0")
                totals['reste_a_payer'] += ligne.reste_a_payer or Decimal("0")

        # Calculate global execution rate
        taux_global = None
        if totals['previsions_definitives'] > 0:
            taux_global = totals['mandat_admis'] / totals['previsions_definitives'] * 100

        titre = "SECTION DE FONCTIONNEMENT" if section_type == SectionBudgetaire.FONCTIONNEMENT else "SECTION D'INVESTISSEMENT"

        sections.append(SectionTableauDepenses(
            section=section_type,
            titre=titre,
            lignes=lignes,
            total_budget_primitif=totals['budget_primitif'],
            total_budget_additionnel=totals['budget_additionnel'],
            total_modifications=totals['modifications'],
            total_previsions_definitives=totals['previsions_definitives'],
            total_engagement=totals['engagement'],
            total_mandat_admis=totals['mandat_admis'],
            total_paiement=totals['paiement'],
            total_reste_a_payer=totals['reste_a_payer'],
            taux_execution_global=taux_global
        ))

    return sections


# =====================
# Main Endpoints
# =====================

@router.get(
    "",
    response_model=TableauComplet,
    summary="Tableau complet",
    description="Retourne le tableau complet du compte administratif (recettes, dépenses, équilibre)."
)
async def get_tableau_complet(
    commune_id: int = Query(..., description="ID de la commune"),
    exercice_annee: int = Query(..., description="Année de l'exercice"),
    db: Session = Depends(get_db),
):
    """
    Get the complete administrative account table.

    Includes receipts, expenses, and budget balance tables.
    """
    commune, exercice = _get_commune_and_exercice(db, commune_id, exercice_annee)

    # Build sections
    recettes_sections = _build_recettes_sections(db, commune_id, exercice.id)
    depenses_sections = _build_depenses_sections(db, commune_id, exercice.id)

    # Calculate totals for recettes
    total_recettes_prev = sum(s.total_previsions_definitives for s in recettes_sections)
    total_recettes_or = sum(s.total_or_admis for s in recettes_sections)
    total_recettes_recouv = sum(s.total_recouvrement for s in recettes_sections)

    # Calculate totals for depenses
    total_depenses_prev = sum(s.total_previsions_definitives for s in depenses_sections)
    total_depenses_mandat = sum(s.total_mandat_admis for s in depenses_sections)
    total_depenses_paiement = sum(s.total_paiement for s in depenses_sections)

    # Build recettes table
    taux_recettes = (total_recettes_or / total_recettes_prev * 100) if total_recettes_prev > 0 else None
    tableau_recettes = TableauRecettes(
        commune_id=commune_id,
        commune_nom=commune.nom,
        exercice_annee=exercice_annee,
        sections=recettes_sections,
        total_general_previsions=total_recettes_prev,
        total_general_or_admis=total_recettes_or,
        total_general_recouvrement=total_recettes_recouv,
        taux_execution_global=taux_recettes
    )

    # Build depenses table
    taux_depenses = (total_depenses_mandat / total_depenses_prev * 100) if total_depenses_prev > 0 else None
    tableau_depenses = TableauDepenses(
        commune_id=commune_id,
        commune_nom=commune.nom,
        exercice_annee=exercice_annee,
        sections=depenses_sections,
        total_general_previsions=total_depenses_prev,
        total_general_mandat_admis=total_depenses_mandat,
        total_general_paiement=total_depenses_paiement,
        taux_execution_global=taux_depenses
    )

    # Build equilibre table
    fonct_recettes = recettes_sections[0] if recettes_sections else None
    fonct_depenses = depenses_sections[0] if depenses_sections else None
    invest_recettes = recettes_sections[1] if len(recettes_sections) > 1 else None
    invest_depenses = depenses_sections[1] if len(depenses_sections) > 1 else None

    fonct_r_prev = fonct_recettes.total_previsions_definitives if fonct_recettes else Decimal("0.00")
    fonct_r_real = fonct_recettes.total_or_admis if fonct_recettes else Decimal("0.00")
    fonct_d_prev = fonct_depenses.total_previsions_definitives if fonct_depenses else Decimal("0.00")
    fonct_d_real = fonct_depenses.total_mandat_admis if fonct_depenses else Decimal("0.00")

    invest_r_prev = invest_recettes.total_previsions_definitives if invest_recettes else Decimal("0.00")
    invest_r_real = invest_recettes.total_or_admis if invest_recettes else Decimal("0.00")
    invest_d_prev = invest_depenses.total_previsions_definitives if invest_depenses else Decimal("0.00")
    invest_d_real = invest_depenses.total_mandat_admis if invest_depenses else Decimal("0.00")

    lignes_equilibre = [
        LigneEquilibre(
            libelle="Section de fonctionnement",
            section=SectionBudgetaire.FONCTIONNEMENT,
            recettes_previsions=fonct_r_prev,
            recettes_realisations=fonct_r_real,
            depenses_previsions=fonct_d_prev,
            depenses_realisations=fonct_d_real,
            solde_previsions=fonct_r_prev - fonct_d_prev,
            solde_realisations=fonct_r_real - fonct_d_real,
        ),
        LigneEquilibre(
            libelle="Section d'investissement",
            section=SectionBudgetaire.INVESTISSEMENT,
            recettes_previsions=invest_r_prev,
            recettes_realisations=invest_r_real,
            depenses_previsions=invest_d_prev,
            depenses_realisations=invest_d_real,
            solde_previsions=invest_r_prev - invest_d_prev,
            solde_realisations=invest_r_real - invest_d_real,
        ),
        LigneEquilibre(
            libelle="TOTAL GÉNÉRAL",
            section=None,
            recettes_previsions=total_recettes_prev,
            recettes_realisations=total_recettes_or,
            depenses_previsions=total_depenses_prev,
            depenses_realisations=total_depenses_mandat,
            solde_previsions=total_recettes_prev - total_depenses_prev,
            solde_realisations=total_recettes_or - total_depenses_mandat,
        ),
    ]

    tableau_equilibre = TableauEquilibre(
        commune_id=commune_id,
        commune_nom=commune.nom,
        exercice_annee=exercice_annee,
        lignes=lignes_equilibre,
        fonctionnement_recettes_prev=fonct_r_prev,
        fonctionnement_recettes_real=fonct_r_real,
        fonctionnement_depenses_prev=fonct_d_prev,
        fonctionnement_depenses_real=fonct_d_real,
        fonctionnement_solde_prev=fonct_r_prev - fonct_d_prev,
        fonctionnement_solde_real=fonct_r_real - fonct_d_real,
        investissement_recettes_prev=invest_r_prev,
        investissement_recettes_real=invest_r_real,
        investissement_depenses_prev=invest_d_prev,
        investissement_depenses_real=invest_d_real,
        investissement_solde_prev=invest_r_prev - invest_d_prev,
        investissement_solde_real=invest_r_real - invest_d_real,
        total_recettes_prev=total_recettes_prev,
        total_recettes_real=total_recettes_or,
        total_depenses_prev=total_depenses_prev,
        total_depenses_real=total_depenses_mandat,
        total_solde_prev=total_recettes_prev - total_depenses_prev,
        total_solde_real=total_recettes_or - total_depenses_mandat,
    )

    from datetime import datetime
    return TableauComplet(
        commune_id=commune_id,
        commune_nom=commune.nom,
        commune_code=commune.code,
        region_nom=commune.region.nom,
        province_nom=commune.region.province.nom,
        exercice_id=exercice.id,
        exercice_annee=exercice_annee,
        exercice_cloture=exercice.cloture,
        recettes=tableau_recettes,
        depenses=tableau_depenses,
        equilibre=tableau_equilibre,
        date_generation=datetime.now().isoformat(),
        validee=False  # TODO: check if all data is validated
    )


@router.get(
    "/recettes",
    response_model=TableauRecettes,
    summary="Tableau des recettes",
    description="Retourne uniquement le tableau des recettes."
)
async def get_tableau_recettes(
    commune_id: int = Query(..., description="ID de la commune"),
    exercice_annee: int = Query(..., description="Année de l'exercice"),
    db: Session = Depends(get_db),
):
    """
    Get only the receipts table.
    """
    commune, exercice = _get_commune_and_exercice(db, commune_id, exercice_annee)

    sections = _build_recettes_sections(db, commune_id, exercice.id)

    total_prev = sum(s.total_previsions_definitives for s in sections)
    total_or = sum(s.total_or_admis for s in sections)
    total_recouv = sum(s.total_recouvrement for s in sections)
    taux = (total_or / total_prev * 100) if total_prev > 0 else None

    return TableauRecettes(
        commune_id=commune_id,
        commune_nom=commune.nom,
        exercice_annee=exercice_annee,
        sections=sections,
        total_general_previsions=total_prev,
        total_general_or_admis=total_or,
        total_general_recouvrement=total_recouv,
        taux_execution_global=taux
    )


@router.get(
    "/depenses",
    response_model=TableauDepenses,
    summary="Tableau des dépenses",
    description="Retourne uniquement le tableau des dépenses."
)
async def get_tableau_depenses(
    commune_id: int = Query(..., description="ID de la commune"),
    exercice_annee: int = Query(..., description="Année de l'exercice"),
    db: Session = Depends(get_db),
):
    """
    Get only the expenses table.
    """
    commune, exercice = _get_commune_and_exercice(db, commune_id, exercice_annee)

    sections = _build_depenses_sections(db, commune_id, exercice.id)

    total_prev = sum(s.total_previsions_definitives for s in sections)
    total_mandat = sum(s.total_mandat_admis for s in sections)
    total_paiement = sum(s.total_paiement for s in sections)
    taux = (total_mandat / total_prev * 100) if total_prev > 0 else None

    return TableauDepenses(
        commune_id=commune_id,
        commune_nom=commune.nom,
        exercice_annee=exercice_annee,
        sections=sections,
        total_general_previsions=total_prev,
        total_general_mandat_admis=total_mandat,
        total_general_paiement=total_paiement,
        taux_execution_global=taux
    )


@router.get(
    "/equilibre",
    response_model=TableauEquilibre,
    summary="Tableau d'équilibre",
    description="Retourne uniquement le tableau d'équilibre budgétaire."
)
async def get_tableau_equilibre(
    commune_id: int = Query(..., description="ID de la commune"),
    exercice_annee: int = Query(..., description="Année de l'exercice"),
    db: Session = Depends(get_db),
):
    """
    Get only the budget balance table.
    """
    commune, exercice = _get_commune_and_exercice(db, commune_id, exercice_annee)

    recettes_sections = _build_recettes_sections(db, commune_id, exercice.id)
    depenses_sections = _build_depenses_sections(db, commune_id, exercice.id)

    # Get section totals
    fonct_recettes = recettes_sections[0] if recettes_sections else None
    fonct_depenses = depenses_sections[0] if depenses_sections else None
    invest_recettes = recettes_sections[1] if len(recettes_sections) > 1 else None
    invest_depenses = depenses_sections[1] if len(depenses_sections) > 1 else None

    fonct_r_prev = fonct_recettes.total_previsions_definitives if fonct_recettes else Decimal("0.00")
    fonct_r_real = fonct_recettes.total_or_admis if fonct_recettes else Decimal("0.00")
    fonct_d_prev = fonct_depenses.total_previsions_definitives if fonct_depenses else Decimal("0.00")
    fonct_d_real = fonct_depenses.total_mandat_admis if fonct_depenses else Decimal("0.00")

    invest_r_prev = invest_recettes.total_previsions_definitives if invest_recettes else Decimal("0.00")
    invest_r_real = invest_recettes.total_or_admis if invest_recettes else Decimal("0.00")
    invest_d_prev = invest_depenses.total_previsions_definitives if invest_depenses else Decimal("0.00")
    invest_d_real = invest_depenses.total_mandat_admis if invest_depenses else Decimal("0.00")

    total_r_prev = fonct_r_prev + invest_r_prev
    total_r_real = fonct_r_real + invest_r_real
    total_d_prev = fonct_d_prev + invest_d_prev
    total_d_real = fonct_d_real + invest_d_real

    lignes = [
        LigneEquilibre(
            libelle="Section de fonctionnement",
            section=SectionBudgetaire.FONCTIONNEMENT,
            recettes_previsions=fonct_r_prev,
            recettes_realisations=fonct_r_real,
            depenses_previsions=fonct_d_prev,
            depenses_realisations=fonct_d_real,
            solde_previsions=fonct_r_prev - fonct_d_prev,
            solde_realisations=fonct_r_real - fonct_d_real,
        ),
        LigneEquilibre(
            libelle="Section d'investissement",
            section=SectionBudgetaire.INVESTISSEMENT,
            recettes_previsions=invest_r_prev,
            recettes_realisations=invest_r_real,
            depenses_previsions=invest_d_prev,
            depenses_realisations=invest_d_real,
            solde_previsions=invest_r_prev - invest_d_prev,
            solde_realisations=invest_r_real - invest_d_real,
        ),
        LigneEquilibre(
            libelle="TOTAL GÉNÉRAL",
            section=None,
            recettes_previsions=total_r_prev,
            recettes_realisations=total_r_real,
            depenses_previsions=total_d_prev,
            depenses_realisations=total_d_real,
            solde_previsions=total_r_prev - total_d_prev,
            solde_realisations=total_r_real - total_d_real,
        ),
    ]

    return TableauEquilibre(
        commune_id=commune_id,
        commune_nom=commune.nom,
        exercice_annee=exercice_annee,
        lignes=lignes,
        fonctionnement_recettes_prev=fonct_r_prev,
        fonctionnement_recettes_real=fonct_r_real,
        fonctionnement_depenses_prev=fonct_d_prev,
        fonctionnement_depenses_real=fonct_d_real,
        fonctionnement_solde_prev=fonct_r_prev - fonct_d_prev,
        fonctionnement_solde_real=fonct_r_real - fonct_d_real,
        investissement_recettes_prev=invest_r_prev,
        investissement_recettes_real=invest_r_real,
        investissement_depenses_prev=invest_d_prev,
        investissement_depenses_real=invest_d_real,
        investissement_solde_prev=invest_r_prev - invest_d_prev,
        investissement_solde_real=invest_r_real - invest_d_real,
        total_recettes_prev=total_r_prev,
        total_recettes_real=total_r_real,
        total_depenses_prev=total_d_prev,
        total_depenses_real=total_d_real,
        total_solde_prev=total_r_prev - total_d_prev,
        total_solde_real=total_r_real - total_d_real,
    )


# =====================
# Summary/Statistics Endpoints
# =====================

@router.get(
    "/resume",
    response_model=ResumeFinancier,
    summary="Résumé financier",
    description="Retourne un résumé financier simplifié pour une commune/exercice."
)
async def get_resume_financier(
    commune_id: int = Query(..., description="ID de la commune"),
    exercice_annee: int = Query(..., description="Année de l'exercice"),
    db: Session = Depends(get_db),
):
    """
    Get a simplified financial summary for a commune/year.
    """
    commune, exercice = _get_commune_and_exercice(db, commune_id, exercice_annee)

    # Sum recettes
    recettes_totals = db.query(
        func.sum(DonneesRecettes.previsions_definitives).label("prevues"),
        func.sum(DonneesRecettes.or_admis).label("realisees"),
    ).filter(
        DonneesRecettes.commune_id == commune_id,
        DonneesRecettes.exercice_id == exercice.id
    ).first()

    # Sum depenses
    depenses_totals = db.query(
        func.sum(DonneesDepenses.previsions_definitives).label("prevues"),
        func.sum(DonneesDepenses.mandat_admis).label("realisees"),
    ).filter(
        DonneesDepenses.commune_id == commune_id,
        DonneesDepenses.exercice_id == exercice.id
    ).first()

    recettes_prev = recettes_totals.prevues or Decimal("0.00")
    recettes_real = recettes_totals.realisees or Decimal("0.00")
    depenses_prev = depenses_totals.prevues or Decimal("0.00")
    depenses_real = depenses_totals.realisees or Decimal("0.00")

    taux_recettes = (recettes_real / recettes_prev * 100) if recettes_prev > 0 else None
    taux_depenses = (depenses_real / depenses_prev * 100) if depenses_prev > 0 else None

    return ResumeFinancier(
        commune_id=commune_id,
        exercice_annee=exercice_annee,
        total_recettes_prevues=recettes_prev,
        total_recettes_realisees=recettes_real,
        total_depenses_prevues=depenses_prev,
        total_depenses_realisees=depenses_real,
        solde_budgetaire=recettes_real - depenses_real,
        taux_execution_recettes=taux_recettes,
        taux_execution_depenses=taux_depenses
    )


@router.get(
    "/comparaison",
    response_model=ComparaisonExercices,
    summary="Comparaison entre exercices",
    description="Compare les données financières entre deux exercices."
)
async def get_comparaison_exercices(
    commune_id: int = Query(..., description="ID de la commune"),
    annee_1: int = Query(..., description="Première année"),
    annee_2: int = Query(..., description="Deuxième année"),
    db: Session = Depends(get_db),
):
    """
    Compare financial data between two fiscal years.
    """
    commune = db.query(Commune).filter(Commune.id == commune_id).first()
    if not commune:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Commune non trouvée"
        )

    exercice_1 = db.query(Exercice).filter(Exercice.annee == annee_1).first()
    exercice_2 = db.query(Exercice).filter(Exercice.annee == annee_2).first()

    if not exercice_1 or not exercice_2:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Un ou plusieurs exercices non trouvés"
        )

    def get_totals(exercice_id: int):
        recettes = db.query(
            func.sum(DonneesRecettes.or_admis)
        ).filter(
            DonneesRecettes.commune_id == commune_id,
            DonneesRecettes.exercice_id == exercice_id
        ).scalar() or Decimal("0.00")

        depenses = db.query(
            func.sum(DonneesDepenses.mandat_admis)
        ).filter(
            DonneesDepenses.commune_id == commune_id,
            DonneesDepenses.exercice_id == exercice_id
        ).scalar() or Decimal("0.00")

        return recettes, depenses

    recettes_1, depenses_1 = get_totals(exercice_1.id)
    recettes_2, depenses_2 = get_totals(exercice_2.id)

    var_recettes = recettes_2 - recettes_1
    var_depenses = depenses_2 - depenses_1

    var_recettes_pct = (var_recettes / recettes_1 * 100) if recettes_1 > 0 else None
    var_depenses_pct = (var_depenses / depenses_1 * 100) if depenses_1 > 0 else None

    return ComparaisonExercices(
        commune_id=commune_id,
        commune_nom=commune.nom,
        exercice_annee_1=annee_1,
        exercice_annee_2=annee_2,
        recettes_annee_1=recettes_1,
        recettes_annee_2=recettes_2,
        variation_recettes=var_recettes,
        variation_recettes_pct=var_recettes_pct,
        depenses_annee_1=depenses_1,
        depenses_annee_2=depenses_2,
        variation_depenses=var_depenses,
        variation_depenses_pct=var_depenses_pct
    )


@router.get(
    "/statistiques/region/{region_id}",
    response_model=StatistiquesRegion,
    summary="Statistiques régionales",
    description="Retourne les statistiques agrégées pour une région."
)
async def get_statistiques_region(
    region_id: int,
    exercice_annee: int = Query(..., description="Année de l'exercice"),
    db: Session = Depends(get_db),
):
    """
    Get aggregated statistics for a region.
    """
    region = db.query(Region).filter(Region.id == region_id).first()
    if not region:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Région non trouvée"
        )

    exercice = db.query(Exercice).filter(Exercice.annee == exercice_annee).first()
    if not exercice:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Exercice {exercice_annee} non trouvé"
        )

    # Get communes in this region
    communes = db.query(Commune).filter(Commune.region_id == region_id).all()
    commune_ids = [c.id for c in communes]

    if not commune_ids:
        return StatistiquesRegion(
            region_id=region_id,
            region_nom=region.nom,
            exercice_annee=exercice_annee,
            nb_communes=0,
            total_recettes=Decimal("0.00"),
            total_depenses=Decimal("0.00"),
            moyenne_recettes_commune=Decimal("0.00"),
            moyenne_depenses_commune=Decimal("0.00"),
            taux_execution_moyen=None
        )

    # Aggregate recettes
    total_recettes = db.query(
        func.sum(DonneesRecettes.or_admis)
    ).filter(
        DonneesRecettes.commune_id.in_(commune_ids),
        DonneesRecettes.exercice_id == exercice.id
    ).scalar() or Decimal("0.00")

    # Aggregate depenses
    total_depenses = db.query(
        func.sum(DonneesDepenses.mandat_admis)
    ).filter(
        DonneesDepenses.commune_id.in_(commune_ids),
        DonneesDepenses.exercice_id == exercice.id
    ).scalar() or Decimal("0.00")

    # Aggregate previsions for execution rate
    total_prev_recettes = db.query(
        func.sum(DonneesRecettes.previsions_definitives)
    ).filter(
        DonneesRecettes.commune_id.in_(commune_ids),
        DonneesRecettes.exercice_id == exercice.id
    ).scalar() or Decimal("0.00")

    nb_communes = len(communes)
    moyenne_recettes = total_recettes / nb_communes if nb_communes > 0 else Decimal("0.00")
    moyenne_depenses = total_depenses / nb_communes if nb_communes > 0 else Decimal("0.00")
    taux_execution = (total_recettes / total_prev_recettes * 100) if total_prev_recettes > 0 else None

    return StatistiquesRegion(
        region_id=region_id,
        region_nom=region.nom,
        exercice_annee=exercice_annee,
        nb_communes=nb_communes,
        total_recettes=total_recettes,
        total_depenses=total_depenses,
        moyenne_recettes_commune=moyenne_recettes,
        moyenne_depenses_commune=moyenne_depenses,
        taux_execution_moyen=taux_execution
    )
