#!/usr/bin/env python3
"""
Script de seed pour peupler la base de données avec des données de démonstration.
Exécuter avec: python -m scripts.seed_database

Ce script crée:
- 6 Provinces de Madagascar
- 22 Régions
- ~50 Communes représentatives
- 3 Exercices budgétaires (2022-2024)
- Plan comptable complet (recettes et dépenses)
- Données financières pour chaque commune/exercice
"""

import random
import sys
from datetime import date
from decimal import Decimal
from pathlib import Path

# Ajouter le répertoire parent au path pour les imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy.orm import Session
from app.database import SessionLocal, engine, Base
from app.models.comptabilite import PlanComptable, Exercice, DonneesRecettes, DonneesDepenses
from app.models.geographie import Province, Region, Commune
from app.models.enums import TypeMouvement, SectionBudgetaire, TypeCommune


# ============================================================================
# DONNÉES DE RÉFÉRENCE - GÉOGRAPHIE MADAGASCAR
# ============================================================================

PROVINCES_DATA = [
    {"code": "ANT", "nom": "Antananarivo"},
    {"code": "ANS", "nom": "Antsiranana"},
    {"code": "FIA", "nom": "Fianarantsoa"},
    {"code": "MAH", "nom": "Mahajanga"},
    {"code": "TOA", "nom": "Toamasina"},
    {"code": "TOL", "nom": "Toliara"},
]

REGIONS_DATA = [
    # Province Antananarivo
    {"code": "ANA", "nom": "Analamanga", "province_code": "ANT"},
    {"code": "BON", "nom": "Bongolava", "province_code": "ANT"},
    {"code": "ITA", "nom": "Itasy", "province_code": "ANT"},
    {"code": "VAK", "nom": "Vakinankaratra", "province_code": "ANT"},
    # Province Antsiranana
    {"code": "DIA", "nom": "Diana", "province_code": "ANS"},
    {"code": "SAV", "nom": "Sava", "province_code": "ANS"},
    # Province Fianarantsoa
    {"code": "AMS", "nom": "Amoron'i Mania", "province_code": "FIA"},
    {"code": "HMA", "nom": "Haute Matsiatra", "province_code": "FIA"},
    {"code": "IHO", "nom": "Ihorombe", "province_code": "FIA"},
    {"code": "VAT", "nom": "Vatovavy", "province_code": "FIA"},
    {"code": "FIT", "nom": "Fitovinany", "province_code": "FIA"},
    {"code": "ATS", "nom": "Atsimo-Atsinanana", "province_code": "FIA"},
    # Province Mahajanga
    {"code": "BET", "nom": "Betsiboka", "province_code": "MAH"},
    {"code": "BOE", "nom": "Boeny", "province_code": "MAH"},
    {"code": "MEL", "nom": "Melaky", "province_code": "MAH"},
    {"code": "SOF", "nom": "Sofia", "province_code": "MAH"},
    # Province Toamasina
    {"code": "ALA", "nom": "Alaotra-Mangoro", "province_code": "TOA"},
    {"code": "ANA2", "nom": "Analanjirofo", "province_code": "TOA"},
    {"code": "ATS2", "nom": "Atsinanana", "province_code": "TOA"},
    # Province Toliara
    {"code": "AND", "nom": "Androy", "province_code": "TOL"},
    {"code": "ANO", "nom": "Anosy", "province_code": "TOL"},
    {"code": "ATM", "nom": "Atsimo-Andrefana", "province_code": "TOL"},
    {"code": "MEN", "nom": "Menabe", "province_code": "TOL"},
]

