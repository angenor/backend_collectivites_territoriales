"""
Tests pour les endpoints d'authentification
"""

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.models.utilisateurs import Role, Utilisateur
from app.core.security import get_password_hash


def test_register_user(client: TestClient, db: Session):
    """Test de l'enregistrement d'un nouvel utilisateur"""
    # Creer un role de test
    role = Role(
        code="LECTEUR",
        nom="Lecteur",
        description="Utilisateur en lecture seule",
        permissions={"read": True}
    )
    db.add(role)
    db.commit()
    db.refresh(role)

    # Donnees d'enregistrement
    register_data = {
        "email": "test@example.com",
        "username": "testuser",
        "password": "TestPassword123!",
        "nom": "Test",
        "prenom": "User",
        "role_id": str(role.id)  # Convert UUID to string for JSON serialization
    }

    response = client.post("/api/v1/auth/register", json=register_data)
    assert response.status_code == 201  # Created status
    data = response.json()
    assert data["email"] == "test@example.com"
    assert data["username"] == "testuser"
    assert "password" not in data
    assert "password_hash" not in data


def test_register_duplicate_email(client: TestClient, db: Session):
    """Test d'enregistrement avec un email deja utilise"""
    # Creer un role
    role = Role(code="LECTEUR", nom="Lecteur", permissions={"read": True})
    db.add(role)
    db.commit()
    db.refresh(role)

    # Creer un utilisateur existant
    existing_user = Utilisateur(
        email="existing@example.com",
        username="existing",
        password_hash=get_password_hash("password123"),
        nom="Existing",
        prenom="User",
        role_id=role.id
    )
    db.add(existing_user)
    db.commit()

    # Tenter de s'enregistrer avec le meme email
    register_data = {
        "email": "existing@example.com",
        "username": "newuser",
        "password": "Password123!",
        "nom": "New",
        "prenom": "User",
        "role_id": str(role.id)  # Convert UUID to string for JSON serialization
    }

    response = client.post("/api/v1/auth/register", json=register_data)
    assert response.status_code == 400


def test_login_success(client: TestClient, db: Session):
    """Test de connexion avec des identifiants valides"""
    # Creer un role
    role = Role(code="LECTEUR", nom="Lecteur", permissions={"read": True})
    db.add(role)
    db.commit()
    db.refresh(role)

    # Creer un utilisateur
    user = Utilisateur(
        email="user@example.com",
        username="testuser",
        password_hash=get_password_hash("password123"),
        nom="Test",
        prenom="User",
        role_id=role.id,
        actif=True
    )
    db.add(user)
    db.commit()

    # Se connecter
    login_data = {
        "username": "testuser",
        "password": "password123"
    }

    response = client.post(
        "/api/v1/auth/login",
        data=login_data,
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_wrong_password(client: TestClient, db: Session):
    """Test de connexion avec un mot de passe incorrect"""
    # Creer un role
    role = Role(code="LECTEUR", nom="Lecteur", permissions={"read": True})
    db.add(role)
    db.commit()
    db.refresh(role)

    # Creer un utilisateur
    user = Utilisateur(
        email="user@example.com",
        username="testuser",
        password_hash=get_password_hash("password123"),
        nom="Test",
        prenom="User",
        role_id=role.id,
        actif=True
    )
    db.add(user)
    db.commit()

    # Tenter de se connecter avec un mauvais mot de passe
    login_data = {
        "username": "testuser",
        "password": "wrongpassword"
    }

    response = client.post(
        "/api/v1/auth/login",
        data=login_data,
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    assert response.status_code == 401


def test_login_inactive_user(client: TestClient, db: Session):
    """Test de connexion avec un utilisateur inactif"""
    # Creer un role
    role = Role(code="LECTEUR", nom="Lecteur", permissions={"read": True})
    db.add(role)
    db.commit()
    db.refresh(role)

    # Creer un utilisateur inactif
    user = Utilisateur(
        email="inactive@example.com",
        username="inactiveuser",
        password_hash=get_password_hash("password123"),
        nom="Inactive",
        prenom="User",
        role_id=role.id,
        actif=False
    )
    db.add(user)
    db.commit()

    # Tenter de se connecter
    login_data = {
        "username": "inactiveuser",
        "password": "password123"
    }

    response = client.post(
        "/api/v1/auth/login",
        data=login_data,
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    assert response.status_code == 400


def test_get_current_user(client: TestClient, db: Session):
    """Test de recuperation de l'utilisateur courant"""
    # Creer un role
    role = Role(code="LECTEUR", nom="Lecteur", permissions={"read": True})
    db.add(role)
    db.commit()
    db.refresh(role)

    # Creer un utilisateur
    user = Utilisateur(
        email="user@example.com",
        username="testuser",
        password_hash=get_password_hash("password123"),
        nom="Test",
        prenom="User",
        role_id=role.id,
        actif=True
    )
    db.add(user)
    db.commit()

    # Se connecter pour obtenir un token
    login_data = {
        "username": "testuser",
        "password": "password123"
    }

    login_response = client.post(
        "/api/v1/auth/login",
        data=login_data,
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    token = login_response.json()["access_token"]

    # Recuperer l'utilisateur courant
    response = client.get(
        "/api/v1/auth/me",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "testuser"
    assert data["email"] == "user@example.com"


def test_get_current_user_invalid_token(client: TestClient):
    """Test de recuperation de l'utilisateur courant avec un token invalide"""
    response = client.get(
        "/api/v1/auth/me",
        headers={"Authorization": "Bearer invalid_token"}
    )
    assert response.status_code == 401


def test_get_current_user_no_token(client: TestClient):
    """Test de recuperation de l'utilisateur courant sans token"""
    response = client.get("/api/v1/auth/me")
    assert response.status_code == 401
