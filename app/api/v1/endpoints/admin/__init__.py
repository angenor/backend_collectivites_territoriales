"""
Admin API endpoints.
Protected routes requiring authentication.
"""

from app.api.v1.endpoints.admin.utilisateurs import router as utilisateurs_router
from app.api.v1.endpoints.admin.donnees import router as donnees_router
from app.api.v1.endpoints.admin.exercices import router as exercices_router
from app.api.v1.endpoints.admin.import_data import router as import_router
from app.api.v1.endpoints.admin.cms import router as cms_router
from app.api.v1.endpoints.admin.upload import router as upload_router

__all__ = [
    "utilisateurs_router",
    "donnees_router",
    "exercices_router",
    "import_router",
    "cms_router",
    "upload_router",
]
