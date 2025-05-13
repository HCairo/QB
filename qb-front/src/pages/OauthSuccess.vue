<template>
  <div class="flex items-center justify-center h-screen">
    <p class="text-lg font-semibold">Connexion en cours... Veuillez patienter</p>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useRouter } from 'vue-router'
import api from '../utils/api'
import { useToast } from 'vue-toastification'

const router = useRouter()
const toast = useToast()

onMounted(async () => {
  try {
    const params = new URLSearchParams(window.location.search)
    const token = params.get('token')

    if (!token) {
      toast.error("Échec de la connexion Google")
      router.push('/login')
      return
    }

    localStorage.setItem('token', token)

    const profileCheck = await api.get('/profile/company', {
      headers: { Authorization: `Bearer ${token}` }
    })

    toast.success('Connexion via Google réussie !')

    if (profileCheck.data.exists) {
      router.push('/dashboard')
    } else {
      router.push('/complete-profile')
    }

  } catch (err) {
    console.error("Erreur OAuth :", err)
    toast.error("Erreur lors de la connexion Google")
    router.push('/login')
  }
})
</script>