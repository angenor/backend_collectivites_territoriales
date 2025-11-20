#!/usr/bin/env python3
"""
Script d'extraction des rubriques budgétaires depuis le fichier Excel
Génère un fichier SQL d'insertion pour peupler la table rubriques_budgetaires
"""

import pandas as pd
import re
from pathlib import Path
from typing import List, Dict, Optional

# Chemins des fichiers
EXCEL_FILE = Path(__file__).parent.parent.parent / "cahier_des_charges" / "Tableaux_de_Compte_Administratif.xlsx"
OUTPUT_SQL = Path(__file__).parent.parent / "migrations" / "002_insertion_rubriques_budgetaires.sql"

class RubriqueBudgetaire:
    """Représente une rubrique budgétaire avec sa hiérarchie"""

    def __init__(self, code: str, intitule: str, type_rubrique: str, section: str, niveau: int = 1, parent_code: Optional[str] = None):
        self.code = str(code).strip() if code else ""
        self.intitule = intitule.strip() if intitule else ""
        self.type_rubrique = type_rubrique  # 'recette' ou 'depense'
        self.section = section  # 'fonctionnement' ou 'investissement'
        self.niveau = niveau
        self.parent_code = parent_code

    def to_sql_values(self, parent_id_expr: str = "NULL", ordre: int = 0) -> str:
        """Génère la partie VALUES de l'INSERT SQL"""
        code_safe = self.code.replace("'", "''")
        intitule_safe = self.intitule.replace("'", "''")

        return f"""(
    '{code_safe}',
    '{intitule_safe}',
    NULL,  -- categorie_id (à définir manuellement si nécessaire)
    '{self.type_rubrique}',
    '{self.section}',
    {parent_id_expr},
    {self.niveau},
    {ordre},
    FALSE,  -- est_calculee
    NULL,   -- formule_calcul
    TRUE,   -- est_active
    NULL    -- description
)"""

def detecter_niveau_compte(code: str) -> int:
    """
    Détermine le niveau hiérarchique d'un compte
    Exemples: '70' -> 1, '708' -> 2, '7080' -> 3
    """
    if not code or not isinstance(code, str):
        return 1

    code = code.strip()

    # Niveau 1: codes à 2 chiffres (70, 71, 72)
    if len(code) == 2 and code.isdigit():
        return 1

    # Niveau 2: codes à 3 chiffres (708, 714, 715)
    if len(code) == 3 and code.isdigit():
        return 2

    # Niveau 3: codes à 4 chiffres (7080, 7140, 7151)
    if len(code) == 4 and code.isdigit():
        return 3

    # Codes spéciaux (119, 110, 12, 10, etc.)
    if code.isdigit() and len(code) <= 3:
        return 1

    return 1

def trouver_code_parent(code: str) -> Optional[str]:
    """
    Trouve le code parent d'un compte dans la hiérarchie
    Exemples: '7080' -> '708', '708' -> '70', '70' -> None
    """
    if not code or not isinstance(code, str):
        return None

    code = code.strip()
    niveau = detecter_niveau_compte(code)

    if niveau == 1:
        return None
    elif niveau == 2 and len(code) == 3:
        return code[:2]  # '708' -> '70'
    elif niveau == 3 and len(code) == 4:
        return code[:3]  # '7080' -> '708'

    return None

