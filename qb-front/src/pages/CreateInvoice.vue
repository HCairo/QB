<template>
    <div>
      <h1 class="text-2xl font-bold text-gray-800 mb-4">Créer une facture</h1>
  
      <form @submit.prevent="submitInvoice" class="space-y-4 max-w-md">
        <input
          v-model="client_name"
          type="text"
          placeholder="Nom du client"
          class="w-full p-2 border rounded"
        />
        <input
          v-model.number="amount"
          type="number"
          placeholder="Montant"
          class="w-full p-2 border rounded"
        />
        <select v-model="status" class="w-full p-2 border rounded">
          <option value="draft">Brouillon</option>
          <option value="sent">Envoyée</option>
          <option value="paid">Payée</option>
        </select>
        <button
          type="submit"
          class="w-full bg-indigo-600 text-white p-2 rounded hover:bg-indigo-500"
        >
          Enregistrer la facture
        </button>
        <p v-if="message" class="text-green-600">{{ message }}</p>
        <p v-if="error" class="text-red-600">{{ error }}</p>
      </form>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted } from 'vue'
  import api from '../utils/api'
  
  const client_name = ref('')
  const amount = ref('')
  const status = ref('draft')
  const message = ref('')
  const error = ref('')
  const userId = ref(null)
  
  onMounted(async () => {
    try {
      const response = await api.get('/me')
      userId.value = response.data.id
    } catch (err) {
      error.value = "Impossible de récupérer l'utilisateur"
    }
  })
  
  const submitInvoice = async () => {
    try {
      const response = await api.post(`/invoices`, {
        client_name: client_name.value,
        amount: amount.value,
        status: status.value,
      })
      message.value = 'Facture créée avec succès !'
      client_name.value = ''
      amount.value = ''
      status.value = 'draft'
      error.value = ''
    } catch (err) {
      error.value = "Erreur lors de la création de la facture"
      message.value = ''
    }
  }
  </script>  