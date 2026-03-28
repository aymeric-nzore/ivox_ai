FROM python:3.11-slim

# Définir le dossier de travail
WORKDIR /app

# Installer les dépendances d'abord (cache Docker)
COPY requirements.txt ./requirements.txt
RUN pip install --no-cache-dir --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Copier uniquement le code utile au runtime
COPY api ./api
COPY core ./core
COPY memory ./memory

EXPOSE 8000

#Commande pour lancer le serv fastapi
CMD [ "uvicorn" , "api.main:app" , "--host" , "0.0.0.0" , "--port" , "8000" ]