def extraire_rubriques_depuis_excel() -> List[RubriqueBudgetaire]:
    """Extrait toutes les rubriques depuis les feuilles RECETTE et DEPENSES"""

    rubriques = []

    # ========================================================================
    # EXTRACTION DES RECETTES
    # ========================================================================
    print("📊 Extraction des recettes...")
    df_recettes = pd.read_excel(EXCEL_FILE, sheet_name='RECETTE', header=None)

    # Les données commencent à la ligne 6 (index 6)
    # Colonnes: 1=Compte niveau 1, 2=Compte niveau 2, 3=Compte niveau 3, 4=Intitulé
    current_section = 'fonctionnement'

    for idx, row in df_recettes.iterrows():
        if idx < 6:  # Sauter l'en-tête
            continue

        # Détecter le changement de section
        if pd.notna(row[1]) and "INVESTISSEMENT" in str(row[1]).upper():
            current_section = 'investissement'
            continue

        # Extraire les codes et intitulés
        code_n1 = row[1] if pd.notna(row[1]) else None
        code_n2 = row[2] if pd.notna(row[2]) else None
        code_n3 = row[3] if pd.notna(row[3]) else None
        intitule = row[4] if pd.notna(row[4]) else ""

        # Ignorer les lignes vides ou de titre
        if not any([code_n1, code_n2, code_n3]) or not intitule:
            continue

        if str(intitule).strip().upper() in ['INTITULES', 'COMPTE', '']:
            continue

        # Déterminer le code et le niveau
        if pd.notna(code_n3) and str(code_n3).replace('.0', '').strip():
            code = str(code_n3).replace('.0', '').strip()
        elif pd.notna(code_n2) and str(code_n2).replace('.0', '').strip():
            code = str(code_n2).replace('.0', '').strip()
        elif pd.notna(code_n1) and str(code_n1).replace('.0', '').strip():
            code = str(code_n1).replace('.0', '').strip()
        else:
            continue

        # Vérifier que le code est numérique
        if not code.isdigit():
            continue

        niveau = detecter_niveau_compte(code)
        parent_code = trouver_code_parent(code)

        rubrique = RubriqueBudgetaire(
            code=code,
            intitule=intitule,
            type_rubrique='recette',
            section=current_section,
            niveau=niveau,
            parent_code=parent_code
        )

        rubriques.append(rubrique)

    print(f"✅ {len(rubriques)} recettes extraites")

    # ========================================================================
    # EXTRACTION DES DÉPENSES
    # ========================================================================
    print("📊 Extraction des dépenses...")
    df_depenses = pd.read_excel(EXCEL_FILE, sheet_name='DEPENSES', header=None)

    current_section = 'fonctionnement'
    nb_depenses_initial = len(rubriques)

    for idx, row in df_depenses.iterrows():
        if idx < 8:  # Sauter l'en-tête
            continue

        # Détecter le changement de section
        if pd.notna(row[1]) and "INVESTISSEMENT" in str(row[1]).upper():
            current_section = 'investissement'
            continue

        # Extraire les codes et intitulés
        code_n1 = row[1] if pd.notna(row[1]) else None
        code_n2 = row[2] if pd.notna(row[2]) else None
        code_n3 = row[3] if pd.notna(row[3]) else None
        intitule = row[4] if pd.notna(row[4]) else ""

        # Ignorer les lignes vides ou de titre
        if not any([code_n1, code_n2, code_n3]) or not intitule:
            continue

        if str(intitule).strip().upper() in ['INTITULES', 'COMPTE', '', 'PROGRAMME :']:
            continue

        # Déterminer le code et le niveau
        if pd.notna(code_n3) and str(code_n3).replace('.0', '').strip():
            code = str(code_n3).replace('.0', '').strip()
        elif pd.notna(code_n2) and str(code_n2).replace('.0', '').strip():
            code = str(code_n2).replace('.0', '').strip()
        elif pd.notna(code_n1) and str(code_n1).replace('.0', '').strip():
            code = str(code_n1).replace('.0', '').strip()
        else:
            continue

        # Vérifier que le code est numérique
        if not code.isdigit():
            continue

        niveau = detecter_niveau_compte(code)
        parent_code = trouver_code_parent(code)

        rubrique = RubriqueBudgetaire(
            code=code,
            intitule=intitule,
            type_rubrique='depense',
            section=current_section,
            niveau=niveau,
            parent_code=parent_code
        )

        rubriques.append(rubrique)

    nb_depenses = len(rubriques) - nb_depenses_initial
    print(f"✅ {nb_depenses} dépenses extraites")

    return rubriques

