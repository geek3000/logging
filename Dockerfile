# Utilisez une image Python 3.9
FROM python:3.9

# Définissez le répertoire de travail dans le conteneur
WORKDIR /app

# Copiez les fichiers de l'application dans le conteneur
COPY requirements.txt .
COPY app.py .
COPY logger.py .

# Installez les dépendances de l'application
RUN pip install -r requirements.txt

# Exposez le port 5000
EXPOSE 5000

# Démarrez l'application Flask
CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]