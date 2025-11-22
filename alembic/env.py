"""
Configuration Alembic pour les migrations
"""

from logging.config import fileConfig
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context
import os
import sys

# Ajout du chemin pour importer les modules de l'application
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

# Import des modèles et configuration
from app.models import Base
from app.core.config import settings

# Configuration Alembic
config = context.config

# Interprétation du fichier de config pour le logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Métadonnées du modèle pour 'autogenerate'
target_metadata = Base.metadata


def get_url():
    """Récupère l'URL de connexion depuis les settings"""
    return settings.DATABASE_URL


def run_migrations_offline() -> None:
    """
    Exécute les migrations en mode 'offline'.
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
