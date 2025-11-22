"""
Configuration Alembic pour les migrations
"""
from logging.config import fileConfig
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context
import os
import sys

# Ajout du chemin parent pour l'import des modèles
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

# Import des modèles SQLAlchemy
from models import Base

# Configuration Alembic
config = context.config

# Interprétation du fichier de config pour la logging Python
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Métadonnées du modèle pour 'autogenerate'
target_metadata = Base.metadata

# Récupération de l'URL de la base de données depuis les variables d'environnement
def get_url():
    """Récupère l'URL de connexion depuis les variables d'environnement"""
    user = os.getenv("POSTGRES_USER", "postgres")
    password = os.getenv("POSTGRES_PASSWORD", "postgres")
    server = os.getenv("POSTGRES_SERVER", "localhost")
    port = os.getenv("POSTGRES_PORT", "5432")
    db = os.getenv("POSTGRES_DB", "revenus_miniers_db")
    return f"postgresql://{user}:{password}@{server}:{port}/{db}"


def run_migrations_offline() -> None:
    """
    Exécute les migrations en mode 'offline'.
    Configure le contexte avec juste une URL et non un Engine.
    """
    url = get_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
        compare_server_default=True,
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """
    Exécute les migrations en mode 'online'.
    Crée un Engine et associe une connexion avec le contexte.
    """
    configuration = config.get_section(config.config_ini_section)
    configuration["sqlalchemy.url"] = get_url()

    connectable = engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
            compare_server_default=True,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