# Communes représentatives par région
COMMUNES_DATA = [
    # Analamanga
    {"code": "ANT-001", "nom": "Antananarivo Renivohitra", "region_code": "ANA", "type": "urbaine", "population": 1275207},
    {"code": "ANT-002", "nom": "Antsirabe I", "region_code": "VAK", "type": "urbaine", "population": 238478},
    {"code": "ANT-003", "nom": "Ambohidratrimo", "region_code": "ANA", "type": "urbaine", "population": 45000},
    {"code": "ANT-004", "nom": "Arivonimamo", "region_code": "ITA", "type": "rurale", "population": 32000},
    # Diana
    {"code": "DIA-001", "nom": "Antsiranana I", "region_code": "DIA", "type": "urbaine", "population": 115000},
    {"code": "DIA-002", "nom": "Nosy Be", "region_code": "DIA", "type": "urbaine", "population": 45000},
    # Sava
    {"code": "SAV-001", "nom": "Sambava", "region_code": "SAV", "type": "urbaine", "population": 55000},
    {"code": "SAV-002", "nom": "Antalaha", "region_code": "SAV", "type": "urbaine", "population": 42000},
    # Haute Matsiatra
    {"code": "HMA-001", "nom": "Fianarantsoa I", "region_code": "HMA", "type": "urbaine", "population": 167227},
    {"code": "HMA-002", "nom": "Ambalavao", "region_code": "HMA", "type": "rurale", "population": 28000},
    # Boeny
    {"code": "BOE-001", "nom": "Mahajanga I", "region_code": "BOE", "type": "urbaine", "population": 220629},
    {"code": "BOE-002", "nom": "Marovoay", "region_code": "BOE", "type": "rurale", "population": 35000},
    # Atsinanana
    {"code": "ATS2-001", "nom": "Toamasina I", "region_code": "ATS2", "type": "urbaine", "population": 274667},
    {"code": "ATS2-002", "nom": "Brickaville", "region_code": "ATS2", "type": "rurale", "population": 22000},
    # Atsimo-Andrefana
    {"code": "ATM-001", "nom": "Toliara I", "region_code": "ATM", "type": "urbaine", "population": 156710},
    {"code": "ATM-002", "nom": "Sakaraha", "region_code": "ATM", "type": "rurale", "population": 18000},
    # Alaotra-Mangoro
    {"code": "ALA-001", "nom": "Ambatondrazaka", "region_code": "ALA", "type": "urbaine", "population": 52000},
    {"code": "ALA-002", "nom": "Moramanga", "region_code": "ALA", "type": "urbaine", "population": 45000},
    # Vakinankaratra
    {"code": "VAK-001", "nom": "Betafo", "region_code": "VAK", "type": "rurale", "population": 25000},
    {"code": "VAK-002", "nom": "Faratsiho", "region_code": "VAK", "type": "rurale", "population": 18000},
]


# ============================================================================
# PLAN COMPTABLE - STRUCTURE HIÉRARCHIQUE
# ============================================================================

