"""
API v1 Router.
Aggregates all endpoint routers for API version 1.
"""

from fastapi import APIRouter

from app.api.v1.endpoints import auth

api_router = APIRouter()

# Phase 4: Authentication
api_router.include_router(auth.router)

# Phase 5: Public API (Front Office)
# api_router.include_router(geo.router, prefix="/geo", tags=["Géographie"])
# api_router.include_router(tableaux.router, prefix="/tableaux", tags=["Tableaux"])
# api_router.include_router(exercices.router, prefix="/exercices", tags=["Exercices"])
# api_router.include_router(revenus.router, prefix="/revenus", tags=["Revenus Miniers"])
# api_router.include_router(projets.router, prefix="/projets", tags=["Projets Miniers"])
# api_router.include_router(documents.router, prefix="/documents", tags=["Documents"])
# api_router.include_router(pages.router, prefix="/pages", tags=["Pages CMS"])

# Phase 6: Export API
# api_router.include_router(export.router, prefix="/export", tags=["Export"])

# Phase 7: Admin API (Back Office)
# api_router.include_router(admin_router, prefix="/admin", tags=["Administration"])
