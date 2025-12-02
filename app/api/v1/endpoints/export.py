"""
Export API endpoints.
Generate and download administrative account reports in Excel and Word formats.
"""

from datetime import datetime
from decimal import Decimal
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi.responses import StreamingResponse
from sqlalchemy import func
from sqlalchemy.orm import Session, joinedload

from app.api.deps import get_db
from app.api.v1.endpoints.tableaux import (
    _get_commune_and_exercice,
    _build_recettes_sections,
    _build_depenses_sections,
)
from app.models.comptabilite import (
    DonneesDepenses,
    DonneesRecettes,
    Exercice,
)
from app.models.geographie import Commune, Region
from app.models.enums import SectionBudgetaire
from app.schemas.tableau import (
    LigneEquilibre,
    TableauComplet,
    TableauDepenses,
    TableauEquilibre,
    TableauRecettes,
)
from app.services.export_service import excel_export_service, word_export_service

router = APIRouter(prefix="/export", tags=["Export"])


def _build_tableau_complet(
    db: Session,
    commune_id: int,
    exercice_annee: int
) -> TableauComplet:
    """Build complete financial table for export."""
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

    return TableauComplet(
        commune_id=commune_id,
        commune_nom=commune.nom,
        commune_code=commune.code,
        region_nom=commune.region.nom,
        province_nom=commune.region.province.nom,
        exercice_annee=exercice_annee,
        exercice_cloture=exercice.cloture,
        recettes=tableau_recettes,
        depenses=tableau_depenses,
        equilibre=tableau_equilibre,
        date_generation=datetime.now().isoformat(),
        validee=False
    )


# =====================
# Excel Export Endpoints
# =====================

@router.get(
    "/excel",
    summary="Export Excel complet",
    description="Exporte le tableau complet du compte administratif en Excel.",
    responses={
        200: {
            "content": {"application/vnd.openxmlformats-officedocument.spreadsheetml.sheet": {}},
            "description": "Fichier Excel du compte administratif",
        }
    },
)
async def export_excel_complet(
    commune_id: int = Query(..., description="ID de la commune"),
    exercice_annee: int = Query(..., description="Année de l'exercice"),
    db: Session = Depends(get_db),
):
    """
    Export complete administrative account to Excel.

    Generates an Excel file with three sheets:
    - Recettes (Receipts)
    - Dépenses (Expenses)
    - Équilibre (Budget Balance)

    Returns:
        StreamingResponse with Excel file
    """
    tableau = _build_tableau_complet(db, commune_id, exercice_annee)
    output = excel_export_service.generate_tableau_complet(tableau)

    filename = f"compte_administratif_{tableau.commune_code}_{exercice_annee}.xlsx"

    return StreamingResponse(
        output,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={
            "Content-Disposition": f'attachment; filename="{filename}"',
            "Access-Control-Expose-Headers": "Content-Disposition",
        },
    )


@router.get(
    "/excel/recettes",
    summary="Export Excel recettes",
    description="Exporte uniquement le tableau des recettes en Excel.",
    responses={
        200: {
            "content": {"application/vnd.openxmlformats-officedocument.spreadsheetml.sheet": {}},
            "description": "Fichier Excel des recettes",
        }
    },
)
async def export_excel_recettes(
    commune_id: int = Query(..., description="ID de la commune"),
    exercice_annee: int = Query(..., description="Année de l'exercice"),
    db: Session = Depends(get_db),
):
    """
    Export only receipts table to Excel.

    Returns:
        StreamingResponse with Excel file
    """
    commune, exercice = _get_commune_and_exercice(db, commune_id, exercice_annee)

    sections = _build_recettes_sections(db, commune_id, exercice.id)

    total_prev = sum(s.total_previsions_definitives for s in sections)
    total_or = sum(s.total_or_admis for s in sections)
    total_recouv = sum(s.total_recouvrement for s in sections)
    taux = (total_or / total_prev * 100) if total_prev > 0 else None

    recettes = TableauRecettes(
        commune_id=commune_id,
        commune_nom=commune.nom,
        exercice_annee=exercice_annee,
        sections=sections,
        total_general_previsions=total_prev,
        total_general_or_admis=total_or,
        total_general_recouvrement=total_recouv,
        taux_execution_global=taux
    )

    commune_info = {
        "commune_nom": commune.nom,
        "commune_code": commune.code,
        "region_nom": commune.region.nom,
        "province_nom": commune.region.province.nom,
    }

    output = excel_export_service.generate_recettes_only(recettes, commune_info)

    filename = f"recettes_{commune.code}_{exercice_annee}.xlsx"

    return StreamingResponse(
        output,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={
            "Content-Disposition": f'attachment; filename="{filename}"',
            "Access-Control-Expose-Headers": "Content-Disposition",
        },
    )


