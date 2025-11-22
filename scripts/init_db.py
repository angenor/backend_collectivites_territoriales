#!/usr/bin/env python3
"""
Script pour initialiser complètement la base de données
- Crée les tables
- Charge les données initiales
- Crée l'utilisateur admin

Usage: python scripts/init_db.py
"""

import sys
import os
import subprocess

# Ajouter le dossier parent au path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.config import settings


def run_sql_file(filename: str):
    """Exécute un fichier SQL"""
    filepath = os.path.join("scripts", filename)

    if not os.path.exists(filepath):
        print(f"⚠️  Fichier non trouvé: {filepath}")
        return False

    cmd = [
        "psql",
        "-U", settings.POSTGRES_USER,
        "-h", settings.POSTGRES_SERVER,
        "-p", settings.POSTGRES_PORT,
        "-d", settings.POSTGRES_DB,
        "-f", filepath
    ]

    try:
        print(f"📂 Exécution de {filename}...")
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            env={**os.environ, "PGPASSWORD": settings.POSTGRES_PASSWORD}
        )

        if result.returncode == 0:
            print(f"   ✅ {filename} exécuté avec succès")
            return True
        else:
            print(f"   ❌ Erreur lors de l'exécution de {filename}")
            print(f"   {result.stderr}")
            return False
    except FileNotFoundError:
        print(f"   ❌ psql non trouvé. Assurez-vous que PostgreSQL est installé")
        return False


def create_database():
    """Crée la base de données si elle n'existe pas"""
    cmd = [
        "psql",
        "-U", settings.POSTGRES_USER,
        "-h", settings.POSTGRES_SERVER,
        "-p", settings.POSTGRES_PORT,
        "-c", f"CREATE DATABASE {settings.POSTGRES_DB};"
    ]

    try:
        subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            env={**os.environ, "PGPASSWORD": settings.POSTGRES_PASSWORD}
        )
        print(f"✅ Base de données '{settings.POSTGRES_DB}' créée")
    except Exception:
        # La base existe probablement déjà
        print(f"ℹ️  Base de données '{settings.POSTGRES_DB}' existe déjà")


def main():
    """Fonction principale"""
    print("=" * 70)
    print("🚀 Initialisation complète de la base de données")
    print("=" * 70)
    print()

    # Configuration
    print("📋 Configuration:")
    print(f"   Serveur:   {settings.POSTGRES_SERVER}:{settings.POSTGRES_PORT}")
    print(f"   Base:      {settings.POSTGRES_DB}")
    print(f"   User:      {settings.POSTGRES_USER}")
    print()

    # Créer la base de données
    print("1️⃣  Création de la base de données...")
    create_database()
    print()

    # Charger le schéma
    print("2️⃣  Chargement du schéma...")
    if not run_sql_file("schema.sql"):
        print("❌ Échec du chargement du schéma")
        sys.exit(1)
    print()

    # Charger les données initiales
    print("3️⃣  Chargement des données initiales...")
    if not run_sql_file("seed_data.sql"):
        print("⚠️  Échec du chargement des données initiales (peut-être déjà chargées)")
    print()

    # Charger les données géographiques
    print("4️⃣  Chargement des données géographiques de Madagascar...")
    if not run_sql_file("seed_regions_madagascar.sql"):
        print("⚠️  Échec du chargement des données géographiques (peut-être déjà chargées)")
    print()

    # Créer l'utilisateur admin
    print("5️⃣  Création de l'utilisateur administrateur...")
    try:
        from create_admin import create_roles, create_admin_user
        from app.database import SessionLocal

        db = SessionLocal()
        try:
            roles = create_roles(db)
            admin = create_admin_user(db, roles)

            if admin:
                print("   ✅ Administrateur créé avec succès")
            else:
                print("   ℹ️  Administrateur existe déjà")
        finally:
            db.close()
    except Exception as e:
        print(f"   ❌ Erreur: {str(e)}")
    print()

    # Résumé
    print("=" * 70)
    print("✅ Initialisation terminée!")
    print("=" * 70)
    print()
    print("🎯 Prochaines étapes:")
    print("   1. Démarrer le serveur: ./run.sh")
    print("   2. Accéder à la doc: http://localhost:8000/docs")
    print("   3. Se connecter avec:")
    print(f"      Username: {settings.FIRST_SUPERUSER_USERNAME}")
    print(f"      Password: {settings.FIRST_SUPERUSER_PASSWORD}")
    print()
    print("⚠️  N'oubliez pas de changer le mot de passe admin!")
    print()


if __name__ == "__main__":
    main()
