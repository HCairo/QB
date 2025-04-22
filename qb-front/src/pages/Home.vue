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

    <!-- Main Content -->
    <main class="flex-1 flex flex-col items-center justify-center text-center px-4">
      <h1 class="text-4xl sm:text-5xl font-bold text-indigo-600 mb-6">
        Bienvenue sur QuillBill 💼
      </h1>
      <p class="text-gray-600 text-lg mb-8 max-w-xl">
        Gère ta facturation comme un pro. Connecte-toi pour créer, envoyer et suivre tes factures rapidement.
      </p>
      <div class="flex flex-col sm:flex-row gap-4">
        <RouterLink
          to="/login"
          class="bg-indigo-600 text-white px-6 py-3 rounded hover:bg-indigo-500"
        >
          Se connecter
        </RouterLink>
        <RouterLink
          to="/register"
          class="border border-indigo-600 text-indigo-600 px-6 py-3 rounded hover:bg-indigo-50"
        >
          Créer un compte
        </RouterLink>
      </div>
    </main>

    <!-- Footer -->
    <footer class="bg-gray-100 text-sm text-gray-500 text-center py-4">
      © {{ new Date().getFullYear() }} QuillBill. Tous droits réservés.
    </footer>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const redirecting = ref(false)

onMounted(() => {
  const token = localStorage.getItem('token')
  if (token) {
    redirecting.value = true
    setTimeout(() => {
      router.push('/dashboard')
    }, 500) // Redirection après un court délai pour que l'utilisateur puisse voir la page d'accueil
  }
})
</script>