"""
Admin API endpoints for data import.
Import financial data from Excel files.
"""

from fastapi import APIRouter, Depends, File, HTTPException, Query, UploadFile, status
from sqlalchemy.orm import Session

from app.api.deps import CurrentEditor, get_db
from app.models.comptabilite import Exercice
from app.models.geographie import Commune
from app.services.import_service import ExcelImportService

router = APIRouter(prefix="/import", tags=["Admin - Import"])


@router.post(
    "/excel",
    response_model=dict,
    summary="Importer depuis Excel",
    description="Importe les données financières depuis un fichier Excel.",
)
async def import_excel(
    commune_id: int = Query(..., description="ID de la commune"),
    exercice_id: int = Query(..., description="ID de l'exercice"),
    file: UploadFile = File(..., description="Fichier Excel (.xlsx)"),
    update_existing: bool = Query(
        True, description="Mettre à jour les entrées existantes"
    ),
    current_user: CurrentEditor = None,
    db: Session = Depends(get_db),
):
    """
    Import financial data from Excel file.

    The Excel file should contain sheets named "Recettes" and/or "Dépenses"
    with columns matching the standard administrative account format:

    **Recettes columns:**
    - A: Code comptable
    - B: Intitulé
    - C: Budget Primitif
    - D: Budget Additionnel
    - E: Modifications
    - F: Prévisions Définitives
    - G: OR Admis
    - H: Recouvrement
    - I: Reste à Recouvrer

    **Dépenses columns:**
    - A: Code comptable
    - B: Intitulé
    - C: Budget Primitif
    - D: Budget Additionnel
    - E: Modifications
    - F: Prévisions Définitives
    - G: Engagement
    - H: Mandat Admis
    - I: Paiement
    - J: Reste à Payer

    Returns:
        Import result with counts of imported/updated entries
    """
    # Validate file type
    if not file.filename.endswith((".xlsx", ".xls")):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Le fichier doit être au format Excel (.xlsx ou .xls)",
        )

    # Validate file size (max 10MB)
    content = await file.read()
    if len(content) > 10 * 1024 * 1024:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Le fichier est trop volumineux (max 10MB)",
        )

    # Import service
    import_service = ExcelImportService(db)

    # First validate
    validation_result = import_service.validate_file(content, commune_id, exercice_id)
    if not validation_result.success:
        return {
            "success": False,
            "message": "Erreurs de validation",
            "errors": [
                {
                    "row": e.row,
                    "column": e.column,
                    "message": e.message,
                    "value": str(e.value) if e.value else None,
                }
                for e in validation_result.errors
            ],
        }

    # Import data
    result = import_service.import_file(
        content, commune_id, exercice_id, update_existing
    )

    return {
        "success": result.success,
        "message": "Import réussi" if result.success else "Import échoué",
        "recettes_imported": result.recettes_imported,
        "recettes_updated": result.recettes_updated,
        "depenses_imported": result.depenses_imported,
        "depenses_updated": result.depenses_updated,
        "total_imported": result.recettes_imported + result.depenses_imported,
        "total_updated": result.recettes_updated + result.depenses_updated,
        "errors": [
            {
                "row": e.row,
                "column": e.column,
                "message": e.message,
                "value": str(e.value) if e.value else None,
            }
            for e in result.errors
        ]
        if result.errors
        else [],
    }


@router.post(
    "/excel/validate",
    response_model=dict,
    summary="Valider un fichier Excel",
    description="Valide un fichier Excel sans importer les données.",
)
async def validate_excel(
    commune_id: int = Query(..., description="ID de la commune"),
    exercice_id: int = Query(..., description="ID de l'exercice"),
    file: UploadFile = File(..., description="Fichier Excel (.xlsx)"),
    current_user: CurrentEditor = None,
    db: Session = Depends(get_db),
):
    """
    Validate an Excel file without importing.

    Use this to check for errors before performing the actual import.
    """
    if not file.filename.endswith((".xlsx", ".xls")):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Le fichier doit être au format Excel (.xlsx ou .xls)",
        )

    content = await file.read()
    if len(content) > 10 * 1024 * 1024:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Le fichier est trop volumineux (max 10MB)",
        )

    import_service = ExcelImportService(db)
    result = import_service.validate_file(content, commune_id, exercice_id)

    return {
        "valid": result.success,
        "message": "Fichier valide" if result.success else "Erreurs détectées",
        "errors": [
            {
                "row": e.row,
                "column": e.column,
                "message": e.message,
                "value": str(e.value) if e.value else None,
            }
            for e in result.errors
        ],
    }


@router.get(
    "/template",
    response_model=dict,
    summary="Info template Excel",
    description="Retourne les informations sur le format du template Excel attendu.",
)
async def get_import_template_info(
    current_user: CurrentEditor = None,
):
    """
    Get information about the expected Excel template format.
    """
    return {
        "format": "xlsx",
        "sheets": [
            {
                "name": "Recettes",
                "columns": [
                    {"col": "A", "name": "Code", "required": True},
                    {"col": "B", "name": "Intitulé", "required": False},
                    {"col": "C", "name": "Budget Primitif", "required": False},
                    {"col": "D", "name": "Budget Additionnel", "required": False},
                    {"col": "E", "name": "Modifications", "required": False},
                    {"col": "F", "name": "Prévisions Définitives", "required": False},
                    {"col": "G", "name": "OR Admis", "required": False},
                    {"col": "H", "name": "Recouvrement", "required": False},
                    {"col": "I", "name": "Reste à Recouvrer", "required": False},
                ],
            },
            {
                "name": "Dépenses",
                "columns": [
                    {"col": "A", "name": "Code", "required": True},
                    {"col": "B", "name": "Intitulé", "required": False},
                    {"col": "C", "name": "Budget Primitif", "required": False},
                    {"col": "D", "name": "Budget Additionnel", "required": False},
                    {"col": "E", "name": "Modifications", "required": False},
                    {"col": "F", "name": "Prévisions Définitives", "required": False},
                    {"col": "G", "name": "Engagement", "required": False},
                    {"col": "H", "name": "Mandat Admis", "required": False},
                    {"col": "I", "name": "Paiement", "required": False},
                    {"col": "J", "name": "Reste à Payer", "required": False},
                ],
            },
        ],
        "notes": [
            "Le fichier peut contenir une ou deux feuilles (Recettes et/ou Dépenses)",
            "Les codes comptables doivent correspondre au plan comptable en base",
            "Les valeurs numériques peuvent être formatées avec ou sans séparateurs",
            "Les lignes avec un code vide sont ignorées",
        ],
    }
