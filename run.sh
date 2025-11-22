#!/bin/bash
# Script de démarrage du serveur FastAPI avec .venv

# Couleurs pour les messages
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🚀 Démarrage du serveur FastAPI...${NC}"

# Vérifier que .venv existe
if [ ! -d ".venv" ]; then
    echo "❌ Erreur: .venv n'existe pas. Créez-le avec: python3 -m venv .venv"
    exit 1
fi

# Vérifier que les dépendances sont installées
if [ ! -f ".venv/bin/uvicorn" ]; then
    echo "⚠️  Installation des dépendances..."
    .venv/bin/pip install -r requirements.txt
fi

# Démarrer le serveur
echo -e "${GREEN}✅ Serveur démarré sur http://localhost:8000${NC}"
echo -e "${GREEN}📚 Documentation: http://localhost:8000/docs${NC}"
echo -e "${BLUE}Appuyez sur Ctrl+C pour arrêter le serveur${NC}"
echo ""

.venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
