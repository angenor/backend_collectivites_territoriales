"""
Endpoints pour l'export de données (Excel, Word, PDF)
"""

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from io import BytesIO
from typing import Dict, Any

from app.database import get_db
from app.services.revenu_service import RevenuService
from app.api.deps import get_current_active_user
from app.models.utilisateurs import Utilisateur

router = APIRouter()


def create_excel_response(data: Dict[str, Any]) -> StreamingResponse:
    """
    Crée un fichier Excel à partir des données du tableau

    Note: Nécessite openpyxl (pip install openpyxl)
    Pour l'instant, retourne un placeholder
    """
    try:
        # TODO: Implémenter avec openpyxl
        # from openpyxl import Workbook
        # wb = Workbook()
        # ws = wb.active
        # ... remplir le fichier

        # Placeholder
        output = BytesIO()
        output.write(b"Excel export - To be implemented with openpyxl")
        output.seek(0)

        return StreamingResponse(
            output,
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={
                "Content-Disposition": f"attachment; filename=tableau_revenus.xlsx"
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de l'export Excel: {str(e)}")


def create_word_response(data: Dict[str, Any]) -> StreamingResponse:
    """
    Crée un fichier Word à partir des données du tableau

    Note: Nécessite python-docx (pip install python-docx)
    Pour l'instant, retourne un placeholder
    """
    try:
        # TODO: Implémenter avec python-docx
        # from docx import Document
        # doc = Document()
        # ... remplir le document

        # Placeholder
        output = BytesIO()
        output.write(b"Word export - To be implemented with python-docx")
        output.seek(0)

        return StreamingResponse(
            output,
            media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            headers={
                "Content-Disposition": f"attachment; filename=tableau_revenus.docx"
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de l'export Word: {str(e)}")


def create_pdf_response(data: Dict[str, Any]) -> StreamingResponse:
    """
    Crée un fichier PDF à partir des données du tableau

    Note: Nécessite reportlab (pip install reportlab)
    Pour l'instant, retourne un placeholder
    """
    try:
        # TODO: Implémenter avec reportlab
        # from reportlab.lib.pagesizes import A4, landscape
        # from reportlab.pdfgen import canvas
        # ... générer le PDF

        # Placeholder
        output = BytesIO()
        output.write(b"PDF export - To be implemented with reportlab")
        output.seek(0)

        return StreamingResponse(
            output,
            media_type="application/pdf",
            headers={
                "Content-Disposition": f"attachment; filename=tableau_revenus.pdf"
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de l'export PDF: {str(e)}")


@router.get(
    "/excel/{commune_code}/{exercice_annee}",
    summary="Export Excel du tableau de compte administratif"
)
def export_excel(
    commune_code: str,
    exercice_annee: int,
    request: Request,
    db: Session = Depends(get_db),
    current_user: Utilisateur = Depends(get_current_active_user)
):
    """
    Exporte le tableau de compte administratif en Excel

    - **commune_code**: Code de la commune
    - **exercice_annee**: Année de l'exercice fiscal

    Retourne un fichier Excel téléchargeable
    """
    try:
        # Récupération des données
        tableau = RevenuService.get_tableau_compte_administratif(
            db, commune_code, exercice_annee
        )

        # TODO: Logger le téléchargement
        # ExportService.log_telechargement(...)

        return create_excel_response(tableau)

    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get(
    "/word/{commune_code}/{exercice_annee}",
    summary="Export Word du tableau de compte administratif"
)
def export_word(
    commune_code: str,
    exercice_annee: int,
    request: Request,
    db: Session = Depends(get_db),
    current_user: Utilisateur = Depends(get_current_active_user)
):
    """
    Exporte le tableau de compte administratif en Word

    - **commune_code**: Code de la commune
    - **exercice_annee**: Année de l'exercice fiscal

    Retourne un fichier Word téléchargeable
    """
    try:
        # Récupération des données
        tableau = RevenuService.get_tableau_compte_administratif(
            db, commune_code, exercice_annee
        )

        return create_word_response(tableau)

    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get(
    "/pdf/{commune_code}/{exercice_annee}",
    summary="Export PDF du tableau de compte administratif"
)
def export_pdf(
    commune_code: str,
    exercice_annee: int,
    request: Request,
    db: Session = Depends(get_db),
    current_user: Utilisateur = Depends(get_current_active_user)
):
    """
    Exporte le tableau de compte administratif en PDF

    - **commune_code**: Code de la commune
    - **exercice_annee**: Année de l'exercice fiscal

    Retourne un fichier PDF téléchargeable
    """
    try:
        # Récupération des données
        tableau = RevenuService.get_tableau_compte_administratif(
            db, commune_code, exercice_annee
        )

        return create_pdf_response(tableau)

    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/formats", summary="Liste des formats d'export disponibles")
def get_export_formats():
    """
    Retourne la liste des formats d'export disponibles
    """
    return {
        "formats": [
            {
                "name": "Excel",
                "extension": ".xlsx",
                "mime_type": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                "endpoint": "/api/v1/export/excel/{commune_code}/{exercice_annee}"
            },
            {
                "name": "Word",
                "extension": ".docx",
                "mime_type": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                "endpoint": "/api/v1/export/word/{commune_code}/{exercice_annee}"
            },
            {
                "name": "PDF",
                "extension": ".pdf",
                "mime_type": "application/pdf",
                "endpoint": "/api/v1/export/pdf/{commune_code}/{exercice_annee}"
            }
        ]
    }
