# Guide d'intégration avec Nuxt 3

Ce document explique comment intégrer le backend FastAPI avec un frontend Nuxt 3.

## Configuration de base

### 1. Installation des dépendances

```bash
npm install --save-dev @nuxtjs/tailwindcss
npm install axios
```

### 2. Configuration Nuxt (`nuxt.config.ts`)

```typescript
export default defineNuxtConfig({
  modules: ['@nuxtjs/tailwindcss'],

  runtimeConfig: {
    public: {
      apiBase: process.env.NUXT_PUBLIC_API_BASE || 'http://localhost:8000',
      apiVersion: 'v1'
    }
  },

  app: {
    head: {
      title: 'Plateforme de Suivi des Revenus Miniers',
      meta: [
        { charset: 'utf-8' },
        { name: 'viewport', content: 'width=device-width, initial-scale=1' },
      ],
    }
  }
})
```

### 3. Variables d'environnement (`.env`)

```bash
NUXT_PUBLIC_API_BASE=http://localhost:8000
```

## Composables

### useApi.ts

Composable pour gérer les appels API avec gestion automatique des tokens.

```typescript
// composables/useApi.ts
import type { UseFetchOptions } from 'nuxt/app'

export const useApi = <T>(
  url: string,
  options: UseFetchOptions<T> = {}
) => {
  const config = useRuntimeConfig()
  const { token } = useAuth()

  // Construire l'URL complète
  const fullUrl = `${config.public.apiBase}/api/${config.public.apiVersion}${url}`

  // Ajouter les headers d'authentification si le token existe
  const headers: Record<string, string> = {
    'Accept': 'application/json',
    'Content-Type': 'application/json',
    ...options.headers as Record<string, string>
  }

  if (token.value) {
    headers['Authorization'] = `Bearer ${token.value}`
  }

  return useFetch<T>(fullUrl, {
    ...options,
    headers
  })
}
```

### useAuth.ts

Composable pour gérer l'authentification.

```typescript
// composables/useAuth.ts
export const useAuth = () => {
  const token = useState<string | null>('auth:token', () => null)
  const user = useState<any | null>('auth:user', () => null)
  const loading = ref(false)
  const error = ref<string | null>(null)

  // Initialiser depuis localStorage au montage du composant
  onMounted(() => {
    if (process.client) {
      const savedToken = localStorage.getItem('auth:token')
      const savedUser = localStorage.getItem('auth:user')

      if (savedToken) {
        token.value = savedToken
      }

      if (savedUser) {
        try {
          user.value = JSON.parse(savedUser)
        } catch (e) {
          console.error('Failed to parse saved user:', e)
        }
      }
    }
  })

  // Connexion
  const login = async (credentials: { username: string; password: string }) => {
    loading.value = true
    error.value = null

    try {
      const config = useRuntimeConfig()
      const formData = new URLSearchParams()
      formData.append('username', credentials.username)
      formData.append('password', credentials.password)

      const response = await $fetch<{ access_token: string; token_type: string }>(
        `${config.public.apiBase}/api/v1/auth/login`,
        {
          method: 'POST',
          headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
          },
          body: formData
        }
      )

      token.value = response.access_token

      // Stocker dans localStorage
      if (process.client) {
        localStorage.setItem('auth:token', response.access_token)
      }

      // Récupérer les infos de l'utilisateur
      await fetchUser()

      return true
    } catch (e: any) {
      error.value = e.data?.detail || 'Erreur de connexion'
      return false
    } finally {
      loading.value = false
    }
  }

  // Récupérer les informations de l'utilisateur
  const fetchUser = async () => {
    if (!token.value) return

    try {
      const config = useRuntimeConfig()
      const userData = await $fetch(
        `${config.public.apiBase}/api/v1/auth/me`,
        {
          headers: {
            'Authorization': `Bearer ${token.value}`
          }
        }
      )

      user.value = userData

      if (process.client) {
        localStorage.setItem('auth:user', JSON.stringify(userData))
      }
    } catch (e) {
      console.error('Failed to fetch user:', e)
      logout()
    }
  }

  // Déconnexion
  const logout = () => {
    token.value = null
    user.value = null

    if (process.client) {
      localStorage.removeItem('auth:token')
      localStorage.removeItem('auth:user')
    }

    // Rediriger vers la page de connexion
    navigateTo('/login')
  }

  // Vérifier si l'utilisateur est connecté
  const isAuthenticated = computed(() => !!token.value)

  // Vérifier si l'utilisateur a une permission spécifique
  const hasPermission = (permission: string) => {
    if (!user.value?.role) return false
    return user.value.role.permissions?.[permission] === true || user.value.role.permissions?.all === true
  }

  return {
    token,
    user,
    loading,
    error,
    login,
    logout,
    fetchUser,
    isAuthenticated,
    hasPermission
  }
}
```

