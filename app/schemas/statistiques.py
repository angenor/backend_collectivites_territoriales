"""
Schémas Pydantic pour les statistiques
"""

from pydantic import BaseModel
from typing import List, Dict, Any
from decimal import Decimal

from app.schemas.geographie import Commune, Region
from app.schemas.revenus import Exercice


class StatistiquesCommune(BaseModel):
    """Statistiques financières pour une commune"""
    commune: Commune
    total_recettes: Decimal
    total_depenses: Decimal
    solde: Decimal
    nb_projets_miniers: int
    exercices_disponibles: List[int]


class StatistiquesRegion(BaseModel):
    """Statistiques financières pour une région"""
    region: Region
    nb_communes: int
    nb_projets_miniers: int
    total_revenus_miniers: Decimal
    communes_top: List[Dict[str, Any]]


class TableauCompteAdministratif(BaseModel):
    """Structure complète d'un tableau de compte administratif"""
    commune: Commune
    exercice: Exercice
    donnees: Dict[str, Any]  # Structure complexe des données
    totaux: Dict[str, Decimal]
