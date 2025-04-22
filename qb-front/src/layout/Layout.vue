<template>
  <div class="flex h-screen">
    <aside class="w-64 bg-indigo-700 text-white p-6">
      <h2 class="text-xl font-bold mb-8">QuillBill</h2>
      <nav class="space-y-4">
  <RouterLink to="/" class="block hover:underline">🗃️ Dashboard</RouterLink>
  <RouterLink to="/dashboard/invoices" class="block hover:underline">📄 Factures</RouterLink>
  <RouterLink to="/dashboard/invoices/new" class="block hover:underline">➕ Nouvelle facture</RouterLink>


  <template v-if="!isAuthenticated">
    <RouterLink to="/login" class="block hover:underline">Se connecter</RouterLink>
    <RouterLink to="/register" class="block hover:underline">Créer un compte</RouterLink>
  </template>

  <button
    v-if="isAuthenticated"
    @click="logout"
    class="block hover:underline text-left w-full text-white"
  >
  🚪 Se déconnecter
  </button>
</nav>
    </aside>
    <div class="flex-1 bg-white overflow-y-auto p-8">
      <RouterView />
    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'
import { computed } from 'vue'

const router = useRouter()

const isAuthenticated = computed(() => {
  return !!localStorage.getItem('token')
})

const logout = () => {
  localStorage.removeItem('token')
  router.push('/')
}
</script>