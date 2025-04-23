# 🧾 QuillBill

**QuillBill** est une plateforme SaaS de facturation et de paiement en ligne destinée aux entrepreneurs et aux entreprises. Elle permet de :

- Créer et envoyer des factures professionnelles.
- Générer des liens de paiement sécurisés via Stripe.
- Gérer les paiements et les abonnements clients.
- Personnaliser l'expérience en fonction du secteur d'activité.

## 🚀 Fonctionnalités principales

- 🔐 Authentification sécurisée avec JWT.
- 💳 Intégration de Stripe Checkout pour les paiements.
- 📄 Génération automatique de factures PDF.
- 📬 Envoi de factures par email avec liens de paiement.
- 📊 Tableau de bord utilisateur pour le suivi des paiements.
- 🧩 Personnalisation des offres selon le secteur d'activité.

## 🛠️ Technologies utilisées

- **Frontend** : Vue.js 3, Vite, Tailwind CSS.
- **Backend** : FastAPI, PostgreSQL, SQLAlchemy.
- **Paiement** : Stripe API (Checkout & Billing).
- **Déploiement** : Docker, Docker Compose.

## 📦 Installation

### Prérequis

- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)
- [npm](https://www.npmjs.com/)

### Étapes

1. Cloner le dépôt :

   ```bash
   git clone https://github.com/HCairo/QB.git
   cd QB
2. Lancer les services avec Docker Compose et npm

  ```bash
  cd qb-back
  docker compose up --build

  cd qb-front
  npm install
  npm run dev