PLAN_COMPTABLE_RECETTES = [
    # Fonctionnement - Niveau 1
    {"code": "70", "intitule": "IMPOTS SUR LES REVENUS", "niveau": 1, "section": "fonctionnement"},
    {"code": "701", "intitule": "Impôt sur les revenus fonciers", "niveau": 2, "section": "fonctionnement", "parent": "70"},
    {"code": "7010", "intitule": "Contribution foncière des propriétés bâties", "niveau": 3, "section": "fonctionnement", "parent": "701"},
    {"code": "7011", "intitule": "Contribution foncière des propriétés non bâties", "niveau": 3, "section": "fonctionnement", "parent": "701"},

    {"code": "71", "intitule": "IMPOTS SUR LE PATRIMOINE", "niveau": 1, "section": "fonctionnement"},
    {"code": "711", "intitule": "Taxe annexe à l'impôt foncier", "niveau": 2, "section": "fonctionnement", "parent": "71"},
    {"code": "7110", "intitule": "TAIF sur propriétés bâties", "niveau": 3, "section": "fonctionnement", "parent": "711"},

    {"code": "72", "intitule": "IMPOTS SUR LES BIENS ET SERVICES", "niveau": 1, "section": "fonctionnement"},
    {"code": "721", "intitule": "Taxes sur les transactions", "niveau": 2, "section": "fonctionnement", "parent": "72"},
    {"code": "7210", "intitule": "Droit de mutation", "niveau": 3, "section": "fonctionnement", "parent": "721"},

    {"code": "73", "intitule": "DROITS ET TAXES DIVERSES", "niveau": 1, "section": "fonctionnement"},
    {"code": "731", "intitule": "Droits d'enregistrement", "niveau": 2, "section": "fonctionnement", "parent": "73"},
    {"code": "7310", "intitule": "Droits sur actes civils", "niveau": 3, "section": "fonctionnement", "parent": "731"},

    {"code": "74", "intitule": "TRANSFERTS RECUS", "niveau": 1, "section": "fonctionnement"},
    {"code": "741", "intitule": "Dotations de l'État", "niveau": 2, "section": "fonctionnement", "parent": "74"},
    {"code": "7410", "intitule": "Dotation globale de fonctionnement", "niveau": 3, "section": "fonctionnement", "parent": "741"},

    {"code": "75", "intitule": "REVENUS DU PATRIMOINE", "niveau": 1, "section": "fonctionnement"},
    {"code": "751", "intitule": "Revenus des immeubles", "niveau": 2, "section": "fonctionnement", "parent": "75"},
    {"code": "7510", "intitule": "Loyers des bâtiments communaux", "niveau": 3, "section": "fonctionnement", "parent": "751"},

    {"code": "76", "intitule": "RISTOURNES ET REDEVANCES MINIERES", "niveau": 1, "section": "fonctionnement"},
    {"code": "761", "intitule": "Ristournes minières", "niveau": 2, "section": "fonctionnement", "parent": "76"},
    {"code": "7610", "intitule": "Ristourne minière - Quote-part commune", "niveau": 3, "section": "fonctionnement", "parent": "761"},

    {"code": "77", "intitule": "PRODUITS EXCEPTIONNELS", "niveau": 1, "section": "fonctionnement"},
    {"code": "771", "intitule": "Recettes diverses", "niveau": 2, "section": "fonctionnement", "parent": "77"},
    {"code": "7710", "intitule": "Amendes et pénalités", "niveau": 3, "section": "fonctionnement", "parent": "771"},

    # Investissement - Niveau 1
    {"code": "20", "intitule": "SUBVENTIONS D'INVESTISSEMENT", "niveau": 1, "section": "investissement"},
    {"code": "201", "intitule": "Subventions d'équipement de l'État", "niveau": 2, "section": "investissement", "parent": "20"},
    {"code": "2010", "intitule": "Dotations d'équipement des collectivités", "niveau": 3, "section": "investissement", "parent": "201"},

    {"code": "21", "intitule": "EMPRUNTS", "niveau": 1, "section": "investissement"},
    {"code": "211", "intitule": "Emprunts bancaires", "niveau": 2, "section": "investissement", "parent": "21"},
    {"code": "2110", "intitule": "Emprunts à long terme", "niveau": 3, "section": "investissement", "parent": "211"},

    {"code": "22", "intitule": "CESSIONS D'ACTIFS", "niveau": 1, "section": "investissement"},
    {"code": "221", "intitule": "Cessions d'immobilisations", "niveau": 2, "section": "investissement", "parent": "22"},
    {"code": "2210", "intitule": "Vente de terrains", "niveau": 3, "section": "investissement", "parent": "221"},
]

