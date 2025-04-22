<template>
  <div>
    <h1 class="text-3xl font-bold text-gray-800 mb-4">Tableau de bord</h1>
    <p v-if="user" class="text-gray-600">
      Connecté en tant que <strong>{{ user.email }}</strong>
    </p>
    <p v-else class="text-red-600">Aucun utilisateur chargé.</p>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '../utils/api'

const user = ref(null)

onMounted(async () => {
  try {
    const response = await api.get('/me')
    user.value = response.data
  } catch (err) {
    console.error('Erreur lors du chargement du profil :', err)
  }
})
</script>