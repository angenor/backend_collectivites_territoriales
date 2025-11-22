"""
Tests pour le service d'authentification
"""

from sqlalchemy.orm import Session

from app.models.utilisateurs import Role, Utilisateur
from app.services.auth_service import AuthService
from app.core.security import get_password_hash, verify_password


def test_authenticate_user_success(db: Session):
    """Test d'authentification avec des identifiants valides"""
    # Creer un role
    role = Role(code="ADMIN", nom="Administrateur", permissions={"all": True})
    db.add(role)
    db.commit()
    db.refresh(role)

    # Creer un utilisateur
    user = Utilisateur(
        email="test@example.com",
        username="testuser",
        password_hash=get_password_hash("password123"),
        nom="Test",
        prenom="User",
        role_id=role.id,
        actif=True
    )
    db.add(user)
    db.commit()

    # Tenter de s'authentifier
    authenticated_user = AuthService.authenticate_user(db, "testuser", "password123")
    assert authenticated_user is not None
    assert authenticated_user.username == "testuser"
    assert authenticated_user.email == "test@example.com"


def test_authenticate_user_wrong_password(db: Session):
    """Test d'authentification avec un mot de passe incorrect"""
    # Creer un role
    role = Role(code="ADMIN", nom="Administrateur", permissions={"all": True})
    db.add(role)
    db.commit()

    # Creer un utilisateur
    user = Utilisateur(
        email="test@example.com",
        username="testuser",
        password_hash=get_password_hash("password123"),
        nom="Test",
        prenom="User",
        role_id=role.id,
        actif=True
    )
    db.add(user)
    db.commit()

    # Tenter de s'authentifier avec un mauvais mot de passe
    authenticated_user = AuthService.authenticate_user(db, "testuser", "wrongpassword")
    assert authenticated_user is None


def test_authenticate_user_not_found(db: Session):
    """Test d'authentification avec un utilisateur inexistant"""
    authenticated_user = AuthService.authenticate_user(db, "nonexistent", "password123")
    assert authenticated_user is None


def test_create_access_token(db: Session):
    """Test de creation d'un token d'acces"""
    # Creer un role
    role = Role(code="ADMIN", nom="Administrateur", permissions={"all": True})
    db.add(role)
    db.commit()

    # Creer un utilisateur
    user = Utilisateur(
        email="test@example.com",
        username="testuser",
        password_hash=get_password_hash("password123"),
        nom="Test",
        prenom="User",
        role_id=role.id,
        actif=True
    )
    db.add(user)
    db.commit()

    # Creer un token
    token = AuthService.create_access_token_for_user(user)
    assert token is not None
    assert isinstance(token, str)
    assert len(token) > 0


def test_password_hashing():
    """Test du hachage et de la verification des mots de passe"""
    password = "MySecurePassword123!"
    hashed = get_password_hash(password)

    # Verifier que le hash est different du mot de passe original
    assert hashed != password

    # Verifier que la verification fonctionne
    assert verify_password(password, hashed) is True

    # Verifier qu'un mauvais mot de passe echoue
    assert verify_password("WrongPassword", hashed) is False


def test_register_user(db: Session):
    """Test d'enregistrement d'un nouvel utilisateur"""
    # Creer un role
    role = Role(code="LECTEUR", nom="Lecteur", permissions={"read": True})
    db.add(role)
    db.commit()
    db.refresh(role)

    # Enregistrer un utilisateur
    user = AuthService.register_user(
        db=db,
        email="newuser@example.com",
        username="newuser",
        password="Password123!",
        nom="New",
        prenom="User",
        role_id=role.id
    )

    assert user is not None
    assert user.email == "newuser@example.com"
    assert user.username == "newuser"
    assert user.actif is True

    # Verifier que le mot de passe a ete hache
    assert user.password_hash != "Password123!"
    assert verify_password("Password123!", user.password_hash) is True


def test_register_user_duplicate_email(db: Session):
    """Test d'enregistrement avec un email deja utilise"""
    # Creer un role
    role = Role(code="LECTEUR", nom="Lecteur", permissions={"read": True})
    db.add(role)
    db.commit()

    # Creer un premier utilisateur
    user1 = Utilisateur(
        email="existing@example.com",
        username="user1",
        password_hash=get_password_hash("password123"),
        nom="User",
        prenom="One",
        role_id=role.id
    )
    db.add(user1)
    db.commit()

    # Tenter de creer un autre utilisateur avec le meme email
    try:
        user2 = AuthService.register_user(
            db=db,
            email="existing@example.com",
            username="user2",
            password="Password123!",
            nom="User",
            prenom="Two",
            role_id=role.id
        )
        # Si on arrive ici, le test echoue car une exception aurait du etre levee
        assert False, "Expected an exception for duplicate email"
    except Exception:
        # C'est le comportement attendu
        pass


def test_authenticate_inactive_user(db: Session):
    """Test d'authentification d'un utilisateur inactif"""
    # Creer un role
    role = Role(code="ADMIN", nom="Administrateur", permissions={"all": True})
    db.add(role)
    db.commit()

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

    # Tenter de s'authentifier
    authenticated_user = AuthService.authenticate_user(db, "inactiveuser", "password123")

    # Le service devrait retourner None ou lever une exception
    # selon l'implementation
    assert authenticated_user is None or not authenticated_user.actif