def generer_sql_insertion(rubriques: List[RubriqueBudgetaire]) -> str:
    """Génère le script SQL d'insertion avec gestion des relations parent-enfant"""

    sql_lines = [
        "-- ============================================================================",
        "-- INSERTION DES RUBRIQUES BUDGÉTAIRES DEPUIS EXCEL",
        "-- ============================================================================",
        "-- Généré automatiquement depuis Tableaux_de_Compte_Administratif.xlsx",
        f"-- Nombre total de rubriques: {len(rubriques)}",
        "-- ============================================================================",
        "",
        "-- Désactiver temporairement les triggers utilisateur pour améliorer les performances",
        "ALTER TABLE rubriques_budgetaires DISABLE TRIGGER USER;",
        "",
        "-- Supprimer les rubriques existantes (si nécessaire)",
        "-- TRUNCATE TABLE rubriques_budgetaires CASCADE;",
        "",
    ]

    # Organiser les rubriques par niveau pour insertion dans le bon ordre
    rubriques_par_niveau = {1: [], 2: [], 3: []}

    for rubrique in rubriques:
        if rubrique.niveau in rubriques_par_niveau:
            rubriques_par_niveau[rubrique.niveau].append(rubrique)

    # Insérer niveau par niveau
    for niveau in [1, 2, 3]:
        if not rubriques_par_niveau[niveau]:
            continue

        sql_lines.append(f"-- ========================================")
        sql_lines.append(f"-- Niveau {niveau}")
        sql_lines.append(f"-- ========================================")
        sql_lines.append("")

        for idx, rubrique in enumerate(rubriques_par_niveau[niveau]):
            # Déterminer l'expression parent_id
            if rubrique.parent_code:
                parent_id_expr = f"(SELECT id FROM rubriques_budgetaires WHERE code = '{rubrique.parent_code}' LIMIT 1)"
            else:
                parent_id_expr = "NULL"

            sql_lines.append(f"INSERT INTO rubriques_budgetaires (")
            sql_lines.append("    code, intitule, categorie_id, type, section,")
            sql_lines.append("    parent_id, niveau, ordre, est_calculee, formule_calcul, est_active, description")
            sql_lines.append(f") VALUES {rubrique.to_sql_values(parent_id_expr, idx)};")
            sql_lines.append("")

    sql_lines.extend([
        "",
        "-- Réactiver les triggers utilisateur",
        "ALTER TABLE rubriques_budgetaires ENABLE TRIGGER USER;",
        "",
        "-- Vérification",
        "SELECT",
        "    type,",
        "    section,",
        "    niveau,",
        "    COUNT(*) as nombre_rubriques",
        "FROM rubriques_budgetaires",
        "GROUP BY type, section, niveau",
        "ORDER BY type, section, niveau;",
        "",
        "-- ============================================================================",
        "-- FIN DE L'INSERTION",
        "-- ============================================================================",
    ])

    return "\n".join(sql_lines)

def main():
    """Fonction principale"""
    print("🚀 Extraction des rubriques budgétaires depuis Excel")
    print(f"📁 Fichier source: {EXCEL_FILE}")
    print(f"📁 Fichier destination: {OUTPUT_SQL}")
    print("")

    # Vérifier que le fichier Excel existe
    if not EXCEL_FILE.exists():
        print(f"❌ Erreur: Le fichier {EXCEL_FILE} n'existe pas")
        return 1

    # Extraire les rubriques
    rubriques = extraire_rubriques_depuis_excel()

    # Statistiques
    print("")
    print("📊 Statistiques:")
    print(f"  - Total rubriques: {len(rubriques)}")

    recettes = [r for r in rubriques if r.type_rubrique == 'recette']
    depenses = [r for r in rubriques if r.type_rubrique == 'depense']

    print(f"  - Recettes: {len(recettes)}")
    print(f"  - Dépenses: {len(depenses)}")

    for niveau in [1, 2, 3]:
        nb = len([r for r in rubriques if r.niveau == niveau])
        print(f"  - Niveau {niveau}: {nb}")

    # Générer le SQL
    print("")
    print("📝 Génération du fichier SQL...")
    sql_content = generer_sql_insertion(rubriques)

    # Créer le répertoire si nécessaire
    OUTPUT_SQL.parent.mkdir(parents=True, exist_ok=True)

    # Écrire le fichier
    OUTPUT_SQL.write_text(sql_content, encoding='utf-8')

    print(f"✅ Fichier généré: {OUTPUT_SQL}")
    print(f"📦 Taille: {OUTPUT_SQL.stat().st_size} octets")
    print("")
    print("🎉 Extraction terminée avec succès!")

    return 0

if __name__ == "__main__":
    exit(main())
