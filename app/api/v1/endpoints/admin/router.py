"""
Admin API Router.
Aggregates all admin endpoint routers.
"""

from fastapi import APIRouter

from app.api.v1.endpoints.admin.utilisateurs import router as utilisateurs_router
from app.api.v1.endpoints.admin.donnees import router as donnees_router
from app.api.v1.endpoints.admin.exercices import router as exercices_router
from app.api.v1.endpoints.admin.import_data import router as import_router
from app.api.v1.endpoints.admin.cms import router as cms_router
from app.api.v1.endpoints.admin.upload import router as upload_router
from app.api.v1.endpoints.admin.newsletter import router as newsletter_router
from app.api.v1.endpoints.admin.statistiques import router as statistiques_router

admin_router = APIRouter(prefix="/admin", tags=["Administration"])

# Include all admin sub-routers
admin_router.include_router(utilisateurs_router)
admin_router.include_router(donnees_router)
admin_router.include_router(exercices_router)
admin_router.include_router(import_router)
admin_router.include_router(cms_router)
admin_router.include_router(upload_router)
admin_router.include_router(newsletter_router)
admin_router.include_router(statistiques_router)
