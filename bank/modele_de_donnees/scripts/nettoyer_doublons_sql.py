#!/usr/bin/env python3
"""
Script pour nettoyer les doublons dans le fichier d'insertion des rubriques budgétaires
"""
import re
from pathlib import Path

def nettoyer_doublons():
    """Supprime les doublons du fichier SQL en gardant la première occurrence de chaque code"""

    # Chemins
    input_file = Path(__file__).parent.parent / 'migrations' / '002_insertion_rubriques_budgetaires.sql'
    output_file = Path(__file__).parent.parent / 'migrations' / '002_insertion_rubriques_budgetaires_clean.sql'

    print(f"Lecture du fichier: {input_file}")
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Séparer l'en-tête et les insertions
    lines = content.split('\n')
    header_lines = []
    insert_blocks = []
    current_block = []
    in_insert = False

    for line in lines:
        if line.strip().startswith('INSERT INTO rubriques_budgetaires'):
            in_insert = True
            current_block = [line]
        elif in_insert:
            current_block.append(line)
            if line.strip().endswith(');'):
                # Fin du bloc INSERT
                insert_blocks.append('\n'.join(current_block))
                current_block = []
                in_insert = False
        else:
            if not insert_blocks:  # Encore dans l'en-tête
                header_lines.append(line)

    print(f"Trouvé {len(insert_blocks)} blocs INSERT")

    # Extraire les codes de chaque bloc
    pattern = r"VALUES \(\s*'([^']+)',"
    seen_codes = set()
    unique_blocks = []
    duplicates_removed = []

    for block in insert_blocks:
        match = re.search(pattern, block)
        if match:
            code = match.group(1)
            if code not in seen_codes:
                seen_codes.add(code)
                unique_blocks.append(block)
            else:
                duplicates_removed.append(code)
                print(f"  - Doublons supprimé: code '{code}'")

    print(f"\n=== RÉSUMÉ ===")
    print(f"Insertions originales: {len(insert_blocks)}")
    print(f"Doublons supprimés: {len(duplicates_removed)}")
    print(f"Insertions finales: {len(unique_blocks)}")

    # Reconstruire le fichier
    output_content = '\n'.join(header_lines) + '\n\n'

    # Grouper par niveau pour l'organisation
    niveau1_blocks = [b for b in unique_blocks if "'NULL,\n    1," in b or "NULL,\n    1," in b]
    niveau2_blocks = [b for b in unique_blocks if "'NULL,\n    2," in b or "NULL,\n    2," in b or
                      "(SELECT id FROM rubriques_budgetaires" in b and ",\n    2," in b]
    autres_blocks = [b for b in unique_blocks if b not in niveau1_blocks and b not in niveau2_blocks]

    # Écrire Niveau 1
    output_content += "-- ========================================\n"
    output_content += "-- Niveau 1\n"
    output_content += "-- ========================================\n\n"
    output_content += '\n\n'.join(niveau1_blocks)
    output_content += '\n\n'

    # Écrire Niveau 2
    if niveau2_blocks:
        output_content += "-- ========================================\n"
        output_content += "-- Niveau 2\n"
        output_content += "-- ========================================\n\n"
        output_content += '\n\n'.join(niveau2_blocks)
        output_content += '\n\n'

    # Écrire autres niveaux
    if autres_blocks:
        output_content += "-- ========================================\n"
        output_content += "-- Autres niveaux\n"
        output_content += "-- ========================================\n\n"
        output_content += '\n\n'.join(autres_blocks)
        output_content += '\n\n'

    # Réactiver les triggers
    output_content += "-- Réactiver les triggers\n"
    output_content += "ALTER TABLE rubriques_budgetaires ENABLE TRIGGER USER;\n"

    # Écrire le fichier nettoyé
    print(f"\nÉcriture du fichier nettoyé: {output_file}")
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(output_content)

    print(f"✓ Fichier nettoyé créé avec succès!")
    print(f"\nCodes dupliqués supprimés: {sorted(set(duplicates_removed))}")

    return output_file

if __name__ == '__main__':
    nettoyer_doublons()
