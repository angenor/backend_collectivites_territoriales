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
from app.services.export_service import ExportService
from app.api.deps import get_current_active_user
from app.models.utilisateurs import Utilisateur

router = APIRouter()


def create_excel_response(data: Dict[str, Any], filename: str = "tableau_revenus.xlsx") -> StreamingResponse:
    """
    Cree un fichier Excel a partir des donnees du tableau

    Args:
        data: Dictionnaire contenant les donnees du tableau
        filename: Nom du fichier a telecharger

    Returns:
        StreamingResponse avec le fichier Excel

    Raises:
        HTTPException: Si openpyxl n'est pas installe ou en cas d'erreur
    """
    try:
        output = ExportService.generate_excel(data)

        return StreamingResponse(
            output,
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={
                "Content-Disposition": f"attachment; filename={filename}"
            }
        )
    except ImportError as e:
        raise HTTPException(
            status_code=501,
            detail="Les bibliotheques d'export Excel ne sont pas installees. Installez-les avec: pip install openpyxl"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de l'export Excel: {str(e)}")


def create_word_response(data: Dict[str, Any], filename: str = "tableau_revenus.docx") -> StreamingResponse:
    """
    Cree un fichier Word a partir des donnees du tableau

    Args:
        data: Dictionnaire contenant les donnees du tableau
        filename: Nom du fichier a telecharger

    Returns:
        StreamingResponse avec le fichier Word

    Raises:
        HTTPException: Si python-docx n'est pas installe ou en cas d'erreur
    """
    try:
        output = ExportService.generate_word(data)

        return StreamingResponse(
            output,
            media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            headers={
                "Content-Disposition": f"attachment; filename={filename}"
            }
        )
    except ImportError as e:
        raise HTTPException(
            status_code=501,
            detail="Les bibliotheques d'export Word ne sont pas installees. Installez-les avec: pip install python-docx"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de l'export Word: {str(e)}")


def create_pdf_response(data: Dict[str, Any], filename: str = "tableau_revenus.pdf") -> StreamingResponse:
    """
    Cree un fichier PDF a partir des donnees du tableau

    Args:
        data: Dictionnaire contenant les donnees du tableau
        filename: Nom du fichier a telecharger

    Returns:
        StreamingResponse avec le fichier PDF

    Raises:
        HTTPException: Si reportlab n'est pas installe ou en cas d'erreur
    """
    try:
        output = ExportService.generate_pdf(data)

        return StreamingResponse(
            output,
            media_type="application/pdf",
            headers={
                "Content-Disposition": f"attachment; filename={filename}"
            }
        )
    except ImportError as e:
        raise HTTPException(
            status_code=501,
            detail="Les bibliotheques d'export PDF ne sont pas installees. Installez-les avec: pip install reportlab"
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
    - **exercice_annee**: Annee de l'exercice fiscal

    Retourne un fichier Excel telechargeable
    """
    try:
        # Recuperation des donnees
        tableau = RevenuService.get_tableau_compte_administratif(
            db, commune_code, exercice_annee
        )

        # Generer un nom de fichier descriptif
        commune_nom = tableau["commune"].nom.replace(" ", "_")
        filename = f"compte_administratif_{commune_nom}_{exercice_annee}.xlsx"

        # TODO: Logger le telechargement
        # ExportService.log_telechargement(...)

        return create_excel_response(tableau, filename)

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
    - **exercice_annee**: Annee de l'exercice fiscal

    Retourne un fichier Word telechargeable
    """
    try:
        # Recuperation des donnees
        tableau = RevenuService.get_tableau_compte_administratif(
            db, commune_code, exercice_annee
        )

        # Generer un nom de fichier descriptif
        commune_nom = tableau["commune"].nom.replace(" ", "_")
        filename = f"compte_administratif_{commune_nom}_{exercice_annee}.docx"

        return create_word_response(tableau, filename)

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
    - **exercice_annee**: Annee de l'exercice fiscal

    Retourne un fichier PDF telechargeable
    """
    try:
        # Recuperation des donnees
        tableau = RevenuService.get_tableau_compte_administratif(
            db, commune_code, exercice_annee
        )

        # Generer un nom de fichier descriptif
        commune_nom = tableau["commune"].nom.replace(" ", "_")
        filename = f"compte_administratif_{commune_nom}_{exercice_annee}.pdf"

        return create_pdf_response(tableau, filename)

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
