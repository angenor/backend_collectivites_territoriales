"""
API v1 Router.
Aggregates all endpoint routers for API version 1.
"""

from fastapi import APIRouter

from app.api.v1.endpoints import (
    auth,
    documents,
    exercices,
    export,
    geo,
    pages,
    projets,
    revenus,
    tableaux,
)
from app.api.v1.endpoints.admin.router import admin_router

api_router = APIRouter()

# Phase 4: Authentication
api_router.include_router(auth.router)

# Phase 5: Public API (Front Office)
api_router.include_router(geo.router)
api_router.include_router(tableaux.router)
api_router.include_router(exercices.router)
api_router.include_router(revenus.router)
api_router.include_router(projets.router)
api_router.include_router(documents.router)
api_router.include_router(pages.router)

# Phase 6: Export API
api_router.include_router(export.router)

# Phase 7: Admin API (Back Office)
api_router.include_router(admin_router)
