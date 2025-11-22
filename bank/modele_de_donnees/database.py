"""
Configuration de la base de données pour FastAPI avec SQLAlchemy
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool
import os
from typing import Generator

# Configuration de la base de données depuis les variables d'environnement
POSTGRES_USER = os.getenv("POSTGRES_USER", "postgres")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "postgres")
POSTGRES_SERVER = os.getenv("POSTGRES_SERVER", "localhost")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")
POSTGRES_DB = os.getenv("POSTGRES_DB", "revenus_miniers_db")

# URL de connexion
DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}"

# Création de l'engine SQLAlchemy
engine = create_engine(
    DATABASE_URL,
    poolclass=NullPool,  # Désactive le pool de connexions pour éviter les problèmes avec les connexions longues
    echo=False,  # Mettre à True pour le debug SQL
    future=True,
)

# Session locale
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    future=True,
)


def get_db() -> Generator:
    """
    Dependency pour obtenir une session de base de données dans FastAPI

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


def init_db():
    """
    Initialise la base de données en créant toutes les tables
    Note: En production, préférer les migrations Alembic
    """
    from models import Base
    Base.metadata.create_all(bind=engine)


def drop_db():
    """
    Supprime toutes les tables de la base de données
    ATTENTION: À utiliser uniquement en développement!
    """
    from models import Base
    Base.metadata.drop_all(bind=engine)
