"""
Application FastAPI principale
Point d'entrée de l'application
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.core.config import settings
from app.core.logger import setup_logging
from app.api.v1.api import api_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Gestion du cycle de vie de l'application"""
    # Startup
    setup_logging()
    yield
    # Shutdown
    pass


# Création de l'application FastAPI
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="API pour la gestion des revenus miniers des collectivités territoriales de Madagascar",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    lifespan=lifespan
)

# Configuration CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclusion du router API v1
app.include_router(api_router, prefix=settings.API_V1_STR)


# Routes de base
@app.get("/")
def root():
    """Route racine"""
    return {
        "message": "Bienvenue sur l'API de la Plateforme de Suivi des Revenus Miniers",
        "version": settings.APP_VERSION,
        "docs": "/docs",
        "redoc": "/redoc",
        "environment": settings.ENVIRONMENT
    }


@app.get("/health")
def health_check():
    """Health check pour monitoring"""
    return {
        "status": "healthy",
        "version": settings.APP_VERSION,
        "environment": settings.ENVIRONMENT
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG
    )