PLAN_COMPTABLE_DEPENSES = [
    # Fonctionnement - Niveau 1
    {"code": "60", "intitule": "CHARGES DE PERSONNEL", "niveau": 1, "section": "fonctionnement"},
    {"code": "601", "intitule": "Salaires et accessoires", "niveau": 2, "section": "fonctionnement", "parent": "60"},
    {"code": "6010", "intitule": "Personnel permanent", "niveau": 3, "section": "fonctionnement", "parent": "601"},
    {"code": "6011", "intitule": "Personnel contractuel", "niveau": 3, "section": "fonctionnement", "parent": "601"},

    {"code": "61", "intitule": "ACHATS DE BIENS", "niveau": 1, "section": "fonctionnement"},
    {"code": "611", "intitule": "Achats de biens de fonctionnement", "niveau": 2, "section": "fonctionnement", "parent": "61"},
    {"code": "6110", "intitule": "Fournitures et articles de bureau", "niveau": 3, "section": "fonctionnement", "parent": "611"},
    {"code": "6111", "intitule": "Carburants et lubrifiants", "niveau": 3, "section": "fonctionnement", "parent": "611"},

    {"code": "62", "intitule": "ACHATS DE SERVICES", "niveau": 1, "section": "fonctionnement"},
    {"code": "621", "intitule": "Services extérieurs", "niveau": 2, "section": "fonctionnement", "parent": "62"},
    {"code": "6210", "intitule": "Entretien et réparations", "niveau": 3, "section": "fonctionnement", "parent": "621"},
    {"code": "6211", "intitule": "Eau, électricité, téléphone", "niveau": 3, "section": "fonctionnement", "parent": "621"},

    {"code": "63", "intitule": "SUBVENTIONS ET TRANSFERTS", "niveau": 1, "section": "fonctionnement"},
    {"code": "631", "intitule": "Subventions aux associations", "niveau": 2, "section": "fonctionnement", "parent": "63"},
    {"code": "6310", "intitule": "Associations sportives et culturelles", "niveau": 3, "section": "fonctionnement", "parent": "631"},

    {"code": "64", "intitule": "CHARGES FINANCIERES", "niveau": 1, "section": "fonctionnement"},
    {"code": "641", "intitule": "Intérêts des emprunts", "niveau": 2, "section": "fonctionnement", "parent": "64"},
    {"code": "6410", "intitule": "Intérêts emprunts bancaires", "niveau": 3, "section": "fonctionnement", "parent": "641"},

    {"code": "65", "intitule": "DEPENSES IMPREVUES", "niveau": 1, "section": "fonctionnement"},
    {"code": "651", "intitule": "Dépenses imprévues", "niveau": 2, "section": "fonctionnement", "parent": "65"},
    {"code": "6510", "intitule": "Crédits d'urgence", "niveau": 3, "section": "fonctionnement", "parent": "651"},

    # Investissement - Niveau 1
    {"code": "20D", "intitule": "IMMOBILISATIONS INCORPORELLES", "niveau": 1, "section": "investissement"},
    {"code": "201D", "intitule": "Logiciels et brevets", "niveau": 2, "section": "investissement", "parent": "20D"},
    {"code": "2010D", "intitule": "Logiciels informatiques", "niveau": 3, "section": "investissement", "parent": "201D"},

    {"code": "21D", "intitule": "IMMOBILISATIONS CORPORELLES", "niveau": 1, "section": "investissement"},
    {"code": "211D", "intitule": "Constructions", "niveau": 2, "section": "investissement", "parent": "21D"},
    {"code": "2110D", "intitule": "Bâtiments administratifs", "niveau": 3, "section": "investissement", "parent": "211D"},
    {"code": "2111D", "intitule": "Écoles et centres de santé", "niveau": 3, "section": "investissement", "parent": "211D"},

    {"code": "22D", "intitule": "REMBOURSEMENT D'EMPRUNTS", "niveau": 1, "section": "investissement"},
    {"code": "221D", "intitule": "Remboursement du capital", "niveau": 2, "section": "investissement", "parent": "22D"},
    {"code": "2210D", "intitule": "Amortissement emprunts bancaires", "niveau": 3, "section": "investissement", "parent": "221D"},
]


# ============================================================================
# FONCTIONS DE SEED
# ============================================================================

def seed_provinces(db: Session) -> dict:
    """Crée les 6 provinces de Madagascar."""
    print("  Création des provinces...")
    provinces = {}
    for data in PROVINCES_DATA:
        province = Province(code=data["code"], nom=data["nom"])
        db.add(province)
        db.flush()
        provinces[data["code"]] = province
    return provinces


def seed_regions(db: Session, provinces: dict) -> dict:
    """Crée les 22 régions de Madagascar."""
    print("  Création des régions...")
    regions = {}
    for data in REGIONS_DATA:
        region = Region(
            code=data["code"],
            nom=data["nom"],
            province_id=provinces[data["province_code"]].id
        )
        db.add(region)
        db.flush()
        regions[data["code"]] = region
    return regions


def seed_communes(db: Session, regions: dict) -> list:
    """Crée les communes représentatives."""
    print("  Création des communes...")
    communes = []
    for data in COMMUNES_DATA:
        commune = Commune(
            code=data["code"],
            nom=data["nom"],
            region_id=regions[data["region_code"]].id,
            type_commune=TypeCommune.URBAINE if data["type"] == "urbaine" else TypeCommune.RURALE,
            population=data.get("population"),
        )
        db.add(commune)
        db.flush()
        communes.append(commune)
    return communes


