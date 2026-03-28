FROM python:3.11-slim

# Définir le dossier de travail
WORKDIR /app

#Copier tous les fichiers du projet
COPY . .

#Installer les dépendances
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 8000

#Commande pour lancer le serv fastapi
CMD [ "uvicorn" , "api.main:app" , "--host" , "0.0.0.0" , "--port" , "8000" ]