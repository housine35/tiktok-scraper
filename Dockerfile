# Utiliser une image de base légère avec Python 3.12
FROM python:3.12-slim

# Installer les dépendances système pour Node.js et Playwright
RUN apt-get update && apt-get install -y \
  curl \
  nodejs \
  npm \
  libnss3 \
  libatk1.0-0 \
  libatk-bridge2.0-0 \
  libcups2 \
  libdrm2 \
  libxkbcommon0 \
  libxcomposite1 \
  libxdamage1 \
  libxfixes3 \
  libxrandr2 \
  libgbm1 \
  libasound2 \
  libpango-1.0-0 \
  libcairo2 \
  && apt-get clean && rm -rf /var/lib/apt/lists/*

# Mettre à jour npm à une version stable
RUN npm install -g npm@10.8.2 && npm cache clean --force

# Définir le répertoire de travail
WORKDIR /app

# Copier package.json et package-lock.json (s'il existe)
COPY package*.json ./

# Installer Playwright
RUN npm install playwright@1.48.1 && npm cache clean --force

# Installer toutes les dépendances système pour Playwright
RUN npx playwright install-deps

# Installer le navigateur Chromium
RUN npx playwright install chromium

# Copier requirements.txt et installer les dépendances Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copier tout le code source
COPY . .

# Exposer le port
EXPOSE 8000

# Commande pour lancer FastAPI
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--log-level", "debug"]