FROM node:slim

WORKDIR /app

# Installer les dépendances
COPY package*.json ./
RUN npm install

# Copier le reste du code
COPY . .

# Exposer le port Vite
EXPOSE 5173

# Démarrer Vite avec l’option --host
CMD ["npm", "run", "dev", "--", "--host"]