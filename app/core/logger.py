"""
Configuration du logger pour l'application
"""

import logging
import sys
from pathlib import Path
from loguru import logger

from app.core.config import settings


def setup_logging() -> None:
    """Configure le système de logging avec Loguru"""

    # Supprime les handlers par défaut
    logger.remove()

    # Format du log
    log_format = (
        "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
        "<level>{level: <8}</level> | "
        "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
        "<level>{message}</level>"
    )

    # Console output
    logger.add(
        sys.stdout,
        format=log_format,
        level="DEBUG" if settings.DEBUG else "INFO",
        colorize=True,
    )

    # File output (si en production)
    if settings.ENVIRONMENT == "production":
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)

        logger.add(
            log_dir / "app_{time:YYYY-MM-DD}.log",
            format=log_format,
            level="INFO",
            rotation="1 day",
            retention="30 days",
            compression="zip",
        )

        logger.add(
            log_dir / "errors_{time:YYYY-MM-DD}.log",
            format=log_format,
            level="ERROR",
            rotation="1 day",
            retention="90 days",
            compression="zip",
        )


def get_logger(name: str) -> logging.Logger:
    """
    Retourne un logger pour un module spécifique

    Args:
        name: Nom du module

    Returns:
        Logger configuré
    """
    return logger.bind(name=name)
