<template>
    <div>
      <h1 class="text-2xl font-bold text-gray-800 mb-4">Mes factures</h1>
  
      <div v-if="invoices.length === 0" class="text-gray-600">Aucune facture trouvée.</div>
  
      <ul v-else class="space-y-2">
        <li
          v-for="invoice in invoices"
          :key="invoice.id"
          class="p-4 bg-white shadow rounded"
        >
          <!-- EN MODE ÉDITION -->
          <div v-if="editId === invoice.id" class="space-y-2">
            <input
              v-model="editClientName"
              class="w-full p-2 border rounded"
              placeholder="Nom du client"
            />
            <input
              v-model.number="editAmount"
              type="number"
              class="w-full p-2 border rounded"
              placeholder="Montant"
            />
            
            <!-- Dropdown pour le statut -->
            <select
              v-model="editStatus"
              class="w-full p-2 border rounded"
            >
              <option value="draft">Brouillon</option>
              <option value="sent">Envoyée</option>
              <option value="paid">Payée</option>
            </select>
  
            <button
              class="bg-indigo-600 text-white px-3 py-1 rounded hover:bg-indigo-500"
              @click="saveEdit(invoice.id)"
            >
              💾 Sauvegarder
            </button>
            <button
              class="text-gray-500 hover:underline ml-2"
              @click="cancelEdit"
            >
              Annuler
            </button>
          </div>
  
          <!-- EN MODE AFFICHAGE -->
          <div v-else>
            <div class="flex justify-between items-start">
              <div>
                <span class="font-semibold text-indigo-600">{{ invoice.client_name }}</span>
                <div class="text-gray-700">Montant : {{ invoice.amount }} €</div>
                <div class="text-sm text-gray-500">Statut : {{ invoice.status }}</div>
              </div>
              <button
                class="text-sm text-gray-400 hover:text-indigo-600"
                @click="startEdit(invoice)"
              >✏️</button>
            </div>
            <div class="text-sm text-gray-500 mt-1">{{ formatDate(invoice.created_at) }}</div>
  
            <div class="mt-2 flex flex-wrap gap-2">
              <button
                class="text-sm text-red-600 hover:underline ml-auto"
                @click="deleteInvoice(invoice.id)"
              >🗑 Supprimer</button>
            </div>
          </div>
        </li>
      </ul>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted } from 'vue'
  import api from '../utils/api'
  
  const invoices = ref([])
  const editId = ref(null)
  const editClientName = ref('')
  const editAmount = ref(0)
  const editStatus = ref('draft')  // Initialiser avec un statut par défaut
  
  const formatDate = (dateStr) => new Date(dateStr).toLocaleDateString()
  
  onMounted(async () => {
    try {
      const invoiceRes = await api.get(`/invoices`)
      invoices.value = invoiceRes.data
    } catch (err) {
      console.error("Erreur chargement factures", err)
    }
  })
  
  const updateStatus = async (id, newStatus) => {
    const invoice = invoices.value.find(i => i.id === id)
    try {
      await api.patch(`/invoices/${id}`, { status: newStatus })
      invoice.status = newStatus
    } catch (err) {
      console.error("Erreur de mise à jour", err)
    }
  }
  
  const deleteInvoice = async (id) => {
    try {
      await api.delete(`/invoices/${id}`)
      invoices.value = invoices.value.filter(i => i.id !== id)
    } catch (err) {
      console.error("Erreur suppression", err)
    }
  }
  
  const startEdit = (invoice) => {
    editId.value = invoice.id
    editClientName.value = invoice.client_name
    editAmount.value = invoice.amount
    editStatus.value = invoice.status // Charger le statut dans l'éditeur
  }
  
  const cancelEdit = () => {
    editId.value = null
    editClientName.value = ''
    editAmount.value = 0
    editStatus.value = 'draft' // Réinitialiser le statut
  }
  
  const saveEdit = async (id) => {
    try {
      const payload = {
        client_name: editClientName.value.trim(),
        amount: parseInt(editAmount.value),
        status: editStatus.value,  // Ajouter le statut
      }
  
      if (!payload.client_name || isNaN(payload.amount)) {
        console.error("Champs invalides", payload)
        return
      }
  
      console.log('Payload envoyé à FastAPI :', payload)
  
      await api.patch(`/invoices/${id}`, payload)
  
      const invoice = invoices.value.find(i => i.id === id)
      invoice.client_name = payload.client_name
      invoice.amount = payload.amount
      invoice.status = payload.status  // Mise à jour du statut
  
      cancelEdit()
    } catch (err) {
      console.error("Erreur de sauvegarde", err.response?.data?.detail || err.message)
    }
  }
  </script>  