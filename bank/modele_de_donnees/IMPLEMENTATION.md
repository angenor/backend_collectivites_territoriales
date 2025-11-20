# Guide d'Implémentation - Modèle de Données Supabase

## Prérequis

1. **Compte Supabase**
   - Créer un compte sur [supabase.com](https://supabase.com)
   - Créer un nouveau projet
   - Noter l'URL du projet et les clés API (anon key, service role key)

2. **Environnement de développement**
   - Node.js 18+ et pnpm installés
   - Nuxt 4 configuré (déjà fait selon CLAUDE.md)
   - Supabase CLI (optionnel mais recommandé)

3. **Variables d'environnement**
   - Créer un fichier `.env` à la racine du projet
   ```bash
   SUPABASE_URL=https://your-project.supabase.co
   SUPABASE_KEY=your-anon-key
   SUPABASE_SERVICE_KEY=your-service-role-key
   ```

---

## Étape 1 : Créer le Projet Supabase

### 1.1 Via le Dashboard Supabase

1. Se connecter à [app.supabase.com](https://app.supabase.com)
2. Cliquer sur "New Project"
3. Renseigner :
   - **Name** : `collectivites-territoriales` (ou nom de votre choix)
   - **Database Password** : Mot de passe sécurisé (le noter!)
   - **Region** : Choisir la région la plus proche (ex: Europe - Frankfurt)
   - **Plan** : Free tier pour commencer
4. Cliquer sur "Create new project"
5. Attendre 1-2 minutes que le projet soit prêt

### 1.2 Noter les informations de connexion

Dans l'onglet **Settings → API**, noter :
- Project URL (SUPABASE_URL)
- anon/public key (SUPABASE_KEY)
- service_role key (SUPABASE_SERVICE_KEY) - **À garder secret!**

---

## Étape 2 : Exécuter le Schéma SQL

### 2.1 Via le SQL Editor du Dashboard

1. Dans le Dashboard Supabase, aller dans **SQL Editor**
2. Cliquer sur **New Query**
3. Copier-coller le contenu de `schema.sql`
4. Cliquer sur **Run** (Ctrl+Enter)
5. Vérifier qu'il n'y a pas d'erreurs dans le panneau inférieur

### 2.2 Via Supabase CLI (Recommandé pour la production)

```bash
# Installer Supabase CLI
npm install -g supabase

# Se connecter au projet
supabase login

# Lier le projet local au projet Supabase
supabase link --project-ref your-project-ref

# Exécuter le schéma
supabase db push

# Ou exécuter directement le fichier
psql -h db.your-project.supabase.co -U postgres -d postgres -f bank/modele_de_donnees/schema.sql
```

### 2.3 Vérification

1. Aller dans **Table Editor**
2. Vérifier que toutes les tables sont créées :
   - regions, districts, communes
   - projets_miniers, revenus_miniers
   - comptes_administratifs, rubriques_budgetaires, etc.

---

## Étape 3 : Appliquer les Politiques RLS

### 3.1 Exécuter policies.sql

1. Dans **SQL Editor**, créer une nouvelle requête
2. Copier-coller le contenu de `policies.sql`
3. Cliquer sur **Run**
4. Vérifier qu'il n'y a pas d'erreurs

### 3.2 Vérifier l'activation de RLS

1. Aller dans **Authentication → Policies**
2. Vérifier que chaque table a des politiques RLS activées
3. Vérifier que les politiques apparaissent pour chaque table

### 3.3 Tester les politiques

```sql
-- Tester l'accès public aux régions
SELECT * FROM regions; -- Devrait fonctionner

-- Tester l'accès aux comptes administratifs (devrait retourner uniquement les publiés)
SELECT * FROM comptes_administratifs;
```

---

## Étape 4 : Charger les Données d'Exemple

### 4.1 Via SQL Editor

1. Créer une nouvelle requête dans **SQL Editor**
2. Copier-coller le contenu de `seed-data.sql`
3. Cliquer sur **Run**
4. Vérifier que les données sont insérées

### 4.2 Vérification

```sql
-- Vérifier les régions
SELECT * FROM regions;

-- Vérifier la hiérarchie
SELECT * FROM v_hierarchie_collectivites;

-- Vérifier les comptes administratifs
SELECT * FROM comptes_administratifs;

-- Vérifier les lignes budgétaires
SELECT * FROM lignes_budgetaires LIMIT 10;
```

---

## Étape 5 : Configurer Supabase Storage

### 5.1 Créer les Buckets

1. Aller dans **Storage** dans le Dashboard
2. Cliquer sur **New bucket**
3. Créer les buckets suivants :

#### Bucket: documents
- **Name** : `documents`
- **Public** : Cocher si les documents doivent être publics
- **File size limit** : 10 MB (ou plus selon besoin)
- **Allowed MIME types** :
  - `application/vnd.openxmlformats-officedocument.spreadsheetml.sheet` (Excel)
  - `application/vnd.openxmlformats-officedocument.wordprocessingml.document` (Word)
  - `application/pdf` (PDF)

#### Bucket: avatars
- **Name** : `avatars`
- **Public** : Cocher
- **File size limit** : 2 MB
- **Allowed MIME types** : `image/*`

#### Bucket: messages-attachments
- **Name** : `messages-attachments`
- **Public** : Décocher (privé)
- **File size limit** : 5 MB

### 5.2 Configurer les Politiques Storage

Dans **Storage → Policies**, créer les politiques suivantes :

```sql
-- Politique: Lecture publique des documents publics
CREATE POLICY "Documents publics: lecture publique"
ON storage.objects FOR SELECT
USING (
    bucket_id = 'documents' AND
    EXISTS (
        SELECT 1 FROM documents d
        WHERE d.fichier_url = storage.objects.name
        AND d.est_public = TRUE
    )
);

-- Politique: Upload de documents par éditeurs
CREATE POLICY "Documents: upload par éditeurs"
ON storage.objects FOR INSERT
WITH CHECK (
    bucket_id = 'documents' AND
    (auth.jwt() ->> 'role') IN ('administrateur', 'editeur')
);

-- Politique: Lecture des avatars publics
CREATE POLICY "Avatars: lecture publique"
ON storage.objects FOR SELECT
USING (bucket_id = 'avatars');

-- Politique: Upload de son propre avatar
CREATE POLICY "Avatars: upload propre avatar"
ON storage.objects FOR INSERT
WITH CHECK (
    bucket_id = 'avatars' AND
    (storage.foldername(name))[1] = auth.uid()::text
);
```

---

## Étape 6 : Configuration dans Nuxt

### 6.1 Installer les dépendances Supabase

```bash
pnpm add @supabase/supabase-js
```

### 6.2 Créer le plugin Supabase

Créer `app/plugins/supabase.ts` :

```typescript
import { createClient } from '@supabase/supabase-js'

export default defineNuxtPlugin(() => {
  const config = useRuntimeConfig()

  const supabase = createClient(
    config.public.supabaseUrl,
    config.public.supabaseKey
  )

  return {
    provide: {
      supabase
    }
  }
})
```

### 6.3 Configurer nuxt.config.ts

Ajouter dans `nuxt.config.ts` :

```typescript
export default defineNuxtConfig({
  runtimeConfig: {
    // Clés privées (côté serveur uniquement)
    supabaseServiceKey: process.env.SUPABASE_SERVICE_KEY,

    // Clés publiques (exposées au client)
    public: {
      supabaseUrl: process.env.SUPABASE_URL,
      supabaseKey: process.env.SUPABASE_KEY,
    }
  },

  // ... reste de la config
})
```

### 6.4 Créer les composables Supabase

Créer `app/composables/useSupabase.ts` :

```typescript
export const useSupabase = () => {
  const { $supabase } = useNuxtApp()
  return $supabase
}

export const useSupabaseUser = () => {
  const supabase = useSupabase()
  const user = useState('supabase_user', () => null)

  // Charger l'utilisateur au montage
  onMounted(async () => {
    const { data: { user: currentUser } } = await supabase.auth.getUser()
    user.value = currentUser
  })

  return user
}
```

### 6.5 Créer les composables métier

Créer `app/composables/useCollectivites.ts` :

```typescript
export const useCollectivites = () => {
  const supabase = useSupabase()

  const getRegions = async () => {
    const { data, error } = await supabase
      .from('regions')
      .select('*')
      .order('nom')

    if (error) throw error
    return data
  }

  const getDistricts = async (regionId: string) => {
    const { data, error } = await supabase
      .from('districts')
      .select('*')
      .eq('region_id', regionId)
      .order('nom')

    if (error) throw error
    return data
  }

  const getCommunes = async (districtId: string) => {
    const { data, error } = await supabase
      .from('communes')
      .select('*')
      .eq('district_id', districtId)
      .order('nom')

    if (error) throw error
    return data
  }

  return {
    getRegions,
    getDistricts,
    getCommunes
  }
}
```

Créer `app/composables/useComptesAdministratifs.ts` :

```typescript
export const useComptesAdministratifs = () => {
  const supabase = useSupabase()

  const getCompteByCommune = async (communeId: string, annee: number) => {
    const { data, error } = await supabase
      .from('comptes_administratifs')
      .select(`
        *,
        commune:communes(*),
        lignes_budgetaires(
          *,
          rubrique:rubriques_budgetaires(*)
        )
      `)
      .eq('commune_id', communeId)
      .eq('annee', annee)
      .eq('statut', 'publie')
      .single()

    if (error) throw error
    return data
  }

  const getLignesBudgetaires = async (compteId: string) => {
    const { data, error } = await supabase
      .from('lignes_budgetaires')
      .select(`
        *,
        rubrique:rubriques_budgetaires(*)
      `)
      .eq('compte_administratif_id', compteId)
      .order('rubrique.ordre')

    if (error) throw error
    return data
  }

  return {
    getCompteByCommune,
    getLignesBudgetaires
  }
}
```

---

## Étape 7 : Configurer l'Authentification

### 7.1 Activer les fournisseurs d'authentification

Dans **Authentication → Providers** :

1. **Email** : Activer l'authentification par email/mot de passe
2. **Magic Link** (optionnel) : Pour connexion sans mot de passe
3. **OAuth** (optionnel) : Google, GitHub, etc.

### 7.2 Configurer les URLs de redirection

Dans **Authentication → URL Configuration** :

- **Site URL** : `http://localhost:3000` (dev) ou votre domaine de production
- **Redirect URLs** : Ajouter les URLs autorisées pour les redirections

### 7.3 Personnaliser les emails

Dans **Authentication → Email Templates** :

Personnaliser les templates pour :
- Confirmation d'inscription
- Réinitialisation de mot de passe
- Magic link

### 7.4 Créer les composables d'authentification

Créer `app/composables/useAuth.ts` :

```typescript
export const useAuth = () => {
  const supabase = useSupabase()
  const user = useSupabaseUser()
  const router = useRouter()

  const signUp = async (email: string, password: string, metadata = {}) => {
    const { data, error } = await supabase.auth.signUp({
      email,
      password,
      options: {
        data: metadata
      }
    })

    if (error) throw error
    return data
  }

  const signIn = async (email: string, password: string) => {
    const { data, error } = await supabase.auth.signInWithPassword({
      email,
      password
    })

    if (error) throw error
    user.value = data.user
    return data
  }

  const signOut = async () => {
    const { error } = await supabase.auth.signOut()
    if (error) throw error
    user.value = null
    router.push('/')
  }

  const isAdmin = computed(() => {
    // Implémenter la logique de vérification du rôle
    return user.value?.user_metadata?.role === 'administrateur'
  })

  const canEdit = computed(() => {
    const role = user.value?.user_metadata?.role
    return role === 'administrateur' || role === 'editeur'
  })

  return {
    user,
    signUp,
    signIn,
    signOut,
    isAdmin,
    canEdit
  }
}
```

---

## Étape 8 : Tester l'Implémentation

### 8.1 Tests de base

1. **Test de connexion à la base de données**
   ```typescript
   // Dans une page de test
   const supabase = useSupabase()
   const { data, error } = await supabase.from('regions').select('*')
   console.log('Régions:', data)
   ```

2. **Test d'authentification**
   - Créer un compte utilisateur
   - Se connecter
   - Vérifier que le profil est créé automatiquement

3. **Test des politiques RLS**
   - Vérifier l'accès public aux données publiées
   - Vérifier les restrictions pour les données en brouillon
   - Tester les différents rôles (admin, éditeur, lecteur)

### 8.2 Tests fonctionnels

1. **Sélection de collectivité**
   - Charger les régions
   - Sélectionner une région → charger les districts
   - Sélectionner un district → charger les communes
   - Afficher le compte administratif d'une commune

2. **Affichage des tableaux**
   - Récupérer les lignes budgétaires
   - Récupérer la configuration des colonnes
   - Générer le tableau dynamique

3. **Téléchargement de documents**
   - Uploader un fichier Excel dans Storage
   - Créer un enregistrement dans la table `documents`
   - Télécharger le fichier
   - Vérifier l'incrémentation du compteur

---

## Étape 9 : Optimisations de Performance

### 9.1 Activer la mise en cache

```typescript
// Dans les composables
const getRegions = async () => {
  const { data, error } = await supabase
    .from('regions')
    .select('*')
    .order('nom')

  if (error) throw error

  // Mettre en cache côté client
  return useState('regions', () => data).value
}
```

### 9.2 Utiliser Supabase Realtime (optionnel)

Pour les mises à jour en temps réel :

```typescript
// S'abonner aux changements
const channel = supabase
  .channel('comptes_administratifs')
  .on(
    'postgres_changes',
    {
      event: '*',
      schema: 'public',
      table: 'comptes_administratifs'
    },
    (payload) => {
      console.log('Changement détecté:', payload)
      // Actualiser les données
    }
  )
  .subscribe()
```

### 9.3 Optimiser les requêtes

- Utiliser `select()` avec uniquement les champs nécessaires
- Utiliser les index créés dans le schéma
- Limiter les résultats avec `.limit()` et `.range()`
- Utiliser la pagination pour les grandes listes

---

## Étape 10 : Déploiement en Production

### 10.1 Vérifications avant déploiement

- [ ] Toutes les tables sont créées
- [ ] Les politiques RLS sont activées
- [ ] Les buckets Storage sont configurés
- [ ] Les données d'exemple sont chargées (ou supprimées)
- [ ] Les variables d'environnement de production sont définies
- [ ] L'authentification est configurée
- [ ] Les emails sont personnalisés

### 10.2 Sécurité

1. **Ne jamais exposer la service_role key** au client
2. Utiliser HTTPS en production
3. Configurer CORS correctement
4. Activer 2FA pour les comptes administrateurs
5. Auditer régulièrement les logs d'activité

### 10.3 Monitoring

1. Activer **Database Logs** dans Supabase
2. Configurer des alertes pour :
   - Utilisation de la base de données
   - Erreurs d'authentification
   - Quotas de Storage
3. Utiliser **Table Editor → Usage** pour surveiller les performances

### 10.4 Backup

1. Activer **Database Backups** dans Supabase (plan payant)
2. Ou configurer des backups manuels avec `pg_dump`
3. Tester régulièrement la restauration

---

## Ressources Complémentaires

### Documentation
- [Supabase Documentation](https://supabase.com/docs)
- [Supabase JavaScript Client](https://supabase.com/docs/reference/javascript)
- [Row Level Security Guide](https://supabase.com/docs/guides/auth/row-level-security)

### Outils utiles
- [Supabase CLI](https://supabase.com/docs/guides/cli)
- [DB Migrations](https://supabase.com/docs/guides/cli/local-development)
- [PostgREST API](https://postgrest.org/)

### Support
- [Supabase Community Discord](https://discord.supabase.com)
- [GitHub Discussions](https://github.com/supabase/supabase/discussions)
- [Stack Overflow](https://stackoverflow.com/questions/tagged/supabase)

---

## Dépannage

### Erreur: "permission denied for table"
→ Vérifier que RLS est activé et que les politiques sont correctes

### Erreur: "relation does not exist"
→ Vérifier que le schéma SQL a été exécuté correctement

### Erreur: "JWT expired"
→ Rafraîchir le token d'authentification

### Upload de fichier échoue
→ Vérifier les politiques Storage et les types MIME autorisés

### Performance lente
→ Vérifier les index, optimiser les requêtes, activer la mise en cache

---

## Prochaines Étapes

Après l'implémentation du modèle de données :

1. Développer les composants Vue pour l'interface utilisateur
2. Implémenter les tableaux dynamiques
3. Créer le back-office d'administration
4. Intégrer le système de newsletter
5. Implémenter le tracking analytics
6. Développer les exports Excel/Word
7. Tester et optimiser les performances
8. Déployer en production
