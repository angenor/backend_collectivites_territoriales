#!/bin/bash
set -e

# =============================================================================
# Script d'initialisation de la base de données
# Exécute les scripts SQL dans l'ordre correct
# =============================================================================

SCRIPTS_DIR="/scripts"

echo "=========================================="
echo " Initialisation de la base de données"
echo " Base: ${POSTGRES_DB}"
echo " Serveur: ${POSTGRES_SERVER}:${POSTGRES_PORT}"
echo "=========================================="

# Attendre que PostgreSQL soit prêt
echo "[1/5] Vérification de la connexion PostgreSQL..."
until PGPASSWORD="${POSTGRES_PASSWORD}" psql -h "${POSTGRES_SERVER}" -p "${POSTGRES_PORT}" -U "${POSTGRES_USER}" -d "${POSTGRES_DB}" -c '\q' 2>/dev/null; do
    echo "  PostgreSQL n'est pas encore prêt, attente 2s..."
    sleep 2
done
echo "  PostgreSQL est prêt."

# Fonction pour exécuter un script SQL
run_sql() {
    local file="$1"
    local description="$2"

    if [ ! -f "${SCRIPTS_DIR}/${file}" ]; then
        echo "  ERREUR: Fichier ${file} introuvable!"
        exit 1
    fi

    echo "  Exécution de ${file} (${description})..."
    PGPASSWORD="${POSTGRES_PASSWORD}" psql \
        -h "${POSTGRES_SERVER}" \
        -p "${POSTGRES_PORT}" \
        -U "${POSTGRES_USER}" \
        -d "${POSTGRES_DB}" \
        -f "${SCRIPTS_DIR}/${file}" \
        --quiet \
        --set ON_ERROR_STOP=1
    echo "  ${file} OK"
}

# Exécution des scripts dans l'ordre
echo "[2/5] Création du schéma (tables, vues, triggers)..."
run_sql "schema.sql" "25 tables, 5 vues, triggers"

echo "[3/5] Insertion du plan comptable..."
run_sql "seed_plan_comptable.sql" "~300 comptes hiérarchiques"

echo "[4/5] Insertion des régions de Madagascar..."
run_sql "seed_regions_madagascar.sql" "6 provinces, 22 régions, communes"

echo "[5/5] Insertion des données de démonstration..."
run_sql "seed_data.sql" "sociétés minières, projets, données financières"

echo ""
echo "=========================================="
echo " Initialisation terminée avec succès!"
echo "=========================================="
