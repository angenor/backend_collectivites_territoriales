"""
Exemples de routes FastAPI pour l'API
Ces routes utilisent les services et schémas définis
"""

from fastapi import APIRouter, Depends, HTTPException, Query, Request
from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import UUID

from database import get_db
from schemas import (
    RegionInDB, DepartementInDB, CommuneInDB, CommuneDetail,
    RevenuCreate, RevenuUpdate, RevenuInDB, RevenuDetail, RevenuFilter,
    StatistiquesCommune, StatistiquesRegion,
    TableauCompteAdministratif, PaginationParams, PaginatedResponse
)
from services_examples import (
    CommuneService, RevenuService, StatistiquesService, ExportService
)


# ============================================================================
# ROUTER GÉOGRAPHIQUE
# ============================================================================

router_geo = APIRouter(prefix="/geo", tags=["Géographie"])


@router_geo.get("/regions", response_model=List[RegionInDB])
def get_regions(db: Session = Depends(get_db)):
    """
    Récupère toutes les régions de Madagascar

    Retourne la liste des 22 régions administratives.
    """
    return CommuneService.get_all_regions(db)


@router_geo.get("/regions/{region_code}/departements", response_model=List[DepartementInDB])
def get_departements_by_region(
    region_code: str,
    db: Session = Depends(get_db)
):
    """
    Récupère tous les départements d'une région

    - **region_code**: Code de la région (ex: ANA, ATI, ANO)
    """
    departements = CommuneService.get_departements_by_region(db, region_code)
    if not departements:
        raise HTTPException(status_code=404, detail="Région non trouvée ou sans départements")
    return departements


@router_geo.get("/departements/{departement_code}/communes", response_model=List[CommuneInDB])
def get_communes_by_departement(
    departement_code: str,
    db: Session = Depends(get_db)
):
    """
    Récupère toutes les communes d'un département

    - **departement_code**: Code du département (ex: ANA-01, ATI-02)
    """
    communes = CommuneService.get_communes_by_departement(db, departement_code)
    if not communes:
        raise HTTPException(status_code=404, detail="Département non trouvé ou sans communes")
    return communes


@router_geo.get("/communes/{commune_code}", response_model=CommuneDetail)
def get_commune_detail(
    commune_code: str,
    db: Session = Depends(get_db)
):
    """
    Récupère les détails d'une commune avec sa hiérarchie

    - **commune_code**: Code de la commune (ex: ANO-01-001)

    Retourne la commune avec son département et sa région.
    """
    commune = CommuneService.get_commune_with_hierarchy(db, commune_code)
    if not commune:
        raise HTTPException(status_code=404, detail="Commune non trouvée")
    return commune


@router_geo.get("/communes/search", response_model=List[CommuneInDB])
def search_communes(
    region_code: Optional[str] = Query(None, description="Code de la région"),
    departement_code: Optional[str] = Query(None, description="Code du département"),
    search_term: Optional[str] = Query(None, description="Terme de recherche"),
    db: Session = Depends(get_db)
):
    """
    Recherche de communes avec filtres

    Permet de filtrer par région, département ou recherche textuelle.
    """
    return CommuneService.search_communes(
        db,
        region_code=region_code,
        departement_code=departement_code,
        search_term=search_term
    )


# ============================================================================
# ROUTER REVENUS
# ============================================================================

router_revenus = APIRouter(prefix="/revenus", tags=["Revenus"])


@router_revenus.post("/", response_model=RevenuInDB, status_code=201)
def create_revenu(
    revenu: RevenuCreate,
    db: Session = Depends(get_db)
):
    """
    Crée une nouvelle entrée de revenu

    Calcule automatiquement l'écart et le taux de réalisation si montant_prevu est fourni.
    """
    try:
        return RevenuService.create_revenu(db, revenu)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router_revenus.put("/{revenu_id}", response_model=RevenuInDB)
