"""
Aggregation de tous les routers API v1
"""

from fastapi import APIRouter

from app.api.v1.endpoints import geographie, revenus, utilisateurs, export

api_router = APIRouter()

# Inclusion des routers
api_router.include_router(geographie.router, prefix="/geo", tags=["Géographie"])
api_router.include_router(revenus.router, prefix="/revenus", tags=["Revenus"])
api_router.include_router(utilisateurs.router, prefix="/auth", tags=["Authentification"])
api_router.include_router(export.router, prefix="/export", tags=["Export"])
