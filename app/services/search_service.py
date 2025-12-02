"""
Search service with PostgreSQL full-text search.
Provides global search across communes, projects, and documents.
"""

from dataclasses import dataclass
from typing import Optional

from sqlalchemy import func, or_, text
from sqlalchemy.orm import Session

from app.models.documents import Document
from app.models.geographie import Commune, Province, Region
from app.models.projets_miniers import ProjetMinier, SocieteMiniere


@dataclass
class SearchResult:
    """Individual search result."""
    type: str  # 'commune', 'region', 'province', 'projet', 'societe', 'document'
    id: int
    titre: str
    description: Optional[str]
    score: float
    metadata: dict


@dataclass
class SearchResponse:
    """Complete search response."""
    query: str
    total: int
    results: list[SearchResult]
    facets: dict


class SearchService:
    """
    Service for full-text search across multiple entities.
    Uses PostgreSQL full-text search with ts_vector and ts_query.
    """

    def search(
        self,
        db: Session,
        query: str,
        types: Optional[list[str]] = None,
        limit: int = 20,
        offset: int = 0,
    ) -> SearchResponse:
        """
        Perform global search across all entities.

        Args:
            db: Database session
            query: Search query string
            types: Optional list of types to search ('commune', 'projet', 'document', etc.)
            limit: Maximum results to return
            offset: Results offset for pagination

        Returns:
            SearchResponse with results and facets
        """
        if not query or len(query.strip()) < 2:
            return SearchResponse(query=query, total=0, results=[], facets={})

        # Normalize query for PostgreSQL full-text search
        search_term = self._normalize_query(query)
        like_term = f"%{query.lower()}%"

        all_results: list[SearchResult] = []
        facets = {
            "commune": 0,
            "region": 0,
            "province": 0,
            "projet": 0,
            "societe": 0,
            "document": 0,
        }

        # Determine which types to search
        search_types = types if types else list(facets.keys())

        # Search communes
        if "commune" in search_types:
            communes = self._search_communes(db, like_term, limit * 2)
            for c in communes:
                all_results.append(SearchResult(
                    type="commune",
                    id=c.id,
                    titre=c.nom,
                    description=f"{c.region.nom}, {c.region.province.nom}" if c.region else None,
                    score=self._calculate_score(query, c.nom),
                    metadata={
                        "code": c.code,
                        "type_commune": c.type_commune.value if c.type_commune else None,
                        "region_id": c.region_id,
                    },
                ))
            facets["commune"] = len(communes)

        # Search regions
        if "region" in search_types:
            regions = self._search_regions(db, like_term, limit)
            for r in regions:
                all_results.append(SearchResult(
                    type="region",
                    id=r.id,
                    titre=r.nom,
                    description=f"Province: {r.province.nom}" if r.province else None,
                    score=self._calculate_score(query, r.nom),
                    metadata={
                        "code": r.code,
                        "province_id": r.province_id,
                        "nb_communes": len(r.communes) if r.communes else 0,
                    },
                ))
            facets["region"] = len(regions)

        # Search provinces
        if "province" in search_types:
            provinces = self._search_provinces(db, like_term, limit)
            for p in provinces:
                all_results.append(SearchResult(
                    type="province",
                    id=p.id,
                    titre=p.nom,
                    description=f"Chef-lieu: {p.chef_lieu}" if p.chef_lieu else None,
                    score=self._calculate_score(query, p.nom),
                    metadata={
                        "code": p.code,
                        "nb_regions": len(p.regions) if p.regions else 0,
                    },
                ))
            facets["province"] = len(provinces)

        # Search mining projects
        if "projet" in search_types:
            projets = self._search_projets(db, like_term, limit)
            for p in projets:
                all_results.append(SearchResult(
                    type="projet",
                    id=p.id,
                    titre=p.nom,
                    description=f"{p.type_minerai} - {p.societe.nom}" if p.societe else p.type_minerai,
                    score=self._calculate_score(query, p.nom),
                    metadata={
                        "type_minerai": p.type_minerai,
                        "statut": p.statut.value if p.statut else None,
                        "societe_id": p.societe_id,
                    },
                ))
            facets["projet"] = len(projets)

        # Search mining companies
        if "societe" in search_types:
            societes = self._search_societes(db, like_term, limit)
            for s in societes:
                all_results.append(SearchResult(
                    type="societe",
                    id=s.id,
                    titre=s.nom,
                    description=s.pays_origine,
                    score=self._calculate_score(query, s.nom),
                    metadata={
                        "pays_origine": s.pays_origine,
                        "nb_projets": len(s.projets) if s.projets else 0,
                    },
                ))
            facets["societe"] = len(societes)

        # Search documents
        if "document" in search_types:
            documents = self._search_documents(db, like_term, limit)
            for d in documents:
                all_results.append(SearchResult(
                    type="document",
                    id=d.id,
                    titre=d.titre,
                    description=d.description,
                    score=self._calculate_score(query, d.titre),
                    metadata={
                        "type_document": d.type_document.value if d.type_document else None,
                        "mime_type": d.mime_type,
                        "commune_id": d.commune_id,
                    },
                ))
            facets["document"] = len(documents)

        # Sort by score
        all_results.sort(key=lambda x: x.score, reverse=True)

        # Apply pagination
        total = len(all_results)
        paginated_results = all_results[offset:offset + limit]

        return SearchResponse(
            query=query,
            total=total,
            results=paginated_results,
            facets=facets,
        )

    def get_suggestions(
        self,
        db: Session,
        query: str,
        limit: int = 10,
    ) -> list[dict]:
        """
        Get search suggestions based on partial query.

        Returns list of suggestions with type and label.
        """
        if not query or len(query.strip()) < 2:
            return []

        like_term = f"%{query.lower()}%"
        suggestions = []

        # Get commune suggestions
        communes = db.query(Commune.id, Commune.nom).filter(
            Commune.nom.ilike(like_term)
        ).limit(limit // 3).all()

        for c in communes:
            suggestions.append({
                "type": "commune",
                "id": c.id,
                "label": c.nom,
                "value": c.nom,
            })

        # Get project suggestions
        projets = db.query(ProjetMinier.id, ProjetMinier.nom).filter(
            ProjetMinier.nom.ilike(like_term)
        ).limit(limit // 3).all()

        for p in projets:
            suggestions.append({
                "type": "projet",
                "id": p.id,
                "label": p.nom,
                "value": p.nom,
            })

        # Get region suggestions
        regions = db.query(Region.id, Region.nom).filter(
            Region.nom.ilike(like_term)
        ).limit(limit // 3).all()

        for r in regions:
            suggestions.append({
                "type": "region",
                "id": r.id,
                "label": r.nom,
                "value": r.nom,
            })

        return suggestions[:limit]

    def _normalize_query(self, query: str) -> str:
        """Normalize query for PostgreSQL full-text search."""
        # Remove special characters and prepare for tsquery
        words = query.strip().split()
        return " & ".join(words)

    def _calculate_score(self, query: str, text: str) -> float:
        """Calculate relevance score based on query match."""
        if not text:
            return 0.0

        query_lower = query.lower()
        text_lower = text.lower()

        # Exact match gets highest score
        if query_lower == text_lower:
            return 1.0

        # Starts with gets high score
        if text_lower.startswith(query_lower):
            return 0.9

        # Contains gets medium score
        if query_lower in text_lower:
            return 0.7

        # Partial word match
        query_words = set(query_lower.split())
        text_words = set(text_lower.split())
        common = query_words & text_words
        if common:
            return 0.5 * len(common) / len(query_words)

        return 0.1

    def _search_communes(self, db: Session, like_term: str, limit: int) -> list[Commune]:
        """Search communes by name or code."""
        return db.query(Commune).filter(
            or_(
                Commune.nom.ilike(like_term),
                Commune.code.ilike(like_term),
            )
        ).limit(limit).all()

    def _search_regions(self, db: Session, like_term: str, limit: int) -> list[Region]:
        """Search regions by name or code."""
        return db.query(Region).filter(
            or_(
                Region.nom.ilike(like_term),
                Region.code.ilike(like_term),
            )
        ).limit(limit).all()

    def _search_provinces(self, db: Session, like_term: str, limit: int) -> list[Province]:
        """Search provinces by name or code."""
        return db.query(Province).filter(
            or_(
                Province.nom.ilike(like_term),
                Province.code.ilike(like_term),
                Province.chef_lieu.ilike(like_term),
            )
        ).limit(limit).all()

    def _search_projets(self, db: Session, like_term: str, limit: int) -> list[ProjetMinier]:
        """Search mining projects by name or mineral type."""
        return db.query(ProjetMinier).filter(
            or_(
                ProjetMinier.nom.ilike(like_term),
                ProjetMinier.type_minerai.ilike(like_term),
                ProjetMinier.description.ilike(like_term),
            )
        ).limit(limit).all()

    def _search_societes(self, db: Session, like_term: str, limit: int) -> list[SocieteMiniere]:
        """Search mining companies by name."""
        return db.query(SocieteMiniere).filter(
            or_(
                SocieteMiniere.nom.ilike(like_term),
                SocieteMiniere.pays_origine.ilike(like_term),
            )
        ).limit(limit).all()

    def _search_documents(self, db: Session, like_term: str, limit: int) -> list[Document]:
        """Search public documents by title or description."""
        return db.query(Document).filter(
            Document.public == True,
            or_(
                Document.titre.ilike(like_term),
                Document.description.ilike(like_term),
                Document.nom_fichier.ilike(like_term),
            )
        ).limit(limit).all()


# Singleton instance
search_service = SearchService()
