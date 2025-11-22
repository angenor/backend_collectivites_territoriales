"""
Configuration pytest et fixtures globales
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool

from app.main import app
from app.database import Base, get_db
from app.core.config import settings

# Utiliser PostgreSQL pour les tests avec une base de donnees dediee
# Remplacer le nom de la base de donnees par une version test
TEST_DATABASE_URL = settings.DATABASE_URL.replace(
    settings.POSTGRES_DB,
    f"{settings.POSTGRES_DB}_test"
)

engine = create_engine(
    TEST_DATABASE_URL,
    poolclass=NullPool,  # Pas de pool pour les tests
    echo=False  # Mettre a True pour voir les requetes SQL
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, future=True)


def override_get_db():
    """Override de la dependance get_db pour les tests"""
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


@pytest.fixture(scope="session", autouse=True)
def setup_test_database():
    """Cree la base de donnees de test au debut de la session de tests"""
    from sqlalchemy import create_engine

    # Connexion au serveur PostgreSQL (sans specifier de base de donnees)
    server_url = TEST_DATABASE_URL.rsplit("/", 1)[0] + "/postgres"
    server_engine = create_engine(server_url, isolation_level="AUTOCOMMIT")

    # Supprimer la base de test si elle existe et la recreer
    with server_engine.connect() as conn:
        # Deconnecter tous les utilisateurs de la base de test
        conn.execute(text(f"""
            SELECT pg_terminate_backend(pg_stat_activity.pid)
            FROM pg_stat_activity
            WHERE pg_stat_activity.datname = '{settings.POSTGRES_DB}_test'
            AND pid <> pg_backend_pid()
        """))

        # Supprimer la base si elle existe
        conn.execute(text(f"DROP DATABASE IF EXISTS {settings.POSTGRES_DB}_test"))

        # Creer la base de test
        conn.execute(text(f"CREATE DATABASE {settings.POSTGRES_DB}_test"))

    server_engine.dispose()

    # Creer toutes les tables
    Base.metadata.create_all(bind=engine)

    yield

    # Nettoyage final : supprimer toutes les tables
    Base.metadata.drop_all(bind=engine)
    engine.dispose()

    # Supprimer la base de donnees de test
    cleanup_engine = create_engine(server_url, isolation_level="AUTOCOMMIT")
    with cleanup_engine.connect() as conn:
        conn.execute(text(f"""
            SELECT pg_terminate_backend(pg_stat_activity.pid)
            FROM pg_stat_activity
            WHERE pg_stat_activity.datname = '{settings.POSTGRES_DB}_test'
            AND pid <> pg_backend_pid()
        """))
        conn.execute(text(f"DROP DATABASE IF EXISTS {settings.POSTGRES_DB}_test"))

    cleanup_engine.dispose()


@pytest.fixture(scope="function")
def db():
    """Fixture pour la base de donnees de test - nettoie les donnees entre chaque test"""
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)

    yield session

    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture(scope="function")
def client(db):
    """Fixture pour le client de test FastAPI"""
    def override_get_db_with_session():
        try:
            yield db
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db_with_session
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()
