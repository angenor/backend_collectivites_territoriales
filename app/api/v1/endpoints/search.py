"""
Public Search API endpoints.
Global search across communes, projects, documents, and more.
"""

from typing import Optional

from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.services.search_service import search_service

router = APIRouter(prefix="/search", tags=["Recherche"])


class SearchResultItem(BaseModel):
    """Individual search result."""
    type: str = Field(..., description="Type of result: commune, region, province, projet, societe, document")
    id: int
    titre: str
    description: Optional[str] = None
    score: float = Field(..., ge=0, le=1, description="Relevance score")
    metadata: dict = Field(default_factory=dict)


class SearchResultsResponse(BaseModel):
    """Search response with results and facets."""
    query: str
    total: int
    results: list[SearchResultItem]
    facets: dict = Field(..., description="Count by type")


class SuggestionItem(BaseModel):
    """Search suggestion."""
    type: str
    id: int
    label: str
    value: str


@router.get(
    "",
    response_model=SearchResultsResponse,
    summary="Recherche globale",
    description="Recherche dans les communes, régions, projets miniers et documents.",
)
async def search(
    q: str = Query(..., min_length=2, max_length=100, description="Terme de recherche"),
    types: Optional[str] = Query(
        None,
        description="Types à rechercher (séparés par virgule): commune, region, province, projet, societe, document"
    ),
    limit: int = Query(20, ge=1, le=100, description="Nombre maximum de résultats"),
    offset: int = Query(0, ge=0, description="Décalage pour la pagination"),
    db: Session = Depends(get_db),
):
    """
    Perform a global search across all entity types.

    Returns results sorted by relevance score, with facet counts by type.
    """
    # Parse types if provided
    type_list = None
    if types:
        type_list = [t.strip().lower() for t in types.split(",")]
        valid_types = {"commune", "region", "province", "projet", "societe", "document"}
        type_list = [t for t in type_list if t in valid_types]

    # Perform search
    response = search_service.search(
        db=db,
        query=q,
        types=type_list,
        limit=limit,
        offset=offset,
    )

    # Convert to response model
    return SearchResultsResponse(
        query=response.query,
        total=response.total,
        results=[
            SearchResultItem(
                type=r.type,
                id=r.id,
                titre=r.titre,
                description=r.description,
                score=r.score,
                metadata=r.metadata,
            )
            for r in response.results
        ],
        facets=response.facets,
    )


@router.get(
    "/suggestions",
    response_model=list[SuggestionItem],
    summary="Suggestions de recherche",
    description="Retourne des suggestions basées sur une saisie partielle.",
)
async def get_suggestions(
    q: str = Query(..., min_length=2, max_length=50, description="Texte partiel"),
    limit: int = Query(10, ge=1, le=20, description="Nombre maximum de suggestions"),
    db: Session = Depends(get_db),
):
    """
    Get search suggestions for autocomplete.

    Returns suggestions from communes, projects, and regions.
    """
    suggestions = search_service.get_suggestions(
        db=db,
        query=q,
        limit=limit,
    )

    return [
        SuggestionItem(
            type=s["type"],
            id=s["id"],
            label=s["label"],
            value=s["value"],
        )
        for s in suggestions
    ]


@router.get(
    "/communes",
    response_model=SearchResultsResponse,
    summary="Recherche de communes",
    description="Recherche spécifique dans les communes.",
)
async def search_communes(
    q: str = Query(..., min_length=2, max_length=100, description="Terme de recherche"),
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
):
    """
    Search only in communes.
    """
    response = search_service.search(
        db=db,
        query=q,
        types=["commune"],
        limit=limit,
        offset=offset,
    )

    return SearchResultsResponse(
        query=response.query,
        total=response.total,
        results=[
            SearchResultItem(
                type=r.type,
                id=r.id,
                titre=r.titre,
                description=r.description,
                score=r.score,
                metadata=r.metadata,
            )
            for r in response.results
        ],
        facets=response.facets,
    )


@router.get(
    "/projets",
    response_model=SearchResultsResponse,
    summary="Recherche de projets miniers",
    description="Recherche spécifique dans les projets miniers.",
)
async def search_projets(
    q: str = Query(..., min_length=2, max_length=100, description="Terme de recherche"),
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
):
    """
    Search only in mining projects and companies.
    """
    response = search_service.search(
        db=db,
        query=q,
        types=["projet", "societe"],
        limit=limit,
        offset=offset,
    )

    return SearchResultsResponse(
        query=response.query,
        total=response.total,
        results=[
            SearchResultItem(
                type=r.type,
                id=r.id,
                titre=r.titre,
                description=r.description,
                score=r.score,
                metadata=r.metadata,
            )
            for r in response.results
        ],
        facets=response.facets,
    )


@router.get(
    "/documents",
    response_model=SearchResultsResponse,
    summary="Recherche de documents",
    description="Recherche spécifique dans les documents publics.",
)
async def search_documents(
    q: str = Query(..., min_length=2, max_length=100, description="Terme de recherche"),
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
):
    """
    Search only in public documents.
    """
    response = search_service.search(
        db=db,
        query=q,
        types=["document"],
        limit=limit,
        offset=offset,
    )

    return SearchResultsResponse(
        query=response.query,
        total=response.total,
        results=[
            SearchResultItem(
                type=r.type,
                id=r.id,
                titre=r.titre,
                description=r.description,
                score=r.score,
                metadata=r.metadata,
            )
            for r in response.results
        ],
        facets=response.facets,
    )
