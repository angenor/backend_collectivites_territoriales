#!/usr/bin/env python3
"""
Script pour créer le premier utilisateur administrateur
Usage: python scripts/create_admin.py
"""

import sys
import os

# Ajouter le dossier parent au path pour importer les modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session
from app.database import SessionLocal, engine
from app.models import Base, Role, Utilisateur
from app.core.security import get_password_hash
from app.core.config import settings


def create_roles(db: Session):
    """Crée les rôles par défaut s'ils n'existent pas"""
    roles_data = [
        {
            "code": "ADMIN",
            "nom": "Administrateur",
            "description": "Administrateur système avec tous les droits",
            "permissions": {"all": True}
        },
        {
            "code": "EDITEUR",
            "nom": "Éditeur",
            "description": "Éditeur de contenu avec droits limités",
            "permissions": {"read": True, "create": True, "update": True}
        },
        {
            "code": "LECTEUR",
            "nom": "Lecteur",
            "description": "Utilisateur en lecture seule",
            "permissions": {"read": True}
        }
    ]

    created_roles = {}
    for role_data in roles_data:
        existing_role = db.query(Role).filter(Role.code == role_data["code"]).first()
        if not existing_role:
            role = Role(**role_data)
            db.add(role)
            print(f"✅ Rôle créé: {role_data['nom']}")
            created_roles[role_data["code"]] = role
        else:
            print(f"ℹ️  Rôle existe déjà: {role_data['nom']}")
            created_roles[role_data["code"]] = existing_role

    db.commit()
    return created_roles


def create_admin_user(db: Session, roles: dict):
    """Crée l'utilisateur administrateur"""
    # Vérifier si l'admin existe déjà
    existing_admin = db.query(Utilisateur).filter(
        (Utilisateur.email == settings.FIRST_SUPERUSER_EMAIL) |
        (Utilisateur.username == settings.FIRST_SUPERUSER_USERNAME)
    ).first()

    if existing_admin:
        print(f"⚠️  L'utilisateur admin existe déjà: {existing_admin.username}")
        return existing_admin

    # Créer l'admin
    admin_role = roles.get("ADMIN")
    if not admin_role:
        admin_role = db.query(Role).filter(Role.code == "ADMIN").first()
        if not admin_role:
            print("❌ Erreur: Rôle ADMIN non trouvé")
            return None

    admin = Utilisateur(
        email=settings.FIRST_SUPERUSER_EMAIL,
        username=settings.FIRST_SUPERUSER_USERNAME,
        nom="Administrateur",
        prenom="Système",
        password_hash=get_password_hash(settings.FIRST_SUPERUSER_PASSWORD),
        role_id=admin_role.id,
        actif=True,
        email_verifie=True
    )

    db.add(admin)
    db.commit()
    db.refresh(admin)

    print(f"✅ Utilisateur admin créé: {admin.username}")
    print(f"   Email: {admin.email}")
    print(f"   ⚠️  Pensez à changer le mot de passe par défaut!")
    return admin


def main():
    """Fonction principale"""
    print("=" * 60)
    print("🔐 Initialisation de l'utilisateur administrateur")
    print("=" * 60)
    print()

    # Créer les tables si nécessaire
    print("📊 Vérification de la base de données...")
    Base.metadata.create_all(bind=engine)

    # Créer une session
    db = SessionLocal()

    try:
        # Créer les rôles
        print("\n👥 Création des rôles...")
        roles = create_roles(db)

        # Créer l'admin
        print("\n🔑 Création de l'utilisateur admin...")
        admin = create_admin_user(db, roles)

        if admin:
            print("\n" + "=" * 60)
            print("✅ Initialisation terminée avec succès!")
            print("=" * 60)
            print(f"\n📋 Identifiants de connexion:")
            print(f"   Username: {settings.FIRST_SUPERUSER_USERNAME}")
            print(f"   Password: {settings.FIRST_SUPERUSER_PASSWORD}")
            print(f"   Email:    {settings.FIRST_SUPERUSER_EMAIL}")
            print("\n⚠️  IMPORTANT: Changez le mot de passe après la première connexion!")
            print()
        else:
            print("\n❌ Erreur lors de la création de l'admin")
            sys.exit(1)

    except Exception as e:
        print(f"\n❌ Erreur: {str(e)}")
        db.rollback()
        sys.exit(1)
    finally:
        db.close()


if __name__ == "__main__":
    main()
