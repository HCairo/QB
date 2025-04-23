<template>
    <div>
      <button @click="handleCheckout" class="bg-indigo-600 text-white px-6 py-3 rounded hover:bg-indigo-500">
        Payer
      </button>
    </div>
</template>

<script setup>
import { loadStripe } from '@stripe/stripe-js'
import axios from 'axios'

const stripePromise = loadStripe(import.meta.env.VITE_STRIPE_PUBLIC_KEY)

const handleCheckout = async () => {
  const stripe = await stripePromise
  try {
    // Appelle le backend pour créer une session de paiement
    const { data } = await axios.post('http://localhost:8000/create-checkout-session')

    // Vérifie que l'URL de la session Stripe est valide
    if (data.sessionId) {
      // Redirige l'utilisateur vers Stripe Checkout avec l'ID de la session
      const result = await stripe.redirectToCheckout({ sessionId: data.sessionId })
      if (result.error) {
        console.error(result.error.message)
      }
    } else {
      console.error("Aucune URL de session Stripe retournée")
    }
  } catch (err) {
    console.error("Erreur lors de la création de la session Stripe", err)
  }
}
</script>