@router.get(
    "/excel/depenses",
    summary="Export Excel dépenses",
    description="Exporte uniquement le tableau des dépenses en Excel.",
    responses={
        200: {
            "content": {"application/vnd.openxmlformats-officedocument.spreadsheetml.sheet": {}},
            "description": "Fichier Excel des dépenses",
        }
    },
)
async def export_excel_depenses(
    commune_id: int = Query(..., description="ID de la commune"),
    exercice_annee: int = Query(..., description="Année de l'exercice"),
    db: Session = Depends(get_db),
):
    """
    Export only expenses table to Excel.

    Returns:
        StreamingResponse with Excel file
    """
    commune, exercice = _get_commune_and_exercice(db, commune_id, exercice_annee)

    sections = _build_depenses_sections(db, commune_id, exercice.id)

    total_prev = sum(s.total_previsions_definitives for s in sections)
    total_mandat = sum(s.total_mandat_admis for s in sections)
    total_paiement = sum(s.total_paiement for s in sections)
    taux = (total_mandat / total_prev * 100) if total_prev > 0 else None

    depenses = TableauDepenses(
        commune_id=commune_id,
        commune_nom=commune.nom,
        exercice_annee=exercice_annee,
        sections=sections,
        total_general_previsions=total_prev,
        total_general_mandat_admis=total_mandat,
        total_general_paiement=total_paiement,
        taux_execution_global=taux
    )

    commune_info = {
        "commune_nom": commune.nom,
        "commune_code": commune.code,
        "region_nom": commune.region.nom,
        "province_nom": commune.region.province.nom,
    }

    output = excel_export_service.generate_depenses_only(depenses, commune_info)

    filename = f"depenses_{commune.code}_{exercice_annee}.xlsx"

    return StreamingResponse(
        output,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={
            "Content-Disposition": f'attachment; filename="{filename}"',
            "Access-Control-Expose-Headers": "Content-Disposition",
        },
    )


# =====================
# Word Export Endpoint
# =====================

@router.get(
    "/word",
    summary="Export Word complet",
    description="Exporte le tableau complet du compte administratif en Word.",
    responses={
        200: {
            "content": {"application/vnd.openxmlformats-officedocument.wordprocessingml.document": {}},
            "description": "Fichier Word du compte administratif",
        }
    },
)
async def export_word_complet(
    commune_id: int = Query(..., description="ID de la commune"),
    exercice_annee: int = Query(..., description="Année de l'exercice"),
    db: Session = Depends(get_db),
):
    """
    Export complete administrative account to Word.

    Generates a Word document with:
    - Header information (commune, region, year)
    - Receipts table (summarized)
    - Expenses table (summarized)
    - Budget balance table

    Returns:
        StreamingResponse with Word file
    """
    tableau = _build_tableau_complet(db, commune_id, exercice_annee)
    output = word_export_service.generate_tableau_complet(tableau)

    filename = f"compte_administratif_{tableau.commune_code}_{exercice_annee}.docx"

    return StreamingResponse(
        output,
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        headers={
            "Content-Disposition": f'attachment; filename="{filename}"',
            "Access-Control-Expose-Headers": "Content-Disposition",
        },
    )