## Middleware d'authentification

```typescript
// middleware/auth.ts
export default defineNuxtRouteMiddleware((to, from) => {
  const { isAuthenticated } = useAuth()

  if (!isAuthenticated.value) {
    return navigateTo('/login')
  }
})
```

## Exemples de pages

### Page de connexion

```vue
<!-- pages/login.vue -->
<template>
  <div class="min-h-screen flex items-center justify-center bg-gray-100">
    <div class="max-w-md w-full bg-white rounded-lg shadow-md p-8">
      <h1 class="text-2xl font-bold mb-6 text-center">
        Connexion
      </h1>

      <form @submit.prevent="handleLogin">
        <div class="mb-4">
          <label class="block text-gray-700 text-sm font-bold mb-2">
            Nom d'utilisateur
          </label>
          <input
            v-model="credentials.username"
            type="text"
            class="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            required
          />
        </div>

        <div class="mb-6">
          <label class="block text-gray-700 text-sm font-bold mb-2">
            Mot de passe
          </label>
          <input
            v-model="credentials.password"
            type="password"
            class="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            required
          />
        </div>

        <div v-if="error" class="mb-4 text-red-500 text-sm">
          {{ error }}
        </div>

        <button
          type="submit"
          :disabled="loading"
          class="w-full bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded-lg disabled:opacity-50"
        >
          {{ loading ? 'Connexion...' : 'Se connecter' }}
        </button>
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
definePageMeta({
  layout: false
})

const { login, loading, error } = useAuth()
const router = useRouter()

const credentials = ref({
  username: '',
  password: ''
})

const handleLogin = async () => {
  const success = await login(credentials.value)
  if (success) {
    router.push('/')
  }
}
</script>
```

### Dashboard avec tableau de revenus

