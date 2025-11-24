"""
Aggregation de tous les routers API v1
"""

from fastapi import APIRouter

from app.api.v1.endpoints import geographie, revenus, utilisateurs, export, roles, projets_miniers, exercices, documents, import_excel, rubriques

api_router = APIRouter()

# Inclusion des routers
api_router.include_router(geographie.router, prefix="/geo", tags=["Géographie"])
api_router.include_router(revenus.router, prefix="/revenus", tags=["Revenus"])
api_router.include_router(utilisateurs.router, prefix="/auth", tags=["Authentification"])
api_router.include_router(roles.router, prefix="/roles", tags=["Rôles"])
api_router.include_router(projets_miniers.router, prefix="/projets-miniers", tags=["Projets Miniers"])
api_router.include_router(exercices.router, prefix="/exercices", tags=["Exercices & Périodes"])
api_router.include_router(rubriques.router, prefix="/rubriques", tags=["Rubriques"])
api_router.include_router(documents.router, prefix="/documents", tags=["Documents"])
api_router.include_router(import_excel.router, prefix="/import", tags=["Import"])
api_router.include_router(export.router, prefix="/export", tags=["Export"])
