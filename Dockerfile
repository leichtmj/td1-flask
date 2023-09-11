# Utilisez l’image Python 3.8 comme base
FROM python:3.8

# Installez Flask
RUN pip install Flask

# Définissez le répertoire de travail
WORKDIR /TD1

# Copiez le contenu actuel dans le répertoire de travail
COPY /TD1 /TD1

ENV FLASK_APP="hello.py"

# Exposez le port 5000 (port par défaut de Flask)
EXPOSE 5000

# Commande à exécuter lorsque le conteneur démarre
CMD ["flask", "run", "--host=0.0.0.0"]