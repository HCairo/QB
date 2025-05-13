import { createRouter, createWebHistory } from 'vue-router'
import Login from '../pages/Login.vue'
import Register from '../pages/Register.vue'
import Dashboard from '../pages/Dashboard.vue'
import Home from '../pages/Home.vue'
import Layout from '../layout/Layout.vue'
import CreateInvoice from '../pages/CreateInvoice.vue'
import InvoiceList from '../pages/InvoiceList.vue'
import StripePayment from '../pages/StripePayment.vue'
import OauthSuccess from '../pages/OauthSuccess.vue'
import CompleteProfile from '../pages/CompleteProfile.vue'

const isAuthenticated = () => !!localStorage.getItem('token')

const routes = [
  {
    path: '/',
    component: Home,
    beforeEnter: () => {
      if (isAuthenticated()) return '/dashboard'
    }
  },
  {
    path: '/login',
    component: Login,
    beforeEnter: () => {
      if (isAuthenticated()) return '/'
    }
  },
  { 
    path: '/oauth-success',
    component: OauthSuccess 
  },
  {
    path: '/register',
    component: Register,
    beforeEnter: () => {
      if (isAuthenticated()) return '/'
    }
  },
  { 
    path: '/complete-profile', 
    component: CompleteProfile 
  },
  {
    path: '/dashboard',
    component: Layout,
    beforeEnter: () => {
      if (!isAuthenticated()) return '/'
    },
    children: [
      { path: '', name: 'Dashboard', component: Dashboard },
      { path: 'invoices/new', name: 'CreateInvoice', component: CreateInvoice },
      { path: 'invoices', name: 'InvoiceList', component: InvoiceList }
    ]
  },
  {
    path: '/payment',
    component: StripePayment,
    beforeEnter: () => {
      if (!isAuthenticated()) return '/login'
    }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router