def update_revenu(
    revenu_id: UUID,
    revenu: RevenuUpdate,
    utilisateur_id: UUID = Query(..., description="ID de l'utilisateur"),
    db: Session = Depends(get_db)
):
    """
    Met à jour un revenu existant

    Recalcule automatiquement l'écart et le taux de réalisation.
    Enregistre l'action dans les logs d'audit.
    """
    try:
        return RevenuService.update_revenu(db, revenu_id, revenu, utilisateur_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router_revenus.get("/commune/{commune_code}", response_model=List[RevenuDetail])
def get_revenus_by_commune(
    commune_code: str,
    exercice_annee: Optional[int] = Query(None, description="Année de l'exercice fiscal"),
    db: Session = Depends(get_db)
):
    """
    Récupère tous les revenus d'une commune

    - **commune_code**: Code de la commune
    - **exercice_annee**: Année de l'exercice (optionnel)
    """
    revenus = RevenuService.get_revenus_by_commune(db, commune_code, exercice_annee)
    if not revenus:
        raise HTTPException(status_code=404, detail="Aucun revenu trouvé pour cette commune")
    return revenus


@router_revenus.post("/search", response_model=PaginatedResponse)
def search_revenus(
    filters: RevenuFilter,
    pagination: PaginationParams = Depends(),
    db: Session = Depends(get_db)
):
    """
    Recherche de revenus avec filtres et pagination

    Permet de filtrer par:
    - commune_code
    - region_code
    - exercice_annee
    - rubrique_code
    - projet_minier_id
    - valide (true/false)
    """
    return RevenuService.search_revenus(db, filters, pagination)


# ============================================================================
# ROUTER TABLEAUX
# ============================================================================

router_tableaux = APIRouter(prefix="/tableaux", tags=["Tableaux Administratifs"])


@router_tableaux.get(
    "/compte-administratif/{commune_code}/{exercice_annee}",
    response_model=TableauCompteAdministratif
)
def get_tableau_compte_administratif(
    commune_code: str,
    exercice_annee: int,
    db: Session = Depends(get_db)
):
    """
    Génère le tableau de compte administratif complet

    - **commune_code**: Code de la commune
    - **exercice_annee**: Année de l'exercice fiscal

    Retourne la structure complète du tableau avec:
    - Informations de la commune et hiérarchie
    - Exercice fiscal
    - Toutes les périodes (trimestres, mois, etc.)
    - Toutes les rubriques hiérarchisées
    - Les données de revenus organisées en pivot
    - Les totaux par rubrique
    """
    try:
        return RevenuService.get_tableau_compte_administratif(
            db, commune_code, exercice_annee
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# ROUTER STATISTIQUES
# ============================================================================

router_stats = APIRouter(prefix="/statistiques", tags=["Statistiques"])


@router_stats.get("/commune/{commune_code}", response_model=StatistiquesCommune)
def get_statistiques_commune(
    commune_code: str,
    exercice_annee: int = Query(..., description="Année de l'exercice"),
    db: Session = Depends(get_db)
):
    """
    Statistiques financières pour une commune

    Retourne:
    - Total des recettes
    - Total des dépenses
    - Solde
    - Nombre de projets miniers
    - Exercices disponibles
    """
    try:
        return StatistiquesService.get_statistiques_commune(
            db, commune_code, exercice_annee
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router_stats.get("/region/{region_code}", response_model=StatistiquesRegion)
def get_statistiques_region(
    region_code: str,
    exercice_annee: int = Query(..., description="Année de l'exercice"),
    db: Session = Depends(get_db)
):
    """
    Statistiques financières pour une région

    Retourne:
    - Nombre de communes
    - Nombre de projets miniers
    - Total des revenus miniers
    - Top 5 des communes par revenus
    """
    try:
        return StatistiquesService.get_statistiques_region(
            db, region_code, exercice_annee
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router_stats.get("/telechargements")
def get_statistiques_telechargements(
    date_debut: Optional[str] = Query(None, description="Date de début (YYYY-MM-DD)"),
    date_fin: Optional[str] = Query(None, description="Date de fin (YYYY-MM-DD)"),
    db: Session = Depends(get_db)
):
    """
    Statistiques des téléchargements

    Retourne le nombre de téléchargements par type (Excel, Word, PDF).
    """
    from datetime import datetime

    date_debut_dt = datetime.fromisoformat(date_debut) if date_debut else None
    date_fin_dt = datetime.fromisoformat(date_fin) if date_fin else None

    return ExportService.get_statistiques_telechargements(
        db, date_debut_dt, date_fin_dt
    )


# ============================================================================
# ROUTER EXPORT
# ============================================================================

router_export = APIRouter(prefix="/export", tags=["Export"])


@router_export.get("/excel/{commune_code}/{exercice_annee}")
def export_excel(
    commune_code: str,
    exercice_annee: int,
    request: Request,
    db: Session = Depends(get_db)
):
    """
    Exporte le tableau de compte administratif en Excel

    **Note**: Cette route doit être complétée avec la logique d'export Excel
    en utilisant openpyxl ou pandas.
    """
    try:
        # Récupération des données
        tableau = RevenuService.get_tableau_compte_administratif(
            db, commune_code, exercice_annee
        )

        # Log du téléchargement
        ExportService.log_telechargement(
            db=db,
            type_export="excel",
            commune_id=tableau["commune"].id,
            exercice_id=tableau["exercice"].id,
            ip_adresse=request.client.host,
            user_agent=request.headers.get("user-agent")
        )

        # TODO: Implémenter la génération du fichier Excel
        # Utiliser openpyxl pour créer le fichier
        # Retourner FileResponse avec le fichier généré

        return {
            "message": "Export Excel en cours de développement",
            "data": tableau
        }

    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router_export.get("/word/{commune_code}/{exercice_annee}")
def export_word(
    commune_code: str,
    exercice_annee: int,
    request: Request,
    db: Session = Depends(get_db)
):
    """
    Exporte le tableau de compte administratif en Word

    **Note**: Cette route doit être complétée avec la logique d'export Word
    en utilisant python-docx.
    """
    try:
        # Récupération des données
        tableau = RevenuService.get_tableau_compte_administratif(
            db, commune_code, exercice_annee
        )

        # Log du téléchargement
        ExportService.log_telechargement(
            db=db,
            type_export="word",
            commune_id=tableau["commune"].id,
            exercice_id=tableau["exercice"].id,
            ip_adresse=request.client.host,
            user_agent=request.headers.get("user-agent")
        )

        # TODO: Implémenter la génération du fichier Word
        # Utiliser python-docx pour créer le fichier
        # Retourner FileResponse avec le fichier généré

        return {
            "message": "Export Word en cours de développement",
            "data": tableau
        }

    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router_export.get("/pdf/{commune_code}/{exercice_annee}")
def export_pdf(
    commune_code: str,
    exercice_annee: int,
    request: Request,
    db: Session = Depends(get_db)
):
    """
    Exporte le tableau de compte administratif en PDF

    **Note**: Cette route doit être complétée avec la logique d'export PDF
    en utilisant reportlab ou weasyprint.
    """
    try:
        # Récupération des données
        tableau = RevenuService.get_tableau_compte_administratif(
            db, commune_code, exercice_annee
        )

        # Log du téléchargement
        ExportService.log_telechargement(
            db=db,
            type_export="pdf",
            commune_id=tableau["commune"].id,
            exercice_id=tableau["exercice"].id,
            ip_adresse=request.client.host,
            user_agent=request.headers.get("user-agent")
        )

        # TODO: Implémenter la génération du fichier PDF
        # Utiliser reportlab pour créer le fichier
        # Retourner FileResponse avec le fichier généré

        return {
            "message": "Export PDF en cours de développement",
            "data": tableau
        }

    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


# ============================================================================
# APPLICATION PRINCIPALE (EXEMPLE)
# ============================================================================

"""
Pour utiliser ces routers dans votre application FastAPI principale:

from fastapi import FastAPI
from api_examples import router_geo, router_revenus, router_tableaux, router_stats, router_export

app = FastAPI(
    title="Plateforme de Suivi des Revenus Miniers",
    description="API pour la gestion des revenus miniers des collectivités territoriales",
    version="1.0.0"
)

# Inclusion des routers
app.include_router(router_geo, prefix="/api/v1")
app.include_router(router_revenus, prefix="/api/v1")
app.include_router(router_tableaux, prefix="/api/v1")
app.include_router(router_stats, prefix="/api/v1")
app.include_router(router_export, prefix="/api/v1")

@app.get("/")
def root():
    return {
        "message": "Bienvenue sur l'API de la Plateforme de Suivi des Revenus Miniers",
        "version": "1.0.0",
        "docs": "/docs"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
"""
