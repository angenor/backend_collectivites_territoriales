# 🎉 Nouveaux Endpoints Backend - Gestion des Rôles

## ✅ Fichiers Créés/Modifiés

### 1. Nouveau endpoint : [app/api/v1/endpoints/roles.py](app/api/v1/endpoints/roles.py)

Endpoints créés :
- `GET /api/v1/roles/` - Liste tous les rôles
- `GET /api/v1/roles/{role_id}` - Détails d'un rôle par ID
- `GET /api/v1/roles/code/{code}` - Détails d'un rôle par code (ex: LECTEUR)
- `POST /api/v1/roles/` - Créer un nouveau rôle (authentifié)
- `PUT /api/v1/roles/{role_id}` - Modifier un rôle (authentifié)
- `DELETE /api/v1/roles/{role_id}` - Désactiver un rôle (authentifié)

### 2. Schémas mis à jour : [app/schemas/utilisateurs.py](app/schemas/utilisateurs.py)

Ajouts :
- `RoleUpdate` - Schéma pour la modification de rôles
- `RoleResponse` - Alias pour `Role` (compatibilité frontend)

### 3. Router enregistré : [app/api/v1/api.py](app/api/v1/api.py)

Le router `roles` a été ajouté avec le préfixe `/roles`.

---

## 🚀 Comment Redémarrer le Backend

### 1. Arrêter le serveur actuel

Dans le terminal où tourne le backend :
- Appuyez sur `Ctrl + C`

### 2. Redémarrer le serveur

```bash
cd backend_collectivites_territoriales

# Activer l'environnement virtuel
source .venv/bin/activate

# Lancer le serveur
./run.sh

# Ou directement avec uvicorn :
# uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 3. Vérifier que le serveur démarre

Vous devriez voir :
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

---

## 🧪 Tester les Nouveaux Endpoints

### 1. Tester avec curl

```bash
# Récupérer tous les rôles
curl http://localhost:8000/api/v1/roles/

# Récupérer le rôle LECTEUR par code
curl http://localhost:8000/api/v1/roles/code/LECTEUR
```

**Résultat attendu** :
```json
[
  {
    "id": "...",
    "code": "ADMIN",
    "nom": "Administrateur",
    "description": "Administrateur système avec tous les droits",
    "permissions": ["all"],
    "actif": true,
    "created_at": "...",
    "updated_at": "..."
  },
  {
    "id": "...",
    "code": "EDITEUR",
    "nom": "Éditeur",
    "description": "Éditeur de contenu avec droits limités",
    "permissions": ["read", "create", "update"],
    "actif": true,
    "created_at": "...",
    "updated_at": "..."
  },
  {
    "id": "...",
    "code": "LECTEUR",
    "nom": "Lecteur",
    "description": "Utilisateur en lecture seule",
    "permissions": ["read"],
    "actif": true,
    "created_at": "...",
    "updated_at": "..."
  }
]
```

### 2. Tester avec Swagger UI

1. Ouvrez http://localhost:8000/docs
2. Cherchez la section **"Rôles"**
3. Testez l'endpoint `GET /api/v1/roles/`
4. Cliquez sur "Try it out" puis "Execute"

### 3. Vérifier avec le Frontend

Le frontend récupérera automatiquement le rôle LECTEUR lors de l'inscription !

---

## 🎯 Test de l'Inscription Frontend

### 1. Vérifier que les deux serveurs tournent

**Backend** : http://localhost:8000
```bash
curl http://localhost:8000/api/v1/roles/
# Doit retourner la liste des rôles
```

**Frontend** : http://localhost:3000 (ou 3001)
```bash
# Dans un autre terminal
cd frontend_collectivites_territoriales
pnpm dev
```

### 2. Tester l'inscription

1. Ouvrez http://localhost:3000/auth/register (ou 3001)
2. Remplissez le formulaire :
   - Nom : Test
   - Prénom : Utilisateur
   - Email : test@example.mg
   - Username : testuser
   - Téléphone : +261 34 12 345 67
   - Mot de passe : Test1234
   - Confirmer le mot de passe : Test1234
3. Cochez "J'accepte les conditions"
4. Cliquez sur "Créer mon compte"

**Résultat attendu** :
```
✅ Compte créé avec succès !
➜ Redirection vers la connexion...
```

### 3. Se connecter

1. Sur la page de login (http://localhost:3000/auth/login)
2. Username : `testuser`
3. Mot de passe : `Test1234`
4. Cliquez sur "Se connecter"

**Résultat attendu** :
```
✅ Connexion réussie
➜ Redirection vers /admin
```

---

## 📊 Endpoints Disponibles

### Publics (sans authentification)
- `GET /api/v1/roles/` - Liste des rôles actifs
- `GET /api/v1/roles/code/{code}` - Rôle par code

### Protégés (avec authentification)
- `POST /api/v1/roles/` - Créer un rôle
- `PUT /api/v1/roles/{id}` - Modifier un rôle
- `DELETE /api/v1/roles/{id}` - Désactiver un rôle

---

## 🔒 Sécurité

### Protection des Rôles Système

Les rôles système (ADMIN, EDITEUR, LECTEUR) **ne peuvent pas être supprimés**.

Si vous essayez de supprimer un rôle système :
```json
{
  "detail": "Le rôle système 'ADMIN' ne peut pas être supprimé"
}
```

### Soft Delete

La suppression d'un rôle le **désactive** (soft delete) au lieu de le supprimer de la base de données.

```python
# Le rôle n'est pas supprimé, juste désactivé
role.actif = False
```

---

## 🐛 Dépannage

### Erreur "ModuleNotFoundError: No module named 'app.api.v1.endpoints.roles'"

**Solution** : Redémarrez le serveur après avoir créé le fichier roles.py

```bash
# Arrêter le serveur (Ctrl+C)
# Relancer
./run.sh
```

### Erreur "Table 'roles' doesn't exist"

**Solution** : Vérifiez que la base de données a été initialisée avec les scripts SQL :

```bash
cd backend_collectivites_territoriales
psql -U postgres -d revenus_miniers_db -f scripts/schema.sql
psql -U postgres -d revenus_miniers_db -f scripts/seed_data.sql
```

### L'endpoint /api/v1/roles/ retourne une liste vide

**Solution** : Vérifiez que les données de seed ont été insérées :

```bash
psql -U postgres -d revenus_miniers_db -c "SELECT * FROM roles;"
```

Si vide, réexécutez :
```bash
psql -U postgres -d revenus_miniers_db -f scripts/seed_data.sql
```

---

## ✅ Checklist Finale

Avant de tester l'inscription :

- [ ] Backend démarré sur http://localhost:8000
- [ ] Frontend démarré sur http://localhost:3000 (ou 3001)
- [ ] `curl http://localhost:8000/api/v1/roles/` retourne 3 rôles
- [ ] CORS configuré avec le bon port (3000 ou 3001) dans `.env`
- [ ] Base de données initialisée avec schema.sql et seed_data.sql

---

## 🎉 Félicitations !

Vous avez maintenant :
- ✅ Un endpoint complet pour gérer les rôles
- ✅ Une inscription frontend fonctionnelle
- ✅ Une attribution automatique du rôle LECTEUR
- ✅ Une protection des rôles système
- ✅ Une documentation Swagger complète

**Prochaine étape** : Testez l'inscription et la connexion ! 🚀