```vue
<!-- pages/index.vue -->
<template>
  <div class="container mx-auto px-4 py-8">
    <div class="flex justify-between items-center mb-6">
      <h1 class="text-3xl font-bold">Tableau de Compte Administratif</h1>

      <button
        @click="logout"
        class="bg-red-500 hover:bg-red-700 text-white font-bold py-2 px-4 rounded"
      >
        Déconnexion
      </button>
    </div>

    <!-- Filtres -->
    <div class="bg-white rounded-lg shadow-md p-6 mb-6">
      <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div>
          <label class="block text-sm font-medium mb-2">Commune</label>
          <select
            v-model="filters.commune_code"
            class="w-full px-3 py-2 border rounded-lg"
            @change="loadTableau"
          >
            <option value="">Sélectionner...</option>
            <option v-for="commune in communes" :key="commune.code" :value="commune.code">
              {{ commune.nom }}
            </option>
          </select>
        </div>

        <div>
          <label class="block text-sm font-medium mb-2">Exercice</label>
          <select
            v-model="filters.exercice_annee"
            class="w-full px-3 py-2 border rounded-lg"
            @change="loadTableau"
          >
            <option value="">Sélectionner...</option>
            <option v-for="annee in [2024, 2023, 2022]" :key="annee" :value="annee">
              {{ annee }}
            </option>
          </select>
        </div>

        <div class="flex items-end">
          <button
            @click="exportExcel"
            :disabled="!canExport"
            class="w-full bg-green-500 hover:bg-green-700 text-white font-bold py-2 px-4 rounded disabled:opacity-50"
          >
            Export Excel
          </button>
        </div>
      </div>
    </div>

    <!-- Tableau -->
    <div v-if="loading" class="text-center py-12">
      Chargement...
    </div>

    <div v-else-if="tableau" class="bg-white rounded-lg shadow-md overflow-x-auto">
      <table class="min-w-full divide-y divide-gray-200">
        <thead class="bg-blue-900 text-white">
          <tr>
            <th class="px-6 py-3 text-left text-xs font-medium uppercase tracking-wider">
              Code
            </th>
            <th class="px-6 py-3 text-left text-xs font-medium uppercase tracking-wider">
              Rubrique
            </th>
            <th
              v-for="periode in tableau.periodes"
              :key="periode.id"
              class="px-6 py-3 text-right text-xs font-medium uppercase tracking-wider"
            >
              {{ periode.nom }}
            </th>
            <th class="px-6 py-3 text-right text-xs font-medium uppercase tracking-wider">
              TOTAL
            </th>
          </tr>
        </thead>
        <tbody class="bg-white divide-y divide-gray-200">
          <tr v-for="rubrique in tableau.rubriques" :key="rubrique.id">
            <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
              {{ rubrique.code }}
            </td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
              <span :style="{ paddingLeft: `${(rubrique.niveau - 1) * 20}px` }">
                {{ rubrique.nom }}
              </span>
            </td>
            <td
              v-for="periode in tableau.periodes"
              :key="periode.id"
              class="px-6 py-4 whitespace-nowrap text-sm text-gray-900 text-right"
            >
              {{ formatMontant(getMontant(rubrique.id, periode.id)) }}
            </td>
            <td class="px-6 py-4 whitespace-nowrap text-sm font-bold text-gray-900 text-right">
              {{ formatMontant(tableau.totaux[rubrique.id]) }}
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup lang="ts">
definePageMeta({
  middleware: ['auth']
})

const { logout } = useAuth()

const filters = ref({
  commune_code: '',
  exercice_annee: 2024
})

// Charger les communes
const { data: communes } = await useApi('/geo/communes')

// Charger le tableau
const loading = ref(false)
const tableau = ref(null)

const loadTableau = async () => {
  if (!filters.value.commune_code || !filters.value.exercice_annee) return

  loading.value = true
  try {
    const { data } = await useApi(
      `/revenus/tableau/${filters.value.commune_code}/${filters.value.exercice_annee}`
    )
    tableau.value = data.value
  } catch (e) {
    console.error('Failed to load tableau:', e)
  } finally {
    loading.value = false
  }
}

const getMontant = (rubriqueId: string, periodeId: string) => {
  if (!tableau.value?.donnees?.[rubriqueId]?.[periodeId]) return 0
  return tableau.value.donnees[rubriqueId][periodeId].montant || 0
}

const formatMontant = (montant: number) => {
  if (!montant) return '-'
  return new Intl.NumberFormat('fr-FR', {
    style: 'currency',
    currency: 'MGA',
    minimumFractionDigits: 0,
    maximumFractionDigits: 0
  }).format(montant)
}

const canExport = computed(() => {
  return !!(filters.value.commune_code && filters.value.exercice_annee)
})

const exportExcel = async () => {
  const config = useRuntimeConfig()
  const { token } = useAuth()

  const url = `${config.public.apiBase}/api/v1/export/excel/${filters.value.commune_code}/${filters.value.exercice_annee}`

  window.open(url + `?token=${token.value}`, '_blank')
}
</script>
```

## Types TypeScript

```typescript
// types/index.ts
export interface Region {
  id: string
  code: string
  nom: string
  actif: boolean
}

export interface Commune {
  id: string
  code: string
  nom: string
  departement_id: string
  actif: boolean
}

export interface Exercice {
  id: string
  annee: number
  actif: boolean
}

export interface Periode {
  id: string
  nom: string
  code: string
  exercice_id: string
  ordre: number
  actif: boolean
}

export interface Rubrique {
  id: string
  code: string
  nom: string
  categorie_id: string
  parent_id: string | null
  niveau: number
  actif: boolean
}

export interface Revenu {
  id: string
  commune_id: string
  exercice_id: string
  periode_id: string
  rubrique_id: string
  montant: number
}

export interface Tableau {
  commune: Commune
  exercice: Exercice
  periodes: Periode[]
  rubriques: Rubrique[]
  donnees: Record<string, Record<string, Revenu>>
  totaux: Record<string, number>
}
```

## Démarrage

1. **Backend** :
   ```bash
   cd backend_collectivites_territoriales
   ./run.sh  # ou run.bat sur Windows
   ```

2. **Frontend Nuxt** :
   ```bash
   cd frontend  # Votre projet Nuxt
   npm install
   npm run dev
   ```

3. Accédez à http://localhost:3000

## Notes importantes

- **CORS** : Le backend est déjà configuré pour accepter les requêtes depuis `http://localhost:3000`
- **Tokens** : Les tokens JWT sont stockés dans localStorage et ajoutés automatiquement aux requêtes
- **Sécurité** : En production, utilisez HTTPS et configurez correctement les origines CORS
- **Export** : Les exports (Excel/Word/PDF) s'ouvrent dans un nouvel onglet avec le token dans l'URL

## Documentation API complète

La documentation interactive Swagger est disponible à : http://localhost:8000/docs
