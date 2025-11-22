"""
Configuration de la base de données SQLAlchemy
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.pool import NullPool
from typing import Generator

from app.core.config import settings

# Création du moteur SQLAlchemy
engine = create_engine(
    settings.DATABASE_URL,
    poolclass=NullPool,  # Pas de pool pour éviter les problèmes de connexion
    echo=settings.DEBUG,  # Log SQL si DEBUG=True
    future=True,
)

# Session locale
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    future=True,
)

# Base pour les modèles
Base = declarative_base()


def get_db() -> Generator:
    """
    Dependency pour obtenir une session de base de données

    Usage dans FastAPI:
        @app.get("/items/")
        def read_items(db: Session = Depends(get_db)):
            items = db.query(Item).all()
            return items
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db() -> None:
    """
    Initialise la base de données en créant toutes les tables
    Note: En production, utiliser Alembic pour les migrations
    """
    Base.metadata.create_all(bind=engine)


def drop_db() -> None:
    """
    Supprime toutes les tables de la base de données
    ATTENTION: À utiliser uniquement en développement!
    """
    Base.metadata.drop_all(bind=engine)
