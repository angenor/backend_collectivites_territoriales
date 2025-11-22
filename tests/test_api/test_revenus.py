"""
Tests pour les endpoints de revenus
"""

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from decimal import Decimal

from app.models.geographie import Region, Departement, Commune
from app.models.revenus import Exercice, Periode, CategorieRubrique, Rubrique, Revenu
from app.models.utilisateurs import Role, Utilisateur
from app.core.security import get_password_hash


def create_test_user(db: Session) -> tuple[Utilisateur, str]:
    """Cree un utilisateur de test et retourne l'utilisateur et son token"""
    from fastapi.testclient import TestClient
    from app.main import app

    client = TestClient(app)

    # Creer un role
    role = Role(code="ADMIN", nom="Administrateur", permissions={"all": True})
    db.add(role)
    db.commit()
    db.refresh(role)

    # Creer un utilisateur
    user = Utilisateur(
        email="admin@example.com",
        username="admin",
        password_hash=get_password_hash("admin123"),
        nom="Admin",
        prenom="User",
        role_id=role.id,
        actif=True
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    # Se connecter pour obtenir un token
    login_data = {
        "username": "admin",
        "password": "admin123"
    }
    login_response = client.post(
        "/api/v1/auth/login",
        data=login_data,
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    token = login_response.json()["access_token"]

    return user, token


def test_create_revenu(client: TestClient, db: Session):
    """Test de creation d'un revenu"""
    user, token = create_test_user(db)

    # Creer les donnees geographiques
    region = Region(code="ANA", nom="Analamanga", actif=True)
    db.add(region)
    db.commit()

    departement = Departement(code="ANT", nom="Antananarivo", region_id=region.id, actif=True)
    db.add(departement)
    db.commit()

    commune = Commune(code="ANT01", nom="Antananarivo I", departement_id=departement.id, actif=True)
    db.add(commune)
    db.commit()

    # Creer un exercice
    exercice = Exercice(annee=2024, actif=True)
    db.add(exercice)
    db.commit()
    db.refresh(exercice)

    # Creer une periode
    periode = Periode(
        nom="Trimestre 1",
        code="T1",
        exercice_id=exercice.id,
        ordre=1,
        actif=True
    )
    db.add(periode)
    db.commit()
    db.refresh(periode)

    # Creer une categorie et une rubrique
    categorie = CategorieRubrique(code="REC", nom="Recettes", actif=True)
    db.add(categorie)
    db.commit()

    rubrique = Rubrique(
        code="R001",
        nom="Impots locaux",
        categorie_id=categorie.id,
        niveau=1,
        actif=True
    )
    db.add(rubrique)
    db.commit()
    db.refresh(rubrique)

    # Creer un revenu
    revenu_data = {
        "commune_id": commune.id,
        "exercice_id": exercice.id,
        "periode_id": periode.id,
        "rubrique_id": rubrique.id,
        "montant": 150000.50
    }

    response = client.post(
        "/api/v1/revenus/",
        json=revenu_data,
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert float(data["montant"]) == 150000.50
    assert data["rubrique_id"] == rubrique.id


def test_get_tableau_compte_administratif(client: TestClient, db: Session):
    """Test de recuperation du tableau de compte administratif"""
    user, token = create_test_user(db)

    # Creer les donnees geographiques
    region = Region(code="ANA", nom="Analamanga", actif=True)
    db.add(region)
    db.commit()

    departement = Departement(code="ANT", nom="Antananarivo", region_id=region.id, actif=True)
    db.add(departement)
    db.commit()

    commune = Commune(code="ANT01", nom="Antananarivo I", departement_id=departement.id, actif=True)
    db.add(commune)
    db.commit()

    # Creer un exercice
    exercice = Exercice(annee=2024, actif=True)
    db.add(exercice)
    db.commit()
    db.refresh(exercice)

    # Creer des periodes
    periode1 = Periode(nom="T1", code="T1", exercice_id=exercice.id, ordre=1, actif=True)
    periode2 = Periode(nom="T2", code="T2", exercice_id=exercice.id, ordre=2, actif=True)
    db.add_all([periode1, periode2])
    db.commit()
    db.refresh(periode1)
    db.refresh(periode2)

    # Creer une categorie et une rubrique
    categorie = CategorieRubrique(code="REC", nom="Recettes", actif=True)
    db.add(categorie)
    db.commit()

    rubrique = Rubrique(
        code="R001",
        nom="Impots locaux",
        categorie_id=categorie.id,
        niveau=1,
        actif=True
    )
    db.add(rubrique)
    db.commit()
    db.refresh(rubrique)

    # Creer des revenus
    revenu1 = Revenu(
        commune_id=commune.id,
        exercice_id=exercice.id,
        periode_id=periode1.id,
        rubrique_id=rubrique.id,
        montant=Decimal("100000.00")
    )
    revenu2 = Revenu(
        commune_id=commune.id,
        exercice_id=exercice.id,
        periode_id=periode2.id,
        rubrique_id=rubrique.id,
        montant=Decimal("120000.00")
    )
    db.add_all([revenu1, revenu2])
    db.commit()

    # Recuperer le tableau
    response = client.get(
        f"/api/v1/revenus/tableau/{commune.code}/{exercice.annee}",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["commune"]["code"] == "ANT01"
    assert data["exercice"]["annee"] == 2024
    assert len(data["periodes"]) == 2
    assert len(data["rubriques"]) == 1


def test_get_tableau_commune_not_found(client: TestClient, db: Session):
    """Test de recuperation du tableau avec une commune inexistante"""
    user, token = create_test_user(db)

    response = client.get(
        "/api/v1/revenus/tableau/INVALID/2024",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 404


def test_get_tableau_exercice_not_found(client: TestClient, db: Session):
    """Test de recuperation du tableau avec un exercice inexistant"""
    user, token = create_test_user(db)

    # Creer une commune
    region = Region(code="ANA", nom="Analamanga", actif=True)
    db.add(region)
    db.commit()

    departement = Departement(code="ANT", nom="Antananarivo", region_id=region.id, actif=True)
    db.add(departement)
    db.commit()

    commune = Commune(code="ANT01", nom="Antananarivo I", departement_id=departement.id, actif=True)
    db.add(commune)
    db.commit()

    response = client.get(
        f"/api/v1/revenus/tableau/{commune.code}/9999",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 404


def test_get_revenus_with_filters(client: TestClient, db: Session):
    """Test de recuperation des revenus avec filtres"""
    user, token = create_test_user(db)

    # Creer les donnees necessaires
    region = Region(code="ANA", nom="Analamanga", actif=True)
    db.add(region)
    db.commit()

    departement = Departement(code="ANT", nom="Antananarivo", region_id=region.id, actif=True)
    db.add(departement)
    db.commit()

    commune = Commune(code="ANT01", nom="Antananarivo I", departement_id=departement.id, actif=True)
    db.add(commune)
    db.commit()

    exercice = Exercice(annee=2024, actif=True)
    db.add(exercice)
    db.commit()
    db.refresh(exercice)

    periode = Periode(nom="T1", code="T1", exercice_id=exercice.id, ordre=1, actif=True)
    db.add(periode)
    db.commit()
    db.refresh(periode)

    categorie = CategorieRubrique(code="REC", nom="Recettes", actif=True)
    db.add(categorie)
    db.commit()

    rubrique = Rubrique(code="R001", nom="Impots", categorie_id=categorie.id, niveau=1, actif=True)
    db.add(rubrique)
    db.commit()
    db.refresh(rubrique)

    # Creer des revenus
    revenu = Revenu(
        commune_id=commune.id,
        exercice_id=exercice.id,
        periode_id=periode.id,
        rubrique_id=rubrique.id,
        montant=Decimal("100000.00")
    )
    db.add(revenu)
    db.commit()

    # Tester avec filtre par commune
    response = client.get(
        f"/api/v1/revenus/?commune_code={commune.code}",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
