"""
Tests pour les endpoints d'export
"""

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from decimal import Decimal

from app.models.geographie import Region, Departement, Commune
from app.models.revenus import Exercice, Periode, CategorieRubrique, Rubrique, Revenu
from app.models.utilisateurs import Role, Utilisateur
from app.core.security import get_password_hash


def create_test_data_and_user(db: Session) -> tuple[Commune, Exercice, str]:
    """Cree les donnees de test et retourne la commune, l'exercice et le token"""
    from fastapi.testclient import TestClient
    from app.main import app

    client = TestClient(app)

    # Creer un role et un utilisateur
    role = Role(code="ADMIN", nom="Administrateur", permissions={"all": True})
    db.add(role)
    db.commit()
    db.refresh(role)

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

    # Se connecter
    login_data = {"username": "admin", "password": "admin123"}
    login_response = client.post(
        "/api/v1/auth/login",
        data=login_data,
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    token = login_response.json()["access_token"]

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

    # Creer une categorie et des rubriques
    categorie = CategorieRubrique(code="REC", nom="Recettes", actif=True)
    db.add(categorie)
    db.commit()

    rubrique1 = Rubrique(
        code="R001",
        nom="Impots locaux",
        categorie_id=categorie.id,
        niveau=1,
        actif=True
    )
    rubrique2 = Rubrique(
        code="R002",
        nom="Taxes diverses",
        categorie_id=categorie.id,
        niveau=1,
        actif=True
    )
    db.add_all([rubrique1, rubrique2])
    db.commit()
    db.refresh(rubrique1)
    db.refresh(rubrique2)

    # Creer des revenus
    revenus = [
        Revenu(
            commune_id=commune.id,
            exercice_id=exercice.id,
            periode_id=periode1.id,
            rubrique_id=rubrique1.id,
            montant=Decimal("100000.00")
        ),
        Revenu(
            commune_id=commune.id,
            exercice_id=exercice.id,
            periode_id=periode2.id,
            rubrique_id=rubrique1.id,
            montant=Decimal("120000.00")
        ),
        Revenu(
            commune_id=commune.id,
            exercice_id=exercice.id,
            periode_id=periode1.id,
            rubrique_id=rubrique2.id,
            montant=Decimal("50000.00")
        ),
    ]
    db.add_all(revenus)
    db.commit()

    return commune, exercice, token


def test_export_excel(client: TestClient, db: Session):
    """Test d'export Excel"""
    commune, exercice, token = create_test_data_and_user(db)

    response = client.get(
        f"/api/v1/export/excel/{commune.code}/{exercice.annee}",
        headers={"Authorization": f"Bearer {token}"}
    )

    # Verifier le statut de la reponse
    # Si les librairies ne sont pas installees, on recoit un 501
    # Si elles sont installees, on recoit un 200
    assert response.status_code in [200, 501]

    if response.status_code == 200:
        # Verifier les en-tetes
        assert response.headers["content-type"] == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        assert "attachment" in response.headers["content-disposition"]
        assert "Antananarivo_I_2024.xlsx" in response.headers["content-disposition"]

        # Verifier que le contenu n'est pas vide
        assert len(response.content) > 0


def test_export_word(client: TestClient, db: Session):
    """Test d'export Word"""
    commune, exercice, token = create_test_data_and_user(db)

    response = client.get(
        f"/api/v1/export/word/{commune.code}/{exercice.annee}",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code in [200, 501]

    if response.status_code == 200:
        # Verifier les en-tetes
        assert response.headers["content-type"] == "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        assert "attachment" in response.headers["content-disposition"]
        assert "Antananarivo_I_2024.docx" in response.headers["content-disposition"]

        # Verifier que le contenu n'est pas vide
        assert len(response.content) > 0


def test_export_pdf(client: TestClient, db: Session):
    """Test d'export PDF"""
    commune, exercice, token = create_test_data_and_user(db)

    response = client.get(
        f"/api/v1/export/pdf/{commune.code}/{exercice.annee}",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code in [200, 501]

    if response.status_code == 200:
        # Verifier les en-tetes
        assert response.headers["content-type"] == "application/pdf"
        assert "attachment" in response.headers["content-disposition"]
        assert "Antananarivo_I_2024.pdf" in response.headers["content-disposition"]

        # Verifier que le contenu n'est pas vide
        assert len(response.content) > 0


def test_export_formats_list(client: TestClient):
    """Test de la liste des formats d'export disponibles"""
    response = client.get("/api/v1/export/formats")
    assert response.status_code == 200

    data = response.json()
    assert "formats" in data
    assert len(data["formats"]) == 3

    # Verifier que tous les formats sont presents
    format_names = [f["name"] for f in data["formats"]]
    assert "Excel" in format_names
    assert "Word" in format_names
    assert "PDF" in format_names

    # Verifier les extensions
    for format_info in data["formats"]:
        assert "extension" in format_info
        assert "mime_type" in format_info
        assert "endpoint" in format_info


def test_export_commune_not_found(client: TestClient, db: Session):
    """Test d'export avec une commune inexistante"""
    # Creer juste un utilisateur
    role = Role(code="ADMIN", nom="Administrateur", permissions={"all": True})
    db.add(role)
    db.commit()

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

    # Se connecter
    login_data = {"username": "admin", "password": "admin123"}
    login_response = client.post(
        "/api/v1/auth/login",
        data=login_data,
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    token = login_response.json()["access_token"]

    response = client.get(
        "/api/v1/export/excel/INVALID/2024",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 404


def test_export_without_authentication(client: TestClient, db: Session):
    """Test d'export sans authentification"""
    response = client.get("/api/v1/export/excel/ANT01/2024")
    assert response.status_code == 401