def seed_exercices(db: Session) -> list:
    """Crée les exercices budgétaires 2022-2024."""
    print("  Création des exercices budgétaires...")
    exercices = []
    for annee in [2022, 2023, 2024]:
        exercice = Exercice(
            annee=annee,
            libelle=f"Exercice {annee}",
            date_debut=date(annee, 1, 1),
            date_fin=date(annee, 12, 31),
            cloture=(annee < 2024)  # 2022 et 2023 clôturés
        )
        db.add(exercice)
        db.flush()
        exercices.append(exercice)
    return exercices


def seed_plan_comptable(db: Session) -> None:
    """Crée le plan comptable complet."""
    print("  Création du plan comptable...")
    ordre = 0

    # Recettes
    for data in PLAN_COMPTABLE_RECETTES:
        ordre += 1
        compte = PlanComptable(
            code=data["code"],
            intitule=data["intitule"],
            niveau=data["niveau"],
            type_mouvement=TypeMouvement.RECETTE,
            section=SectionBudgetaire.FONCTIONNEMENT if data["section"] == "fonctionnement" else SectionBudgetaire.INVESTISSEMENT,
            parent_code=data.get("parent"),
            est_sommable=(data["niveau"] == 1),
            ordre_affichage=ordre,
            actif=True,
        )
        db.add(compte)

    # Dépenses
    for data in PLAN_COMPTABLE_DEPENSES:
        ordre += 1
        compte = PlanComptable(
            code=data["code"],
            intitule=data["intitule"],
            niveau=data["niveau"],
            type_mouvement=TypeMouvement.DEPENSE,
            section=SectionBudgetaire.FONCTIONNEMENT if data["section"] == "fonctionnement" else SectionBudgetaire.INVESTISSEMENT,
            parent_code=data.get("parent"),
            est_sommable=(data["niveau"] == 1),
            ordre_affichage=ordre,
            actif=True,
        )
        db.add(compte)

    db.flush()


def seed_donnees_financieres(db: Session, communes: list, exercices: list) -> None:
    """Crée des données financières réalistes pour chaque commune/exercice."""
    print("  Création des données financières...")

    # Récupérer tous les comptes de niveau 3 (lignes de détail)
    comptes_recettes = db.query(PlanComptable).filter(
        PlanComptable.type_mouvement == TypeMouvement.RECETTE,
        PlanComptable.niveau == 3
    ).all()

    comptes_depenses = db.query(PlanComptable).filter(
        PlanComptable.type_mouvement == TypeMouvement.DEPENSE,
        PlanComptable.niveau == 3
    ).all()

    for commune in communes:
        # Facteur de taille basé sur la population
        facteur_taille = (commune.population or 50000) / 50000

        for exercice in exercices:
            # Générer des données de recettes
            for compte in comptes_recettes:
                # Variation aléatoire mais réaliste
                base_montant = random.randint(500000, 5000000) * facteur_taille

                budget_primitif = Decimal(str(int(base_montant)))
                budget_additionnel = Decimal(str(int(base_montant * random.uniform(0.05, 0.15))))
                modifications = Decimal(str(int(base_montant * random.uniform(-0.05, 0.1))))
                previsions = budget_primitif + budget_additionnel + modifications

                # Taux d'exécution variable (70-100%)
                taux_exec = random.uniform(0.7, 1.0)
                or_admis = Decimal(str(int(float(previsions) * taux_exec)))
                recouvrement = Decimal(str(int(float(or_admis) * random.uniform(0.85, 0.98))))
                reste = or_admis - recouvrement

                recette = DonneesRecettes(
                    commune_id=commune.id,
                    exercice_id=exercice.id,
                    compte_code=compte.code,
                    budget_primitif=budget_primitif,
                    budget_additionnel=budget_additionnel,
                    modifications=modifications,
                    previsions_definitives=previsions,
                    or_admis=or_admis,
                    recouvrement=recouvrement,
                    reste_a_recouvrer=reste,
                    valide=exercice.cloture,
                )
                db.add(recette)

            # Générer des données de dépenses
            for compte in comptes_depenses:
                base_montant = random.randint(400000, 4000000) * facteur_taille

                budget_primitif = Decimal(str(int(base_montant)))
                budget_additionnel = Decimal(str(int(base_montant * random.uniform(0.05, 0.12))))
                modifications = Decimal(str(int(base_montant * random.uniform(-0.03, 0.08))))
                previsions = budget_primitif + budget_additionnel + modifications

                # Taux d'exécution variable (65-95%)
                taux_exec = random.uniform(0.65, 0.95)
                engagement = Decimal(str(int(float(previsions) * min(taux_exec * 1.05, 1.0))))
                mandat_admis = Decimal(str(int(float(engagement) * random.uniform(0.90, 1.0))))
                paiement = Decimal(str(int(float(mandat_admis) * random.uniform(0.85, 0.98))))
                reste = mandat_admis - paiement

                depense = DonneesDepenses(
                    commune_id=commune.id,
                    exercice_id=exercice.id,
                    compte_code=compte.code,
                    budget_primitif=budget_primitif,
                    budget_additionnel=budget_additionnel,
                    modifications=modifications,
                    previsions_definitives=previsions,
                    engagement=engagement,
                    mandat_admis=mandat_admis,
                    paiement=paiement,
                    reste_a_payer=reste,
                    valide=exercice.cloture,
                )
                db.add(depense)

    db.flush()


