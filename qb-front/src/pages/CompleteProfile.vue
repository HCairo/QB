<template>
    <div class="max-w-md mx-auto mt-10 p-6 bg-white shadow rounded">
      <h2 class="text-2xl font-bold mb-4">Complétez votre profil entreprise</h2>
      <form @submit.prevent="submitProfile">
        <div class="mb-4">
          <label class="block mb-1">Nom de l'entreprise *</label>
          <input v-model="company.company_name" type="text" required class="w-full border px-3 py-2 rounded" />
        </div>
        <div class="mb-4">
          <label class="block mb-1">Numéro SIRET</label>
          <input v-model="company.siret" type="text" class="w-full border px-3 py-2 rounded" />
        </div>
        <div class="mb-4">
          <label class="block mb-1">Secteur d'activité</label>
          <select v-model="company.sector" class="w-full border px-3 py-2 rounded">
            <option value="">Sélectionnez un secteur</option>
            <option value="Informatique">Informatique</option>
            <option value="Commerce">Commerce</option>
            <option value="Construction">Construction</option>
            <option value="Consulting">Consulting</option>
            <option value="Autre">Autre</option>
          </select>
        </div>
        <div class="flex justify-between items-center">
          <button type="submit" class="bg-indigo-600 text-white px-4 py-2 rounded hover:bg-indigo-500">
            Enregistrer
          </button>
          <button @click.prevent="skip" class="text-gray-500 hover:underline">
            Passer pour le moment
          </button>
        </div>
      </form>
    </div>
  </template>
  
  <script setup>
  import { reactive } from 'vue'
  import axios from 'axios'
  import { useRouter } from 'vue-router'
  import { useToast } from 'vue-toastification'
  
  const router = useRouter()
  
  const company = reactive({
    company_name: '',
    siret: '',
    sector: ''
  })

const toast = useToast()

const submitProfile = async () => {
  try {
    const token = localStorage.getItem('token')
    await axios.post('http://localhost:8000/profile/company', company, {
      headers: { Authorization: `Bearer ${token}` }
    })
    toast.success('Profil entreprise enregistré !')
    router.push('/dashboard')
  } catch (err) {
    console.error('Erreur lors de la sauvegarde du profil', err)
    toast.error("Erreur lors de l'enregistrement")
  }
}
  
  const skip = () => {
    router.push('/dashboard')
  }
  </script>  