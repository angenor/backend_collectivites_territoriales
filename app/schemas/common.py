"""
Schémas Pydantic communs utilisés dans toute l'application
"""

from pydantic import BaseModel, Field
from typing import List, Any, Generic, TypeVar
from datetime import datetime


class TimestampSchema(BaseModel):
    """Schéma de base avec timestamps"""
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class PaginationParams(BaseModel):
    """Paramètres de pagination"""
    page: int = Field(default=1, ge=1, description="Numéro de page")
    page_size: int = Field(default=50, ge=1, le=1000, description="Nombre d'éléments par page")


T = TypeVar('T')


class PaginatedResponse(BaseModel, Generic[T]):
    """Réponse paginée générique"""
    items: List[T]
    total: int
    page: int
    page_size: int
    total_pages: int


class MessageResponse(BaseModel):
    """Réponse simple avec message"""
    message: str
    success: bool = True