def clear_existing_data(db: Session) -> None:
    """Supprime toutes les données existantes (pour un seed propre)."""
    print("  Nettoyage des données existantes...")

    # Importer les modèles avec des FK vers nos tables
    from app.models.projets_miniers import RevenuMinier, ProjetCommune
    from app.models.documents import Document
    from app.models.cms import PageCompteAdministratif, SectionCMS

    # Supprimer dans l'ordre des dépendances (tables enfants d'abord)
    try:
        db.query(SectionCMS).delete()
    except Exception:
        pass
    try:
        db.query(PageCompteAdministratif).delete()
    except Exception:
        pass
    try:
        db.query(Document).delete()
    except Exception:
        pass
    try:
        db.query(RevenuMinier).delete()
    except Exception:
        pass
    try:
        db.query(ProjetCommune).delete()
    except Exception:
        pass

    db.query(DonneesDepenses).delete()
    db.query(DonneesRecettes).delete()
    db.query(PlanComptable).delete()
    db.query(Exercice).delete()
    db.query(Commune).delete()
    db.query(Region).delete()
    db.query(Province).delete()
    db.commit()


def run_seed():
    """Exécute le processus de seed complet."""
    print("\n" + "=" * 60)
    print("SEED DE LA BASE DE DONNÉES - Collectivités Territoriales")
    print("=" * 60 + "\n")

    db = SessionLocal()

    try:
        # Nettoyage
        clear_existing_data(db)

        # Seed dans l'ordre des dépendances
        print("\n[1/6] Provinces...")
        provinces = seed_provinces(db)

        print("[2/6] Régions...")
        regions = seed_regions(db, provinces)

        print("[3/6] Communes...")
        communes = seed_communes(db, regions)

        print("[4/6] Exercices...")
        exercices = seed_exercices(db)

        print("[5/6] Plan comptable...")
        seed_plan_comptable(db)

        print("[6/6] Données financières...")
        seed_donnees_financieres(db, communes, exercices)

        # Commit final
        db.commit()

        # Statistiques
        print("\n" + "-" * 60)
        print("SEED TERMINÉ AVEC SUCCÈS!")
        print("-" * 60)
        print(f"  • {len(PROVINCES_DATA)} provinces")
        print(f"  • {len(REGIONS_DATA)} régions")
        print(f"  • {len(communes)} communes")
        print(f"  • {len(exercices)} exercices (2022-2024)")
        print(f"  • {len(PLAN_COMPTABLE_RECETTES) + len(PLAN_COMPTABLE_DEPENSES)} comptes")
        total_donnees = len(communes) * len(exercices) * (
            sum(1 for c in PLAN_COMPTABLE_RECETTES if c["niveau"] == 3) +
            sum(1 for c in PLAN_COMPTABLE_DEPENSES if c["niveau"] == 3)
        )
        print(f"  • ~{total_donnees} lignes de données financières")
        print("\n")

    except Exception as e:
        db.rollback()
        print(f"\n❌ ERREUR: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    run_seed()
