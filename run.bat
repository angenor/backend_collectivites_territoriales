@echo off
REM Script de démarrage du serveur FastAPI avec .venv pour Windows

echo 🚀 Démarrage du serveur FastAPI...

REM Vérifier que .venv existe
if not exist ".venv\" (
    echo ❌ Erreur: .venv n'existe pas. Créez-le avec: python -m venv .venv
    exit /b 1
)

REM Vérifier que les dépendances sont installées
if not exist ".venv\Scripts\uvicorn.exe" (
    echo ⚠️  Installation des dépendances...
    .venv\Scripts\pip install -r requirements.txt
)

REM Démarrer le serveur
echo ✅ Serveur démarré sur http://localhost:8000
echo 📚 Documentation: http://localhost:8000/docs
echo Appuyez sur Ctrl+C pour arrêter le serveur
echo.

.venv\Scripts\uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
