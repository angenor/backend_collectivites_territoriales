"""
Tests pour les endpoints de géographie
"""

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.models.geographie import Region


def test_get_regions_empty(client: TestClient):
    """Test récupération des régions quand la base est vide"""
    response = client.get("/api/v1/geo/regions")
    assert response.status_code == 200
    assert response.json() == []


def test_get_regions_with_data(client: TestClient, db: Session):
    """Test récupération des régions avec données"""
    # Créer des régions de test
    region1 = Region(code="ANA", nom="Analamanga", actif=True)
    region2 = Region(code="VAK", nom="Vakinankaratra", actif=True)

    db.add(region1)
    db.add(region2)
    db.commit()

    response = client.get("/api/v1/geo/regions")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["code"] == "ANA"
    assert data[0]["nom"] == "Analamanga"
