<template>
  <div class="min-h-screen flex flex-col">
    <!-- Header -->
    <header class="bg-white shadow-sm sticky top-0 z-10">
      <div class="max-w-7xl mx-auto px-4 py-4 flex justify-between items-center">
        <RouterLink to="/" class="text-xl font-bold text-indigo-600 hover:underline">
  QuillBill
</RouterLink>

        <nav class="space-x-4">
          <RouterLink to="/login" class="text-gray-700 hover:text-indigo-600">Connexion</RouterLink>
          <RouterLink to="/register" class="text-gray-700 hover:text-indigo-600">Créer un compte</RouterLink>
        </nav>
      </div>
    </header>

    <!-- Form container -->
    <main class="flex-1 flex items-center justify-center px-4 bg-gray-50">
      <div class="max-w-md w-full bg-white shadow-md rounded p-8">
        <h2 class="text-2xl font-bold mb-4">Connexion</h2>
        <form @submit.prevent="login" class="space-y-4">
          <input
            v-model="email"
            type="email"
            placeholder="Email"
            class="w-full p-2 border rounded"
          />
          <input
            v-model="password"
            type="password"
            placeholder="Mot de passe"
            class="w-full p-2 border rounded"
          />
          <button
            type="submit"
            class="w-full bg-indigo-600 text-white p-2 rounded hover:bg-indigo-500"
          >
            Se connecter
          </button>
          <button @click="loginWithGoogle" class="w-full bg-red-500 text-white px-4 py-2 rounded mt-4">
          🖥️ Se connecter avec Google
          </button>
          <p v-if="error" class="text-red-600">{{ error }}</p>
        </form>
      </div>
    </main>

    <!-- Footer -->
    <footer class="bg-gray-100 text-sm text-gray-500 text-center py-4">
      © {{ new Date().getFullYear() }} QuillBill. Tous droits réservés.
    </footer>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import api from '../utils/api'
import { useToast } from 'vue-toastification'

const email = ref('')
const password = ref('')
const error = ref('')
const router = useRouter()
const toast = useToast()

const login = async () => {
  try {
    const res = await api.post('/login', {
      email: email.value,
      password: password.value,
    })

    localStorage.setItem('token', res.data.access_token)

    const profileCheck = await api.get('/profile/company', {
      headers: { Authorization: `Bearer ${res.data.access_token}` }
    })

    toast.success('Connexion réussie !')

    if (profileCheck.data.exists) {
      router.push('/dashboard')
    } else {
      router.push('/complete-profile')
    }

  } catch (err) {
    console.error(err)
    toast.error = "Identifiants invalides"
  }
}

const loginWithGoogle = () => {
  window.location.href = 'http://localhost:8000/auth/google'
}
</script>